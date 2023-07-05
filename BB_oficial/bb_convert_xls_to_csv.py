import pandas as pd

def bb_convert_xls_to_csv(xls_path, csv_path):
    data = pd.read_excel(xls_path)  # Read Excel file into DataFrame
    df = pd.DataFrame(data)

    # Filter rows where the first column is not empty
    df_filtered = df.iloc[6:]

    # Convert filtered DataFrame to CSV
    df_filtered.to_csv(csv_path, index=False)

