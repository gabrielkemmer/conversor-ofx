import csv

def bradesco_convert_csv_to_ofx(csv_file, ofx_file):
    with open(csv_file, 'r', newline='', encoding='latin-1') as csvfile:
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
            ofx.write('<CODE>0\n')
            ofx.write('<SEVERITY>INFO</SEVERITY>\n')
            ofx.write('</STATUS>\n')
            ofx.write('<LANGUAGE>POR\n')
            ofx.write('</SONRS>\n')
            ofx.write('</SIGNONMSGSRSV1>\n')
            ofx.write('<BANKMSGSRSV1>\n')
            ofx.write('<STMTTRNRS>\n')
            ofx.write('<TRNUID>1001\n')
            ofx.write('<STATUS>\n')
            ofx.write('<CODE>0\n')
            ofx.write('<SEVERITY>INFO\n')
            ofx.write('</STATUS>\n')
            ofx.write('<STMTRS>\n')
            ofx.write('<CURDEF>BRL\n')
            ofx.write('<BANKACCTFROM>\n')
            ofx.write('<BANKID>0237</BANKID>\n')  # user`s input
            ofx.write('<ACCTID>3590/14902</ACCTID>\n')  # user`s  input
            ofx.write('<ACCTTYPE>CHECKING\n')
            ofx.write('</BANKACCTFROM>\n')
            ofx.write('<BANKTRANLIST>\n')
            next(reader)
            next(reader)
            for row in reader:
                if row[4] == '' and row[3] == '':
                    continue          
                ofx.write('<STMTTRN>\n')
                if row[4][0:1] == '-':
                    ofx.write('<TRNTYPE>DEBIT\n')
                else:
                    ofx.write('<TRNTYPE>CREDIT\n')
                ofx.write(f'<DTPOSTED>{row[0]}</DTPOSTED>\n')
                if row[4][0:1] == '-':
                    ofx.write(f'<TRNAMT>{row[4]}</TRNAMT>\n')
                else:
                    ofx.write(f'<TRNAMT>{row[3]}</TRNAMT>\n')
                ofx.write(f'<FITID>{row[1]}</FITID>\n')
                ofx.write(f'<MEMO>{row[1]}<MEMO>\n')
                ofx.write('</STMTTRN>\n')

            ofx.write('</BANKTRANLIST>\n')
            ofx.write('</STMTRS>\n')
            ofx.write('</STMTTRNRS>\n')
            ofx.write('</BANKMSGSRSV1>\n')
            ofx.write('</OFX>\n')


