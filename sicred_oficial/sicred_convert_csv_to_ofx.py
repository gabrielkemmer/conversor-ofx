import csv

def sicred_convert_csv_to_ofx(csv_file, ofx_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    
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
            ofx.write('<LANGUAGE>ENG</LANGUAGE>\n')
            ofx.write('<FI>\n')
            ofx.write('<ORG>CCPI VANGUARDA PR/SP/RJ       </ORG>\n')
            ofx.write('<FID>CCPI VANGUARDA PR/SP/RJ       </FID>\n')
            ofx.write('</FI>\n')
            ofx.write('</SONRS>\n')
            ofx.write('</SIGNONMSGSRSV1>\n')
            ofx.write('<BANKMSGSRSV1>\n')
            ofx.write('<STMTTRNRS>\n')
            ofx.write('<TRNUID>1</TRNUID>\n')
            ofx.write('<STATUS>\n')
            ofx.write('<CODE>0</CODE>\n')
            ofx.write('<SEVERITY>INFO</SEVERITY>\n')
            ofx.write('</STATUS>\n')
            ofx.write('<STMTRS>\n')
            ofx.write('<CURDEF>BRL</CURDEF>\n')
            ofx.write('<BANKACCTFROM>\n')
            ofx.write('<BANKID>748</BANKID>\n')#user`s input
            ofx.write('<ACCTID>7100000000950043</ACCTID>\n')#user`s  input
            ofx.write('<ACCTTYPE>CHECKING</ACCTTYPE>\n')
            ofx.write('</BANKACCTFROM>\n')
            ofx.write('<BANKTRANLIST>\n')

            next(reader)  
            next(reader)  
            for row in reader:          
                ofx.write('<STMTTRN>\n')
                if row[3][1:2] == '-':
                    ofx.write('<TRNTYPE>DEBIT<TRNTYPE>\n')
                else:
                    ofx.write('<TRNTYPE>CREDIT<TRNTYPE>\n')
                ofx.write(f'<DTPOSTED>{row[0]}</DTPOSTED>\n')
                ofx.write(f'<TRNAMT>{row[3][1:] + "," + row[4][:-1]}</TRNAMT>\n')
                ofx.write(f'<FITID>{row[2]}</FITID>\n')
                ofx.write(f'<REFNUM>{row[2]}</REFNUM>\n')
                ofx.write(f'<MEMO>{row[1]}<MEMO>\n')
                ofx.write('</STMTTRN>\n')
                
            ofx.write('</BANKTRANLIST>\n')
            ofx.write('</STMTRS>\n')
            ofx.write('</STMTTRNRS>\n')
            ofx.write('</BANKMSGSRSV1>\n')
            ofx.write('</OFX>\n')
