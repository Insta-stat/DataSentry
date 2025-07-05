import os
import csv
import requests
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse
import openai
from openai import OpenAI
import pandas as pd
from datetime import datetime

# Безопасный импорт API ключа
try:
    from creds.accesses import gpt_api
except ImportError:
    gpt_api = os.getenv('OPENAI_API_KEY')

class GPTTranscriptor:
    def __init__(self, api_key=None):
        """
        Инициализация транскриптора
        
        Args:
            api_key (str): OpenAI API ключ. Если None, будет взят из модуля creds или переменной окружения
        """
        self.client = OpenAI(
            api_key=api_key or gpt_api or os.getenv('OPENAI_API_KEY')
        )
        
        # Директории для сохранения результатов
        self.base_dir = Path(__file__).parent.parent
        self.transcripts_dir = self.base_dir / "transcripts"
        self.temp_dir = self.base_dir / "temp_audio"
        
        # Создаем директории если их нет
        self.transcripts_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    def extract_video_id_from_url(self, video_url):
        """Извлекаем уникальный ID из MP4 URL для именования файлов"""
        # Извлекаем часть URL для создания уникального имени
        parsed = urlparse(video_url)
        # Берем последнюю часть пути без расширения
        filename = Path(parsed.path).stem
        if not filename or filename == '':
            # Если не можем извлечь из пути, используем хеш URL
            import hashlib
            filename = hashlib.md5(video_url.encode()).hexdigest()[:12]
        return filename
    
    def validate_url(self, url):
        """Простая проверка URL"""
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(url)
            return bool(parsed.scheme and parsed.netloc), "URL корректный"
        except:
            return False, "Неверный URL"
    
    def download_mp4(self, url, filepath):
        """Простое скачивание MP4 файла"""
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            print(f"📥 Скачиваем файл...")
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ Скачано: {file_size / 1024 / 1024:.2f}MB")
            
            return file_size > 1000  # Проверяем что файл больше 1KB
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def transcribe_audio(self, audio_path):
        """
        Транскрибирует аудио через OpenAI Whisper API
        
        Args:
            audio_path (str): Путь к аудио/видео файлу
            
        Returns:
            str: Оригинальный транскрибированный текст
        """
        try:
            print(f"🎤 Транскрибируем аудио...")
            
            with open(audio_path, 'rb') as audio_file:
                # Получаем оригинальный текст (автоопределение языка)
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                text = response.text.strip()
                
                print(f"✅ Транскрипция завершена: {len(text)} символов")
                return text
                
        except Exception as e:
            print(f"❌ Ошибка транскрипции: {str(e)}")
            return None
    
    def save_transcript(self, video_id, transcript, original_url):
        """Сохраняет транскрипт в файл"""
        try:
            output_file = self.transcripts_dir / f"{video_id}.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {original_url}\n")
                f.write(f"ID: {video_id}\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
                f.write(transcript)
            
            print(f"💾 Сохранено: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Удаляет временные файлы"""
        try:
            for file in self.temp_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            print("🧹 Временные файлы очищены")
        except Exception as e:
            print(f"❌ Ошибка при очистке временных файлов: {str(e)}")
    
    def process_videos(self, csv_path):
        """
        Основная функция обработки видео из CSV
        
        Args:
            csv_path (str): Путь к CSV файлу с URL видео
        """
        try:
            # Читаем CSV
            df = pd.read_csv(csv_path)
            print(f"📊 Загружено {len(df)} записей из CSV")
            
            # Находим колонку с URL
            url_column = None
            for col in ['videoUrl', 'url', 'video_url', 'mp4_url']:
                if col in df.columns:
                    url_column = col
                    break
            
            if url_column is None:
                print("❌ Не найдена колонка с URL видео (videoUrl, url, video_url, mp4_url)")
                return
            
            print(f"✅ Используем колонку: {url_column}")
            
            # Обрабатываем каждое видео
            processed = 0
            failed = 0
            
            for index, row in df.iterrows():
                url = row[url_column]
                if pd.isna(url):
                    continue
                
                print(f"\n📹 Видео {index + 1}/{len(df)}: {url[:50]}...")
                
                # Извлекаем ID для названия файла
                video_id = self.extract_video_id_from_url(url)
                
                # Проверяем, не обработано ли уже
                output_file = self.transcripts_dir / f"{video_id}.txt"
                if output_file.exists():
                    print(f"⏭️ Уже обработано: {output_file}")
                    processed += 1
                    continue
                
                # Скачиваем MP4
                video_path = self.temp_dir / f"{video_id}.mp4"
                if not self.download_mp4(url, video_path):
                    failed += 1
                    continue
                
                # Транскрибируем
                transcript = self.transcribe_audio(str(video_path))
                if not transcript:
                    failed += 1
                    continue
                
                # Сохраняем результат
                self.save_transcript(video_id, transcript, url)
                processed += 1
                
                # Очищаем временный файл
                if video_path.exists():
                    video_path.unlink()
                
            print(f"\n🎯 Итого: {processed} обработано, {failed} ошибок")
            
        except Exception as e:
            print(f"💥 Критическая ошибка: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Основная функция для запуска транскриптора"""
    print("🎙️ Запуск GPT Transcriptor для MP4 файлов")
    
    try:
        transcriptor = GPTTranscriptor()
        # Определяем путь относительно расположения скрипта
        script_dir = Path(__file__).parent
        csv_path = script_dir.parent / "input_data" / "videos.csv"
        
        if not csv_path.exists():
            print(f"❌ Файл не найден: {csv_path}")
            print("💡 Создайте файл input_data/videos.csv с колонкой videoUrl")
        else:
            print(f"✅ Найден файл: {csv_path}")
            transcriptor.process_videos(str(csv_path))
        print("🏁 Обработка завершена!")
    except Exception as e:
        print(f"💥 Критическая ошибка: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
