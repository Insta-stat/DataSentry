import pandas as pd
import os
import numpy as np
import sys
import json

# Add parent directory to sys.path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import z_categorize

pd.set_option('display.float_format', '{:.3f}'.format)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "raw_data", "reels.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "raw_data", "described_data.csv")

# Lightweight z-score implementation (replace SciPy dependency)
def simple_zscore(series: pd.Series) -> pd.Series:
    """Return z-scores for a numeric pandas Series. NaNs are preserved."""
    mean = series.mean(skipna=True)
    std = series.std(ddof=0, skipna=True)
    if std == 0 or np.isnan(std):
        # Avoid division by zero – return zeros or NaNs accordingly
        return pd.Series([0 if not np.isnan(v) else np.nan for v in series], index=series.index)
    return (series - mean) / std

def process_data():
    try:
        # Read the CSV file
        df = pd.read_csv(DATA_PATH)
        
        # Extract required fields
        processed_df = pd.DataFrame()
        processed_df['accountName'] = df['ownerUsername']
        processed_df['timestamp'] = pd.to_datetime(df['timestamp'])
        processed_df['videoPlayCount'] = pd.to_numeric(df['videoPlayCount'], errors='coerce').fillna(0)
        processed_df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce').fillna(0)
        processed_df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce').fillna(0)
        processed_df['caption'] = df['caption']
        processed_df['url'] = df['url']
        processed_df['videoDuration'] = pd.to_numeric(df['videoDuration'], errors='coerce').fillna(0)
        
        # Calculate engagement metrics
        total_followers = 10000  # Default value for demo
        processed_df['engagementRate'] = (processed_df['likesCount'] + processed_df['commentsCount']) / total_followers
        processed_df['commentRate'] = processed_df['commentsCount'] / total_followers
        processed_df['likeRate'] = processed_df['likesCount'] / total_followers
        processed_df['likeCommentRate'] = processed_df['likesCount'] / np.where(processed_df['commentsCount'] > 0, processed_df['commentsCount'], 1)
        processed_df['viralityIndex'] = processed_df['videoPlayCount'] / total_followers
        processed_df['performanceScore'] = (processed_df['engagementRate'] + processed_df['viralityIndex']) / 2
        
        # Calculate z-scores
        metrics = ['commentsCount', 'likesCount', 'videoPlayCount', 'videoDuration', 
                  'engagementRate', 'commentRate', 'likeRate', 'performanceScore']
        
        for metric in metrics:
            z_col = f'z{metric}'
            processed_df[z_col] = simple_zscore(processed_df[metric])
            mark_col = f'mark{metric.replace("Count", "").replace("Rate", "R")}'
            processed_df[mark_col] = processed_df[z_col].apply(z_categorize)
        
        # Save processed data
        processed_df.to_csv(OUTPUT_PATH, index=False)
        print(f"Data processed successfully and saved to {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    process_data()

