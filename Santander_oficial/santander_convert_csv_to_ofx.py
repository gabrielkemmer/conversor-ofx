import csv
import os

def santander_convert_csv_to_ofx(csv_folder, ofx_file):
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
        ofx.write('<BANKMSGSRSV1>\n')
        ofx.write('<STMTTRNRS>\n')
        ofx.write('<STMTRS>\n')
        ofx.write('<BANKTRANLIST>\n')

        for file in os.listdir(csv_folder):
            if file.endswith('.csv'):
                csv_file = os.path.join(csv_folder, file)
                with open(csv_file, newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

                    for row in reader:
                        ofx.write('<STMTTRN>\n')
                        ofx.write(f'<TRNTYPE>{row[3]}<TRNTYPE>\n')
                        ofx.write(f'<DTPOSTED>{row[0]}</DTPOSTED>\n')
                        ofx.write(f'<TRNAMT>{row[1]}</TRNAMT>\n')
                        ofx.write(f'<FITID>{000000}</FITID>\n')
                        ofx.write(f'<CHECKNUM>{000000}</CHECKNUM>\n')
                        ofx.write(f'<PAYEEID>{0}</PAYEEID>\n')
                        ofx.write(f'<MEMO>{row[4]}<MEMO>\n')
                        ofx.write('</STMTTRN>\n')

        ofx.write('</BANKTRANLIST>\n')
        ofx.write('</STMTRS>\n')
        ofx.write('</STMTTRNRS>\n')
        ofx.write('</BANKMSGSRSV1>\n')
        ofx.write('</OFX>\n')

actual_directory = os.getcwd()
path = os.path.join(actual_directory, 'Santander_oficial/')

csv_folder = path # Replace with the path to the folder containing the CSV files
ofx_file = path + 'csv_to_ofx_output.ofx'
santander_convert_csv_to_ofx(csv_folder, ofx_file)
