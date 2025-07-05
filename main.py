#!/usr/bin/env python3
"""
DataSentry - Main entry point for the analytics platform
"""

import os
import sys

def main():
    """Main entry point for the application"""
    print("DataSentry Analytics Platform")
    print("=============================")
    print()
    print("Available commands:")
    print("1. Run dashboard: streamlit run streamlit_dashboard.py")
    print("2. Run transcriptor: python external_analysis/gpt_transcriptor.py")
    print("3. Process data: python external_analysis/descriptive_stat.py")
    print()
    print("For more information, see README.md")

if __name__ == "__main__":
    main()
