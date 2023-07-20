from flask import Flask, render_template, request, redirect, flash, send_file, session
import pandas as pd
import os
from Santander_oficial.santander_convert_pdf_to_csv import *
from Santander_oficial.santander_convert_csv_to_ofx import *
from Santander_oficial.santander_convert_xls_to_csv import *
from BB_oficial.bb_convert_pdf_to_csv import *
from BB_oficial.bb_convert_csv_to_ofx import *
from BB_oficial.bb_convert_xls_to_csv import *
from BB_oficial.bb_convert_txt_to_ofx import *
from Bradesco_oficial.bradesco_convert_pdf_to_csv import *
from Bradesco_oficial.bradesco_convert_csv_to_ofx import *
from Bradesco_oficial.bradesco_convert_txt_to_ofx import *
from Bradesco_oficial.bradesco_convert_xls_to_csv import *
from sicred_oficial.sicred_convert_csv_to_ofx import *
from sicred_oficial.sicred_convert_pdf_to_csv import*
from sicred_oficial.sicred_convert_txt_to_ofx import *
from sicred_oficial.sicred_convert_xls_to_csv import *
from sicred_oficial.sicred_write_all_lines_txt import *
from sicred_oficial.sicred_write_pdf import *
from cef_oficial.cef_convert_txt_to_ofx import *
from cora.cora_convert_csv_to_ofx import *
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

#host='146.190.145.32', port=5000

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Fn741953.741953'
    #app.config['SERVER_NAME'] = 'conversor.contabilitools.com.br'

    # MongoDB configuration
    client = MongoClient('mongodb+srv://gabrielkemmer:Araujo35@cluster0.yxrnwy9.mongodb.net/?retryWrites=true&w=majority')
    db = client['renato']
    users_collection = db['users']


    @app.route('/', methods=['GET', 'POST'])
    def index():
        if 'username' in session:
            return render_template("home.html")
        return redirect("/login")
        #return render_template('home.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = users_collection.find_one({'username': username})

            if user and check_password_hash(user['password'], password):
                session['username'] = username
                return redirect('/')
            else:
                return 'Invalid username or password'

        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            existing_user = users_collection.find_one({'username': username})

            if existing_user:
                return 'The username is already taken'

            hashed_password = generate_password_hash(password)

            new_user = {'username': username, 'password': hashed_password}
            users_collection.insert_one(new_user)

            session['username'] = username
            return redirect('/')

        return render_template('signup.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect('/')

    @app.route('/santander', methods=['GET', 'POST'])
    def santander():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'Santander_oficial')

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            ALLOWED_EXTENSIONS = set(['pdf', 'xlsx', 'csv'])

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()

                if file_extension == 'pdf':
                    filename = 'santander_pdf.pdf'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Santander_oficial/')
                    pdf_path = path3 + 'santander_pdf.pdf'  # Specify the path to your PDF file
                    output_csv_path = path3 + 'novo_pdf'  # Specify the path and prefix for the output CSV files
                    santander_convert_pdf_to_csv(pdf_path, output_csv_path)

                    csv_path = path3 + 'novo_pdf_1.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Santander_oficial/')

                    csv_folder = path  # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'santander_ofx.ofx'
                    santander_convert_csv_to_ofx(csv_folder, ofx_file)
                    return redirect('/download_ofx_santander')
                if file_extension == 'xlsx':
                    filename = 'santander_xls2.xlsx'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Santander_oficial/')
                    xls_path = path3 + 'santander_xls2.xlsx'  # Specify the path to your XLS file
                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path for the output CSV file
                    santander_convert_xls_to_csv(xls_path, csv_path)

                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Santander_oficial/')

                    csv_folder = path  # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'santander_ofx.ofx'
                    santander_convert_csv_to_ofx(csv_folder, ofx_file)

                    return redirect('/download_ofx_santander')
                if file_extension == 'csv':
                    filename = 'santander_xls2.xlsx'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Santander_oficial/')
                    csv_path = path3 + 'santander_csv.csv'  # Specify the path to your XLS file

                    csv_path = path3 + 'santander_csv.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Santander_oficial/')

                    csv_folder = path  # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'santander_ofx.ofx'
                    santander_convert_csv_to_ofx(csv_folder, ofx_file)
                    return redirect('/download_ofx_santander')
                else:
                    flash('Invalid file extension. Only PDF and XLSX files are allowed.')

        return render_template('santander.html')

    @app.route('/download_ofx_santander')
    def download_ofx_santander():
        actual_directory = os.getcwd()
        path = os.path.join(actual_directory, 'Santander_oficial/')
        ofx_file = path + 'santander_ofx.ofx'  # Specify the path to your OFX file
        
        try:
            for filename in os.listdir(path):
                if filename.startswith('novo_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('santander_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('csv_to_ofx'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('novo_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('santander_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)                       
            return send_file(ofx_file)
        finally:
            os.remove(ofx_file)

    @app.route('/bb', methods=['GET', 'POST'])
    def bb():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'BB_oficial')

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            ALLOWED_EXTENSIONS = set(['xlsx', 'csv', 'txt'])

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                """
                if file_extension == 'pdf':
                    filename = 'bb_pdf.pdf'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'BB_oficial/')
                    pdf_path = path3 + 'bb_pdf.pdf'  # Specify the path to your PDF file
                    output_csv_path = path3 + 'bb_novo_pdf.csv'  # Specify the path and prefix for the output CSV files
                    bb_convert_pdf_to_csv(pdf_path, output_csv_path)

                    csv_path = path3 + 'bb_novo_pdf.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'BB_oficial/')

                    csv_folder = path + 'bb_novo_pdf.csv' # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'bb_ofx'
                    bb_convert_csv_to_ofx(csv_folder, ofx_file)
                    return redirect('/download_ofx_bb')
                """
                if file_extension == 'xlsx':
                    filename = 'bb_xls.xlsx'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'BB_oficial/')
                    xls_path = path3 + 'bb_xls.xlsx'  # Specify the path to your XLS file
                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path for the output CSV file
                    bb_convert_xls_to_csv(xls_path, csv_path)

                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'BB_oficial/')

                    csv_folder = path + 'novo_xls_1.csv'  # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'bb_ofx'
                    bb_convert_csv_to_ofx(csv_folder, ofx_file)

                    return redirect('/download_ofx_bb')
                if file_extension == 'txt':
                    filename = 'bb_txt.txt'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'BB_oficial/')
                    txt_path = path3 + 'bb_txt.txt'  # Specify the path to your XLS file
                    
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'BB_oficial/')
                    ofx_file = path + 'bb_ofx'
                    bb_convert_txt_to_ofx(txt_path, ofx_file)
                    return redirect('/download_ofx_bb')
                if file_extension == 'csv':
                    filename = 'bb_csv.csv'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'BB_oficial/')
                    csv_path = path3 + 'bb_csv.csv'  # Specify the path for the output CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'BB_oficial/')

                    csv_file = path + 'bb_csv.csv'# Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'bb_ofx'
                    bb_convert_csv_to_ofx(csv_file, ofx_file)
                    return redirect('/download_ofx_bb')
                else:
                    flash('Invalid file extension. Only PDF and XLSX files are allowed.')

        return render_template('bb.html')

    @app.route('/download_ofx_bb')
    def download_ofx_bb():
        actual_directory = os.getcwd()
        path = os.path.join(actual_directory, 'BB_oficial/')
        ofx_file = path + 'bb_ofx'  # Specify the path to your OFX file
        
        try:
            for filename in os.listdir(path):
                if filename.startswith('bb_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('csv_to'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('novo_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('bb_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('bb_csv'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)           
            return send_file(ofx_file)    
        finally:
            os.remove(ofx_file)

    @app.route('/bradesco', methods=['GET', 'POST'])
    def bradesco():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'Bradesco_oficial')

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            ALLOWED_EXTENSIONS = set(['xlsx'])

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                """
                if file_extension == 'pdf':
                    filename = 'bradesco_pdf.pdf'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Bradesco_oficial/')
                    pdf_path = path3 + 'bradesco_pdf.pdf'  # Specify the path to your PDF file
                    output_csv_path = path3 + 'bradesco_novo_pdf.csv'  # Specify the path and prefix for the output CSV files
                    bradesco_convert_pdf_to_csv(pdf_path, output_csv_path)

                    csv_path = path3 + 'bradesco_novo_pdf.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    bradesco_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Bradesco_oficial/')

                    csv_folder = path + 'bradesco_novo_pdf.csv' # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'bradesco_ofx'
                    bradesco_convert_csv_to_ofx(csv_folder, ofx_file)
                    return redirect('/download_ofx_bradesco')
                    """
                if file_extension == 'xlsx':
                    filename = 'bradesco_xls.xlsx'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Bradesco_oficial/')
                    xls_path = path3 + 'bradesco_xls.xlsx'  # Specify the path to your XLS file
                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path for the output CSV file
                    bradesco_convert_xls_to_csv(xls_path, csv_path)

                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    bradesco_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Bradesco_oficial/')

                    csv_folder = path + 'novo_xls_1.csv'  # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'bradesco_ofx'
                    bradesco_convert_csv_to_ofx(csv_folder, ofx_file)

                    return redirect('/download_ofx_bradesco')
                """
                if file_extension == 'txt':
                    filename = 'bradesco_txt.txt'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Bradesco_oficial/')
                    txt_path = path3 + 'bradesco_txt.txt'  # Specify the path to your XLS file
                    
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Bradesco_oficial/')
                    ofx_file = path + 'bradesco_ofx'
                    bradesco_convert_txt_to_ofx(txt_path, ofx_file)
                    return redirect('/download_ofx_bradesco')
                """        
                """
                if file_extension == 'csv':
                    filename = 'bradesco_csv.csv'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'Bradesco_oficial/')
                    csv_path = path3 + 'bradesco_csv.csv'  # Specify the path for the output CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    bradesco_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'Bradesco_oficial/')

                    csv_file = path + 'bradesco_csv.csv'# Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'bradesco_ofx'
                    bradesco_convert_csv_to_ofx(csv_file, ofx_file)

                    return redirect('/download_ofx_bradesco')
                    """
            else:
                flash('Invalid file extension. Only PDF and XLSX files are allowed.')

        return render_template('bradesco.html')

    @app.route('/download_ofx_bradesco')
    def download_ofx_bradesco():
        actual_directory = os.getcwd()
        path = os.path.join(actual_directory, 'Bradesco_oficial/')
        ofx_file = path + 'bradesco_ofx'  # Specify the path to your OFX file
        try:
            for filename in os.listdir(path):
                if filename.startswith('bradesco_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('novo_'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)                
            for filename in os.listdir(path):
                if filename.startswith('csv_to'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('bradesco_novo'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('bradesco_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('bradesco_csv'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)           
            return send_file(ofx_file)    
        finally:
            os.remove(ofx_file)

    @app.route('/cef', methods=['GET', 'POST'])
    def cef():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'cef_oficial')

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            ALLOWED_EXTENSIONS = set(['pdf', 'xlsx', 'csv', 'txt'])

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()

                if file_extension == 'txt':
                    filename = 'cef_txt.txt'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'cef_oficial/')
                    txt_file = path3 + 'cef_txt.txt'  

                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'cef_oficial/')
                    ofx_file = path + 'cef_ofx'
                    cef_convert_txt_to_ofx(txt_file, ofx_file)
                    return redirect('/download_ofx_cef')
                else:
                    flash('Invalid file extension. Only PDF and XLSX files are allowed.')

        return render_template('cef.html')

    @app.route('/download_ofx_cef')
    def download_ofx_cef():
        actual_directory = os.getcwd()
        path = os.path.join(actual_directory, 'cef_oficial/')
        ofx_file = path + 'cef_ofx' # Specify the path to your OFX file
        try:
            for filename in os.listdir(path):
                if filename.startswith('cef_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('text_'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)                
            for filename in os.listdir(path):
                if filename.startswith('cef_txt'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('cef_novo'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('cef_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('cef_csv'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)           
            return send_file(ofx_file)    
        finally:
            os.remove(ofx_file)

    @app.route('/sicred', methods=['GET', 'POST'])
    def sicred():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'sicred_oficial')

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            ALLOWED_EXTENSIONS = set(['pdf', 'xlsx', 'csv', 'txt'])

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()

                if file_extension == 'pdf':
                    filename = 'sicred_pdf.pdf'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'sicred_oficial/')
                    pdf_path = path3 + 'sicred_pdf.pdf'  # Specify the path to your PDF file
                    output_csv_path = path3 + 'sicred_novo_pdf.csv'  # Specify the path and prefix for the output CSV files
                    sicred_convert_pdf_to_csv(pdf_path, output_csv_path)

                    csv_path = path3 + 'sicred_novo_pdf.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    #santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'sicred_oficial/')

                    csv_folder = path + 'sicred_novo_pdf.csv' # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'sicred_ofx'
                    sicred_convert_csv_to_ofx(csv_folder, ofx_file)
                    return redirect('/download_ofx_sicred')
                if file_extension == 'xlsx':
                    filename = 'sicred_xls.xlsx'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'sicred_oficial/')
                    xls_path = path3 + 'sicred_xls.xlsx'  # Specify the path to your XLS file
                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path for the output CSV file
                    sicred_convert_xls_to_csv(xls_path, csv_path)

                    csv_path = path3 + 'novo_xls_1.csv'  # Specify the path to your CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    santander_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'sicred_oficial/')

                    csv_folder = path + 'novo_xls_1.csv'  # Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'sicred_ofx'
                    sicred_convert_csv_to_ofx(csv_folder, ofx_file)

                    return redirect('/download_ofx_sicred')
                if file_extension == 'txt':
                    filename = 'sicred_txt.txt'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'sicred_oficial/')
                    txt_path = path3 + 'sicred_txt.txt'  # Specify the path to your XLS file
                    
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'sicred_oficial/')
                    ofx_file = path + 'sicred_ofx'
                    sicred_convert_txt_to_ofx2(txt_path, ofx_file)
                    return redirect('/download_ofx_sicred')
                if file_extension == 'csv':
                    filename = 'sicred_csv.csv'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'sicred_oficial/')
                    csv_path = path3 + 'sicred_csv.csv'  # Specify the path for the output CSV file
                    columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    #sicred_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'sicred_oficial/')

                    csv_file = path + 'sicred_csv.csv'# Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'sicred_ofx'
                    sicred_convert_csv_to_ofx(csv_file, ofx_file)

                    return redirect('/download_ofx_sicred')
                else:
                    flash('Invalid file extension. Only PDF and XLSX files are allowed.')

        return render_template('sicred.html')

    @app.route('/download_ofx_sicred')
    def download_ofx_sicred():
        actual_directory = os.getcwd()
        path = os.path.join(actual_directory, 'sicred_oficial/')
        ofx_file = path + 'sicred_ofx' # Specify the path to your OFX file
        try:
            for filename in os.listdir(path):
                if filename.startswith('sicred_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('novo'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)                
            for filename in os.listdir(path):
                if filename.startswith('sicred_txt'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('sicred_novo'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('sicred_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('sicred_csv'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)           
            return send_file(ofx_file)    
        finally:
            os.remove(ofx_file)
            pass


    @app.route('/cora', methods=['GET', 'POST'])
    def cora():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'cora')

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']

            ALLOWED_EXTENSIONS = set([ 'csv'])

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()

                if file_extension == 'csv':
                    filename = 'cora_csv.csv'  # Replace with your desired filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')

                    actual_directory = os.getcwd()
                    path3 = os.path.join(actual_directory, 'cora/')
                    csv_path = path3 + 'cora_csv.csv'  # Specify the path for the output CSV file
                    #columns = ['Data', 'Descricao', 'Docto', 'Credito', 'Debito', 'Saldo']  # List of column names
                    #cora_append_columns_to_csv(csv_path, columns)

                    # Convert to OFX
                    actual_directory = os.getcwd()
                    path = os.path.join(actual_directory, 'cora/')

                    csv_file = path + 'cora_csv.csv'# Replace with the path to the folder containing the CSV files
                    ofx_file = path + 'cora_ofx'
                    cora_convert_csv_to_ofx(csv_file, ofx_file)

                    return redirect('/download_ofx_cora')
                else:
                    flash('Invalid file extension. Only PDF and XLSX files are allowed.')

        return render_template('cora.html')

    @app.route('/download_ofx_cora')
    def download_ofx_cora():
        actual_directory = os.getcwd()
        path = os.path.join(actual_directory, 'cora/')
        ofx_file = path + 'cora_ofx' # Specify the path to your OFX file
        try:
            for filename in os.listdir(path):
                if filename.startswith('cora_pdf'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('novo'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)                
            for filename in os.listdir(path):
                if filename.startswith('cora_txt'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('cora_novo'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)        
            for filename in os.listdir(path):
                if filename.startswith('cora_xls'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            for filename in os.listdir(path):
                if filename.startswith('cora_csv'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)           
            return send_file(ofx_file)    
        finally:
            os.remove(ofx_file)
            pass    

    return app

app = create_app()
