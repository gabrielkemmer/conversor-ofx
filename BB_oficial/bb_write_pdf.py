import pandas as pd
from PyPDF2 import PdfReader

reader = PdfReader("~/Bb.pdf")

new_data = []
for page in reader.pages[0:10]:
    new_data.extend(page.extract_text().split('\n'))

pdf_list = []
for row in new_data:
    pdf_row = list(filter(None, row.split(' ')))
    pdf_list.append(pdf_row)
print(pdf_list[7:])

# Create a dictionary with the column names
columns = {
    'Data Balancete': [],
    'Data Movimento': [],
    'Ag. Origem': [],
    'Lote': [],
    'Historico': [],
    'Documento': [],
    'Valor': [],
    'Saldo': [],
    'Column 9': [],  # Adjust the number of columns accordingly
    'Column 10': [],
    'Column 11': [],
    'Column 12': [],
    'Column 13': [],
    'Column 14': [],
    'Column 15': []
}


# Create a DataFrame from the dictionary
df = pd.DataFrame(columns)

data = []
for item in pdf_list:
    data.append(item)
    
df = df.append(pd.DataFrame(data, columns=df.columns))

# Save the DataFrame to a spreadsheet file (e.g., CSV)
output_file = '~/BB/spreadshet.csv'
df.to_csv(output_file, index=False)

print(f"Spreadsheet created and saved to {output_file}")


