import pandas as pd
import csv

def santander_convert_xls_to_csv(xls_path, csv_path):
    # Read the XLS file into a DataFrame
    xls_data = pd.read_excel(xls_path, skiprows=5)
    
    # Extract the data starting from line 6
    #xls_data = xls_data.iloc[4:] doesn`t need anymore because of the skiprows above
    total_row_index = xls_data[xls_data.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)].index[0]
    xls_data = xls_data.loc[:total_row_index]

    # Save the DataFrame as a CSV file
    xls_data.to_csv(csv_path, index=False)
