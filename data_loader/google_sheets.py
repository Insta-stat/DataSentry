from creds.accesses import client
import pandas as pd

if client is not None:
    try:
        # Load data for Google Sheets upload
        import os
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data_path = os.path.join(base_dir, "raw_data", "described_data.csv")
        df = pd.read_csv(data_path)
        
        # Create a summary or use the full data
        spreadsheet = client.open("Content Analysis")
        worksheet = spreadsheet.worksheet("Лист2")
        
        # Upload the data (first 1000 rows to avoid quota limits)
        data_to_upload = df.head(1000)
        worksheet.update([data_to_upload.columns.values.tolist()] + data_to_upload.values.tolist())
        print("Google Sheets updated successfully")
    except Exception as e:
        print(f"Error updating Google Sheets: {e}")
else:
    print("Google Sheets client not available")
