import csv
import os
from datetime import datetime

def cora_convert_csv_to_ofx(csv_folder, ofx_file):
    with open(csv_folder, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        first = None
        last = None
        for row in reader:
            if first is None:
                first = row
            last = row

    with open(ofx_file, 'w') as ofx:
        ofx.write('OFXHEADER:100\n')
        ofx.write('DATA:OFXSGML\n')
        ofx.write('VERSION:102\n')
        ofx.write('SECURITY:NONE\n')
        ofx.write('ENCODING:UTF-8\n')
        ofx.write('COMPRESSION:NONE\n')
        ofx.write('OLDFILEUID:NONE\n')
        ofx.write('NEWFILEUID:NONE\n')
        ofx.write('<OFX>\n')
        ofx.write('<SIGNONMSGSRSV1>\n')
        ofx.write('<SONRS>\n')
        ofx.write('<STATUS>\n')
        ofx.write('<CODE>0\n')
        ofx.write('<SEVERITY>INFO\n')
        ofx.write('</STATUS>\n')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ofx.write(f'<DTSERVER>{timestamp}[0:GMT]\n')
        ofx.write('<LANGUAGE>POR\n')
        ofx.write('<FI>\n')
        ofx.write('<ORG>CORA PAGAMENTOS LTDA\n')
        ofx.write('<FID>0403\n')
        ofx.write('</FI>\n')
        ofx.write('</SONRS>\n')
        ofx.write('</SIGNONMSGSRSV1>\n')
        ofx.write('<BANKMSGSRSV1>\n')
        ofx.write('<STMTTRNRS>\n')
        ofx.write('<TRNUID>1\n')
        ofx.write('<STATUS>\n')
        ofx.write('<CODE>0\n')
        ofx.write('<SEVERITY>INFO\n')
        ofx.write('</STATUS>\n')
        ofx.write('<STMTRS>\n')
        ofx.write('<CURDEF>BRL\n')
        ofx.write('<BANKACCTFROM>\n')
        ofx.write('<BANKID>0403\n')
        ofx.write('<BRANCHID>1\n')
        ofx.write('<ACCTTYPE>CHECKING\n')
        ofx.write('</BANKACCTFROM>\n')
        ofx.write('<BANKTRANLIST>\n')
        timestamp_format = '%Y%m%d%H%M%S'
        dtstart = datetime.strptime(last[0], '%d/%m/%Y').strftime(timestamp_format) + '[0:GMT]'
        dtend = datetime.strptime(first[0], '%d/%m/%Y').strftime(timestamp_format) + '[0:GMT]'
        ofx.write('<DTSTART>{}</DTSTART>\n'.format(dtstart))
        ofx.write('<DTEND>{}</DTEND>\n'.format(dtend))
        with open(csv_folder, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader)
            for row in reader:
                dtposted = datetime.strptime(row[0], '%d/%m/%Y').strftime(timestamp_format) + '[0:GMT]'
                ofx.write('<STMTTRN>\n')
                if row[2] == "DÉBITO":
                    ofx.write('<TRNTYPE>DEBIT</TRNTYPE>\n')
                if row[2] == "CRÉDITO":    
                    ofx.write('<TRNTYPE>CREDIT</TRNTYPE>\n')    
                ofx.write(f'<DTPOSTED>{dtposted}</DTPOSTED>\n')
                ofx.write(f'<TRNAMT>{row[4]}</TRNAMT>\n')
                if row[2] == "DÉBITO":
                    ofx.write(f'<MEMO>DEBIT - {row[3]}</MEMO>\n')
                if row[2] == "CRÉDITO":   
                    ofx.write(f'<MEMO>CREDIT - {row[3]}</MEMO>\n') 
                ofx.write('</STMTTRN>\n')

        ofx.write('</BANKTRANLIST>\n')
        ofx.write('</STMTRS>\n')
        ofx.write('</STMTTRNRS>\n')
        ofx.write('</BANKMSGSRSV1>\n')
        ofx.write('</OFX>\n')
"""
actual_directory = os.getcwd()
path = os.path.join(actual_directory, 'cora/')

csv_folder = '/Users/gabrielcarvalho/Desktop/conversor-novo/cora/cora_csv.csv'
ofx_file = path + 'csv_to_ofx_output.ofx'
cora_convert_csv_to_ofx(csv_folder, ofx_file)
"""