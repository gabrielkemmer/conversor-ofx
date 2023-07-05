import tabula
import csv

def cora_convert_pdf_to_csv(pdf_path, output_csv_path):
    # Read PDF and extract tables
    tables = tabula.read_pdf(pdf_path, pages='all')
    
    # Convert each table to a CSV file
    for i, table in enumerate(tables):
        table.to_csv(f"{output_csv_path}_{i+1}.csv", index=False)

    print("PDF converted to CSV successfully.")

def cora_append_columns_to_csv(csv_path, columns):
    # Read the existing contents of the CSV file
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        existing_content = list(reader)

    # Insert the new columns at the first row
    existing_content.insert(0, columns)

    # Write the updated content back to the CSV file
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_content)


pdf_path = '/Users/gabrielcarvalho/Desktop/conversor-novo/cora/cora_pdf.pdf'
output_csv_path = '/Users/gabrielcarvalho/Desktop/conversor-novo/cora/cora_pdf_to_csv'

csv_path = '/Users/gabrielcarvalho/Desktop/conversor-novo/cora/cora_pdf_to_csv_1.csv'
columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']

cora_convert_pdf_to_csv(pdf_path, output_csv_path)

cora_append_columns_to_csv(csv_path, columns)


