# 🚨 Решение проблем с GPT Transcriptor

## Проблема: Instagram URL не скачивается (Timeout)

### 🔍 **Причины:**
- Instagram URL истекает через некоторое время
- Файл слишком большой для Whisper API (>25MB)  
- Сетевые ограничения/блокировки
- Instagram требует специальной авторизации

### ✅ **Решения:**

#### **1. Обновите URL Instagram**
Instagram генерирует временные ссылки. Получите новую ссылку:
```bash
# Замените истекший URL в videos.csv на новый
```

#### **2. Используйте локальные файлы**
Скачайте MP4 вручную и используйте локальные пути:

```csv
videoUrl
/path/to/local/video1.mp4
/path/to/local/video2.mp4
```

Обновите код для поддержки локальных файлов:
```python
def process_local_file(self, file_path):
    """Обрабатывает локальный файл"""
    if not Path(file_path).exists():
        print(f"❌ Файл не найден: {file_path}")
        return None
    
    # Копируем в temp директорию
    video_id = Path(file_path).stem
    temp_path = self.temp_dir / f"{video_id}.mp4"
    shutil.copy2(file_path, temp_path)
    
    return str(temp_path)
```

#### **3. Используйте альтернативные источники**
Вместо прямых Instagram URL используйте:
- YouTube (публичные видео)
- Файлы на Google Drive/Dropbox с публичным доступом
- Собственный сервер с MP4 файлами

### 🔧 **Тестирование с публичным файлом:**

Создайте `test_public.csv`:
```csv
videoUrl
https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4
```

Этот файл небольшой и всегда доступен для тестирования.

## Проблема: "API key not found"

### ✅ **Решение:**
```bash
# Установите переменную окружения
export OPENAI_API_KEY="sk-your-key-here"

# Или добавьте в creds/accesses.py
echo 'gpt_api = "sk-your-key-here"' >> creds/accesses.py
```

## Проблема: Файл слишком большой (>25MB)

### ✅ **Решения:**

#### **1. Сжатие видео**
```bash
# Установите ffmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu

# Сжмите видео
ffmpeg -i input.mp4 -vcodec h264 -b:v 1000k -acodec aac output.mp4
```

#### **2. Извлечение только аудио**
```bash
# Извлеките только аудио
ffmpeg -i input.mp4 -vn -acodec mp3 -ab 128k output.mp3
```

#### **3. Разделение на части**
```bash
# Разделите длинное видео на части по 5 минут
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 300 -f segment part_%03d.mp4
```

## Работа с локальными файлами

### Создайте улучшенную версию для локальных файлов:

```python
def process_videos_csv_mixed(self, csv_path="input_data/videos.csv"):
    """Обрабатывает как URL, так и локальные файлы"""
    
    for i, url_or_path in enumerate(urls, 1):
        print(f"\n🎬 Обрабатываем {i}/{len(urls)}")
        
        # Определяем тип: URL или локальный файл
        if url_or_path.startswith(('http://', 'https://')):
            # Это URL
            video_path = self.download_mp4_as_audio(url_or_path)
            original_source = url_or_path
        else:
            # Это локальный файл
            if Path(url_or_path).exists():
                video_path = self.copy_local_file(url_or_path)
                original_source = f"Локальный файл: {url_or_path}"
            else:
                print(f"❌ Локальный файл не найден: {url_or_path}")
                continue
        
        if not video_path:
            continue
            
        # Дальше обычная обработка...
```

## Альтернативные инструменты

### Если проблемы с Instagram продолжаются:

#### **1. yt-dlp для Instagram**
```bash
pip install yt-dlp
yt-dlp "https://www.instagram.com/p/POST_ID/" -f "best[ext=mp4]"
```

#### **2. Галерия-DL**
```bash
pip install gallery-dl
gallery-dl "https://www.instagram.com/p/POST_ID/"
```

#### **3. Instaloader**
```bash
pip install instaloader
instaloader --dirname-pattern="" --filename-pattern="{shortcode}" -- -POST_ID
```

## Проверка готовности системы

Запустите диагностику:
```bash
python -c "
import requests
from external_analysis.gpt_transcriptor import GPTTranscriptor

print('🔍 Диагностика системы...')

# Тест сети
try:
    r = requests.get('https://httpbin.org/get', timeout=5)
    print('✅ Интернет соединение работает')
except:
    print('❌ Проблемы с интернетом')

# Тест создания объекта
try:
    t = GPTTranscriptor.__new__(GPTTranscriptor)
    print('✅ Класс транскриптора доступен')
except Exception as e:
    print(f'❌ Проблема с классом: {e}')

print('🏁 Диагностика завершена')
" 