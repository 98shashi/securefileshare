import os
from datetime import datetime
import mysql.connector
from flask import Flask, flash, request, redirect, url_for, session, render_template
import boto3
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet



app = Flask(__name__)
UPLOAD_FOLDER = 'C:/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bcrypt = Bcrypt(app)

ENDPOINT = "securep.c4etuyab1xx9.us-east-2.rds.amazonaws.com"
PORT = "3306"
USER = "admin"
REGION = "us-east-2"
DBNAME = "securedb"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
token = "Shashi123"

conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME,
                                   ssl_ca='SSLCERTIFICATE')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']

        cursor = conn.cursor()

        pw_hash = bcrypt.generate_password_hash(password1)
        cursor.execute("SELECT password FROM users WHERE username = '{}' ".format(username))
        user_account = cursor.fetchone()  #

        flag = bcrypt.check_password_hash(user_account[0],password1)
        if flag:
            # return render_template('index.html')
            return redirect(url_for('group',user_data=username))
        else:
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        password_has = bcrypt.generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO users(name,username,password) VALUES(%s,%s,%s)''', (name,username,password_has))
        conn.commit()
        cursor.close()
        return render_template('login.html')
    return render_template('register.html')


@app.route('/group/<user_data>', methods=['GET', 'POST'])
def group(user_data):
    username = user_data
    cursor1 = conn.cursor()
    cursor1.execute("SELECT uid FROM users WHERE username = '{}' ".format(username))
    user_id = cursor1.fetchone()
    cursor1.execute("select * from securedb.groups where gid in(select gid from securedb.mapping where uid = 10)")
    groups = cursor1.fetchall()
    return render_template('groups.html',groups=groups)




@app.route('/upload/<groupid>', methods=['GET', 'POST'])
def upload(groupid):
        cursor1 = conn.cursor()
        cursor1.execute("select * from securedb.files where gid = {}".format(groupid))
        files = []
        files = cursor1.fetchall()
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                s3 = boto3.client("s3",
                                  aws_access_key_id="AKIA2EX5QPCJJRJUSG24",
                                  aws_secret_access_key="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")
                bucket_name = "98shashi"
                fullpath = os.path.join(UPLOAD_FOLDER, filename)
                key = Fernet.generate_key()
                with open('keyfile.key', 'wb') as keyfile:
                    keyfile.write(key)

                with open('keyfile.key', 'rb') as keyfile:
                    key = keyfile.read()

                fernet = Fernet(key)
                with open(fullpath, 'rb') as file:
                    original = file.read()

                encrypted = fernet.encrypt(original)


                with open(fullpath, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)


                res = db_opeartions(filename, bucket_name, groupid,key)
                response = s3.upload_file(fullpath, bucket_name, filename)
                print(response)
                return render_template('file_upload.html', files = files)
        return render_template('file_upload.html', files = files)

def db_opeartions(filename, bucket_name, groupid,key):
    ENDPOINT = "securep.c4etuyab1xx9.us-east-2.rds.amazonaws.com"
    PORT = "3306"
    USER = "admin"
    REGION = "us-east-2"
    DBNAME = "securep"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    token = "Shashi123"

    file_url = "https://{}.s3.amazonaws.com/{}".format(bucket_name, filename)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur = conn.cursor()
        print("INSERT INTO `securedb`.`files` (`file_name`,`fileurl`, `timestamp`, `gid`) "
                   "VALUES ('{}', '{}', '{}', {})".format(filename, file_url, date_time, groupid))
        cur.execute("INSERT INTO `securedb`.`files` (`file_name`,`fileurl`, `timestamp`, `gid`) "
                    "VALUES ('{}', '{}', '{}', {})".format(filename, file_url, date_time, groupid))
        conn.commit()
        cur.execute("SELECT fid FROM `securedb`.`files` where file_name='{}' "
                    "and fileurl='{}' and timestamp='{}'".format(filename,file_url, date_time))
        fileinfo = cur.fetchone()
        print(fileinfo)
        if fileinfo:
            conn.commit()
        return "File uploaded successfully"
    except Exception as e:
        print(e)
        return "Database connection failed"

if __name__=='__main__':
    app.run(debug=True)