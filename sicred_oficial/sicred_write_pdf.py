import tabula

def sicred_write_pdf():
    pdf_path = '~/Sicred/sicred.pdf' 
    output_path = '~/Sicred/output.csv'
    tables = tabula.read_pdf(pdf_path, pages='all', options="--columns 1.1,2.2,3.3") # can be 10.1, 20.1, 30,1 too
    #tabula.convert_into(pdf_path, output_path, output_format="csv", options="--columns 1.1,2.2,3.3", pages='all')


