import tabula
import csv

def sicred_convert_pdf_to_csv(pdf_path, output_csv_path):
    # Read PDF and extract tables
    tabula.convert_into(pdf_path, output_csv_path, output_format="csv", options="--columns 1.1,2.2,3.3", pages='all')

    print("PDF converted to CSV successfully.")
""""
def append_columns_to_csv(csv_path, columns):
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

    print("Columns appended to CSV successfully.")
"""
