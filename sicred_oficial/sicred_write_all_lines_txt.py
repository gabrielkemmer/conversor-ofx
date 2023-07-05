
def sicred_convert_txt_to_ofx(txt_file):
    with open(txt_file, 'r') as txtfile:
        lines = txtfile.readlines()

        for line in lines:
            row = line.strip().split(' ')
            print(row)
            
