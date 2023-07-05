import csv

def bradesco_read_csv(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        next(reader)
        for row in reader:
            if row[4] == '' and row[3] == '':
                continue          
            print('<STMTTRN>\n')
            if row[4][0:1] == '-':
                print('<TRNTYPE>DEBIT\n')
            else:
                print('<TRNTYPE>CREDIT\n')
            print(f'<DTPOSTED>{row[0]}</DTPOSTED>\n')
            if row[4][0:1] == '-':
                print(f'<TRNAMT>{row[4]}</TRNAMT>\n')
            else:
                print(f'<TRNAMT>{row[3]}</TRNAMT>\n')
            print(f'<FITID>{row[1]}</FITID>\n')
            print(f'<MEMO>{row[1]}<MEMO>\n')
            print('</STMTTRN>\n')

# Specify the CSV file path to read
csv_file = '~/Bradesco/xls_to_csv.csv'

# Read and print CSV contents
bradesco_read_csv(csv_file)
