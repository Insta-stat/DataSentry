import pandas as pd
import os
import numpy as np
from scipy.stats import zscore
import sys

# Добавляем родительскую директорию в sys.path для импорта config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import z_categorize

pd.set_option('display.float_format', '{:.3f}'.format)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "raw_data", "reels.csv")

# Read the CSV file
df = pd.read_csv(DATA_PATH)

# Extract account name from inputUrl
df['accountName'] = df['ownerUsername']

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Rename columns to match expected format
df = df.rename(columns={
    'videoPlayCount': 'videoPlayCount',
    'likesCount': 'likesCount',
    'commentsCount': 'commentsCount',
    'videoDuration': 'videoDuration'
})

# Ensure numeric columns are properly converted
numeric_columns = ['videoPlayCount', 'likesCount', 'commentsCount', 'videoDuration']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Replace any negative values with 0
for metric in numeric_columns:
    if metric in df.columns:
        negative_count = (df[metric] < 0).sum()
        if negative_count > 0:
            print(f"Найдено {negative_count} отрицательных значений в {metric}, заменяем на 0")
            df[metric] = df[metric].clip(lower=0)

# Calculate engagement metrics
df['engagementRate'] = (df['likesCount'] + df['commentsCount']) / df['videoPlayCount'].replace(0, 1)
df['commentRate'] = df['commentsCount'] / df['videoPlayCount'].replace(0, 1)
df['likeRate'] = df['likesCount'] / df['videoPlayCount'].replace(0, 1)
df['likeCommentRate'] = df['commentsCount'] / df['likesCount'].replace(0, 1)
df['viralityIndex'] = df['videoPlayCount'] / (df['likesCount'] + df['commentsCount'] + 1)
df['performanceScore'] = (
    df['engagementRate'] * 0.4 +
    df['likeRate'] * 0.3 +
    df['commentRate'] * 0.2 +
    (1 / (df['viralityIndex'] + 1)) * 0.1
)

# Calculate z-scores for metrics
metrics = [
    'commentsCount', 'likesCount', 'videoPlayCount', 'videoDuration',
    'engagementRate', 'commentRate', 'likeRate', 'performanceScore'
]

def safe_zscore(x):
    x_clean = x.dropna()
    if len(x_clean) > 1 and x_clean.std(ddof=1) > 0:
        z = pd.Series(zscore(x_clean, ddof=1), index=x_clean.index)
        return z.reindex(x.index, fill_value=float('nan'))
    return pd.Series([float('nan')] * len(x), index=x.index)

for metric in metrics:
    z_col = 'z' + metric[0].upper() + metric[1:]
    df[z_col] = df.groupby('accountName')[metric].transform(safe_zscore)

# Apply categorization
df['markComments'] = df['zCommentsCount'].apply(z_categorize)
df['markLikes'] = df['zLikesCount'].apply(z_categorize)
df['markPlay'] = df['zVideoPlayCount'].apply(z_categorize)
df['markDuration'] = df['zVideoDuration'].apply(z_categorize)
df['markER'] = df['zEngagementRate'].apply(z_categorize)
df['markCR'] = df['zCommentRate'].apply(z_categorize)
df['markLR'] = df['zLikeRate'].apply(z_categorize)
df['markPS'] = df['zPerformanceScore'].apply(z_categorize)

# Save the processed data
df.to_csv(os.path.join(BASE_DIR, 'raw_data', 'described_data.csv'), index=False)
print("Data processing completed successfully")
print("\nFirst few rows of processed data:")
print(df[['accountName', 'timestamp', 'videoPlayCount', 'likesCount', 'commentsCount', 'engagementRate']].head())

