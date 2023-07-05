import csv
from PyPDF2 import PdfReader

reader = PdfReader("~/Bradesco.pdf")
page = reader.pages[0]

new_data = page.extract_text().split('\n')

pdf_list = []
for row in new_data:
    pdf_row = list(filter(None, row.split(' ')))
    pdf_list.append(pdf_row)
#print(pdf_list)

for row in pdf_list[4:]:
    if len(row) > 2 and len(row) < 8:
        print(row)
"""
for row in pdf_list[4:]:
    if len(row) < 5:
        continue
    if row[2] == '' and row[3] == '':
        continue
    print('<STMTTRN>\n')
    if row[1][0:1] == '-':
        print('<TRNTYPE>DEBIT\n')
    else:
        print('<TRNTYPE>CREDIT\n')
    print(f'<DTPOSTED>{row[0][0:8]}</DTPOSTED>\n')
    if row[1][0:1] == '-':
        print(f'<TRNAMT>{row[2] + row[3]}</TRNAMT>\n')
    else:
        print(f'<TRNAMT>{row[2]}</TRNAMT>\n')
    print(f'<FITID>{row[0]}</FITID>\n')
    print(f'<MEMO>{row[0]}<MEMO>\n')
    print('</STMTTRN>\n')
"""

