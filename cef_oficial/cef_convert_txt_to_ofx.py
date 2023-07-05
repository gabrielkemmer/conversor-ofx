import os

def cef_convert_txt_to_ofx(txt_file, ofx_file):
    with open(txt_file, 'r') as txtfile:
        lines = txtfile.readlines()

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
            ofx.write('<LANGUAGE>POR</LANGUAGE>\n')
            ofx.write('</SONRS>\n')
            ofx.write('</SIGNONMSGSRSV1>\n')
            ofx.write('<BANKMSGSRSV1>\n')
            ofx.write('<STMTTRNRS>\n')
            ofx.write('<STMTRS>\n')
            ofx.write('<CURDEF>BRL</CURDEF>\n')
            ofx.write('<BANKACCTFROM>\n')
            ofx.write('<BANKID>0104</BANKID>\n')
            for line in lines:
                row = line.strip().split(';')
            ofx.write(f'<ACCTID>{row[0][1:17]}</ACCTID>\n')
            ofx.write('<ACCTTYPE>CHECKING</ACCTTYPE>\n')
            ofx.write('</BANKACCTFROM>\n')
            ofx.write('<BANKTRANLIST>\n')

            for line in lines:
                row = line.strip().split(';')

                ofx.write('<STMTTRN>\n')
                ofx.write(f'<TRNTYPE>{row[5][1:-1]}</TRNTYPE>\n')
                ofx.write(f'<DTPOSTED>{row[1][1:-1]}[-3:BRT]</DTPOSTED>\n')
                ofx.write(f'<TRNAMT>{row[4][1:-1]}</TRNAMT>\n')
                ofx.write(f'<FITID>{row[2][1:-1]}</FITID>\n')
                ofx.write(f'<CHECKNUM>{row[2][1:-1]}</CHECKNUM>\n')
                ofx.write(f'<MEMO>{row[3][1:-1]}</MEMO>\n')
                ofx.write('</STMTTRN>\n')

            ofx.write('</BANKTRANLIST>\n')
            ofx.write('</STMTRS>\n')
            ofx.write('</STMTTRNRS>\n')
            ofx.write('</BANKMSGSRSV1>\n')
            ofx.write('</OFX>\n')
