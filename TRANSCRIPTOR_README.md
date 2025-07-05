# GPT Transcriptor - Транскрипция MP4 видео через OpenAI Whisper

Простой и эффективный инструмент для автоматической транскрипции MP4 видео с прямых ссылок.

## Возможности

- 📥 Скачивание MP4 файлов по прямым URL
- 🎤 Транскрипция через OpenAI Whisper API
- 🌍 **Автоматическое определение языка и получение оригинального текста**
- 📄 Сохранение текстов в удобном формате
- 🔄 Автоматический пропуск уже обработанных файлов
- 🧹 Автоматическая очистка временных файлов

## Требования

### Для пользователей из России
⚠️ **ВАЖНО**: Instagram заблокирован в РФ. Необходимо включить VPN перед использованием!

### Системные требования
- Python 3.7+
- OpenAI API ключ

## Установка

1. Установите зависимости:
```bash
pip install -r requirements_transcriptor.txt
```

2. Настройте API ключ OpenAI:
   - Добавьте в `creds/accesses.py`: `gpt_api = "your-api-key"`
   - Или установите переменную окружения: `OPENAI_API_KEY=your-api-key`

## Использование

### Формат CSV файла
Создайте файл `input_data/videos.csv` с колонкой URL:

```csv
videoUrl
https://instagram.fdac7-1.fna.fbcdn.net/...mp4
https://example.com/video2.mp4
```

### Запуск транскрипции

```python
from external_analysis.gpt_transcriptor import GPTTranscriptor

# Создаем транскриптор
transcriptor = GPTTranscriptor()

# Обрабатываем видео из CSV
transcriptor.process_videos("input_data/videos.csv")
```

Или запустите напрямую:
```bash
python external_analysis/gpt_transcriptor.py
```

## Структура файлов

```
DataSentry/
├── external_analysis/
│   └── gpt_transcriptor.py      # Основной модуль
├── input_data/
│   └── videos.csv               # CSV с URL видео
├── transcripts/                 # Готовые транскрипты
├── temp_audio/                  # Временные файлы (авто-очистка)
└── requirements_transcriptor.txt
```

## Результат

Транскрипты сохраняются в папке `transcripts/` в формате:

```
URL: https://example.com/video.mp4
ID: video_unique_id
Дата: 2024-01-15 14:30:00
--------------------------------------------------
Original transcribed text in the source language...
```

## Поддерживаемые форматы

- Прямые ссылки на MP4 файлы
- Instagram video URLs (с VPN для РФ)
- Любые публично доступные видео URL

## Ограничения

- Максимальный размер файла: 25MB (лимит Whisper API)
- Поддерживаемые языки: все языки OpenAI Whisper

## Troubleshooting

Для решения проблем см. [README_TROUBLESHOOTING.md](README_TROUBLESHOOTING.md)