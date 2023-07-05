import tabula
import csv
import os

def bb_convert_pdf_to_csv(pdf_path, output_csv_path):
    # Read PDF and extract tables
    tabula.convert_into(pdf_path, output_csv_path, output_format="csv", guess=False, pages='all') #options="--columns 10.1,20.2,30.3")
