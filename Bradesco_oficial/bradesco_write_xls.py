import pandas as pd

def bradesco_convert_xls_to_csv(xls_path):
    # Read the XLS file into a DataFrame
    xls_data = pd.read_excel(xls_path, skiprows=7)
    print(xls_data)
    #total_row_index = xls_data[xls_data.iloc[:, 0].astype(str).str.contains('Saldo da Conta', case=False, na=True)].index[0]
    #xls_data = xls_data.loc[:total_row_index]



if __name__ == '__main__':
    xls_path = '~/Bradesco.xls' # Specify the path to your XLS file
    bradesco_convert_xls_to_csv(xls_path)