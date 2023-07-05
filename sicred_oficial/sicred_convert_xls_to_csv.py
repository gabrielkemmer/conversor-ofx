import pandas as pd
import csv

def sicred_convert_xls_to_csv(xls_path, csv_path):
    # Read the XLS file into a DataFrame
    xls_data = pd.read_excel(xls_path, skiprows=8)
    total_row_index = xls_data[xls_data.iloc[:, 0].astype(str).str.contains('Saldo da Conta', case=False, na=True)].index[0]
    xls_data = xls_data.loc[:total_row_index]

    # Save the DataFrame as a CSV file
    xls_data.to_csv(csv_path, index=False)

    print("XLS converted to CSV successfully.")

