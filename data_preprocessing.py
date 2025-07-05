#!/usr/bin/env python3
"""
DataSentry - Data preprocessing utilities
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def clean_data(df):
    """
    Clean and preprocess raw data
    
    Args:
        df (pd.DataFrame): Raw data frame
        
    Returns:
        pd.DataFrame: Cleaned data frame
    """
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df[col] = df[col].fillna(0)
    
    # Convert timestamps if needed
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def validate_data(df):
    """
    Validate data quality
    
    Args:
        df (pd.DataFrame): Data frame to validate
        
    Returns:
        dict: Validation results
    """
    results = {
        'total_rows': len(df),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict()
    }
    
    return results

def main():
    """Main preprocessing function"""
    print("DataSentry Data Preprocessing")
    print("============================")
    print("This module provides data cleaning and validation utilities.")
    print("Import functions: clean_data, validate_data")

if __name__ == "__main__":
    main()
