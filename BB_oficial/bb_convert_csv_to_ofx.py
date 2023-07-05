import csv
import os

def bb_convert_csv_to_ofx(csv_file, ofx_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        with open(ofx_file, 'w') as ofx:
            ofx.write('OFXHEADER:100\n')
            ofx.write('DATA:OFXSGML\n')
            ofx.write('VERSION:102\n')
            ofx.write('SECURITY:NONE\n')
            ofx.write('ENCODING:USASCII\n')
            ofx.write('CHARSET:1252\n')
            ofx.write('COMPRESSION:NONE\n')
            ofx.write('OLDFILEUID:NONE\n')
            ofx.write('NEWFILEUID:NONE\n')
            ofx.write('\n')
            ofx.write('<OFX>\n')
            ofx.write('<SIGNONMSGSRSV1>\n')
            ofx.write('<SONRS>\n')
            ofx.write('<STATUS>\n')
            ofx.write('<CODE>0</CODE>\n')
            ofx.write('<SEVERITY>INFO</SEVERITY>\n')
            ofx.write('</STATUS>\n')
            ofx.write('<DTSERVER>20230605\n')
            ofx.write('<LANGUAGE>POR\n')
            ofx.write('<DTACCTUP>20230605\n')
            ofx.write('<FI>\n')
            ofx.write('<ORG>Banco Do Brasil S/A\n')
            ofx.write('<FID>001\n')
            ofx.write('</FI>\n')
            ofx.write('</SONRS>\n')
            ofx.write('</SIGNONMSGSRSV1>\n')
            ofx.write('<BANKMSGSRSV1>\n')
            ofx.write('<STMTTRNRS>\n')
            ofx.write('<TRNUID>0\n')
            ofx.write('<STATUS>\n')
            ofx.write('<CODE>0\n')
            ofx.write('<SEVERITY>INFO\n')
            ofx.write('</STATUS>\n')
            ofx.write('<STMTRS>\n')
            ofx.write('<CURDEF>BRL\n')
            ofx.write('<BANKACCTFROM>\n')
            ofx.write('<BANKID>001\n')  # user`s input
            ofx.write('<ACCTID>7567-1\n')  # user`s  input
            ofx.write('<ACCTTYPE>CHECKING\n')
            ofx.write('</BANKACCTFROM>\n')
            ofx.write('<BANKTRANLIST>\n')
            ofx.write('<DTSTART>20230301\n')
            ofx.write('<DTEND>20230331\n')
            next(reader)
            next(reader)
            for row in reader:
                #if row[4] == '' and row[3] == '':
                 #   continue          
                ofx.write('<STMTTRN>\n')
                if row[15][0:1] == '-':
                    ofx.write('<TRNTYPE>DEBIT\n')
                else:
                    ofx.write('<TRNTYPE>DEP\n')
                ofx.write(f'<DTPOSTED>{row[3][6:10]}{row[3][3:5]}{row[3][0:2]}\n')
                ofx.write(f'<TRNAMT>{row[15]}\n')
                ofx.write(f'<FITID>{row[3][6:10]}{row[3][3:5]}{row[3][0:2]}{row[0]}\n')
                ofx.write(f'<CHECKNUM>{row[6]}\n')
                ofx.write(f'<MEMO>{row[11]}\n')
                ofx.write('</STMTTRN>\n')

            ofx.write('</BANKTRANLIST>\n')
            ofx.write('</STMTRS>\n')
            ofx.write('</STMTTRNRS>\n')
            ofx.write('</BANKMSGSRSV1>\n')
            ofx.write('</OFX>\n')
