# DataSentry

DataSentry is a comprehensive analytics platform for Instagram content analysis and video transcription using OpenAI Whisper API.

## Features

### 📊 Analytics Dashboard
- **Streamlit-based interactive dashboard** with three main tabs:
  - **Общая статистика**: Overview of content performance metrics
  - **Метрики детально**: Detailed metrics analysis with statistical thresholds
  - **Анализ контента**: Content analysis and insights

### 🎥 Video Transcription System
- **GPT Transcriptor**: Automated MP4 video transcription using OpenAI Whisper API
- **Batch Processing**: Process multiple videos from CSV input
- **Auto-language Detection**: Automatically detects and transcribes in original language
- **Smart File Management**: Skips already processed videos and cleans up temporary files

### 📈 Statistical Analysis
- **Configurable Thresholds**: 
  - HOT threshold (viral content): μ + 2σ
  - Very Successful threshold: μ + 1σ
- **Visual Indicators**: Color-coded threshold lines on graphs
- **Comprehensive Metrics**: Detailed statistical analysis with visual representations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Insta-stat/DataSentry.git
cd DataSentry
```

2. Install dependencies:
```bash
pip install -r requirements_transcriptor.txt
```

3. Set up OpenAI API key:
   - Create a `creds/` directory
   - Add your OpenAI API key to the credentials

## Usage

### Running the Dashboard
```bash
streamlit run streamlit_dashboard.py
```

### Video Transcription
1. Prepare your video URLs in `input_data/videos.csv`
2. Run the transcriptor:
```python
python external_analysis/gpt_transcriptor.py
```

For detailed transcription setup and troubleshooting, see:
- [Transcriptor README](TRANSCRIPTOR_README.md)
- [Troubleshooting Guide](README_TROUBLESHOOTING.md)

## Project Structure

```
DataSentry/
├── streamlit_dashboard.py      # Main dashboard application
├── config.py                   # Configuration settings
├── external_analysis/
│   ├── gpt_transcriptor.py    # Video transcription system
│   └── descriptive_stat.py    # Statistical analysis functions
├── data_loader/               # Data loading utilities
├── input_data/               # Input CSV files (gitignored)
├── transcripts/              # Generated transcripts (gitignored)
├── temp_audio/              # Temporary audio files (gitignored)
└── creds/                   # API credentials (gitignored)
```

## Configuration

Edit `config.py` to customize:
- Statistical thresholds for content analysis
- Dashboard appearance settings
- API configurations

## Key Features

### Dashboard Visualizations
- **Purple main graphs** with elegant color scheme
- **Red threshold lines** for viral content identification
- **Green threshold lines** for very successful content
- **Interactive filtering** and detailed statistics

### Transcription System
- **Robust error handling** with retry logic
- **VPN compatibility** for region-restricted content
- **Automatic cleanup** of temporary files
- **Progress tracking** and logging

## Dependencies

- `streamlit` - Web dashboard framework
- `openai` - OpenAI API client
- `requests` - HTTP requests handling
- `pandas` - Data manipulation
- `plotly` - Interactive visualizations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the Insta-stat analytics suite.

## Support

For issues and questions:
- Check the [Troubleshooting Guide](README_TROUBLESHOOTING.md)
- Review the [Transcriptor Documentation](TRANSCRIPTOR_README.md)
- Open an issue on GitHub 