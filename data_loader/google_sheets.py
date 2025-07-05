from creds.accesses import client
from external_analysis.descriptive_stat import top_by_account

spreadsheet = client.open("Content Analysis")
worksheet = spreadsheet.worksheet("Лист2")


worksheet.update([top_by_account.columns.values.tolist()] + top_by_account.values.tolist())
