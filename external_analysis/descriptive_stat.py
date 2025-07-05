import pandas as pd
import os
import numpy as np
from scipy.stats import zscore
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

def process_data():
    try:
        # Read the CSV file
        df = pd.read_csv(DATA_PATH)
        
        # Extract required fields
        df['accountName'] = df['ownerUsername']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['videoPlayCount'] = pd.to_numeric(df['videoPlayCount'], errors='coerce')
        df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce')
        df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce')
        df['videoDuration'] = pd.to_numeric(df['videoDuration'], errors='coerce')
        
        # Calculate engagement metrics
        df['engagementRate'] = (df['likesCount'] + df['commentsCount']) / df['videoPlayCount']
        df['commentRate'] = df['commentsCount'] / df['videoPlayCount']
        df['likeRate'] = df['likesCount'] / df['videoPlayCount']
        df['likeCommentRate'] = df['likesCount'] / (df['commentsCount'] + 1)  # Add 1 to avoid division by zero
        df['viralityIndex'] = df['videoPlayCount'] / (df['likesCount'] + df['commentsCount'] + 1)
        df['performanceScore'] = (df['engagementRate'] + df['commentRate'] + df['likeRate']) / 3
        
        # Replace inf and nan with 0
        df = df.replace([np.inf, -np.inf], 0)
        df = df.fillna(0)
        
        # Calculate z-scores
        metrics = ['commentsCount', 'likesCount', 'videoPlayCount', 'videoDuration', 
                  'engagementRate', 'commentRate', 'likeRate', 'performanceScore']
        
        for metric in metrics:
            z_col = f'z{metric}'
            df[z_col] = zscore(df[metric], nan_policy='omit')
            df[f'mark{metric.replace("Count", "").replace("Rate", "R").replace("Score", "S")}'] = df[z_col].apply(z_categorize)
            
        # Save processed data
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"Data processed successfully and saved to {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    process_data()

