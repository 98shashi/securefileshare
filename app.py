import json
import os
from asyncio import sleep
from datetime import datetime

import mysql.connector
from flask import Flask, flash, request, redirect, url_for, session, render_template, send_from_directory
import boto3
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet



app = Flask(__name__)
# UPLOAD_FOLDER = 'C:/uploads'
# DOWNLOAD_FOLDER = 'C:/downloads'
UPLOAD_FOLDER = '/home/ubuntu/uploads'
DOWNLOAD_FOLDER = '/var/www/html/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 80000000
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','mp4'}

app.secret_key = 'this is your secret key'

bcrypt = Bcrypt(app)
ENDPOINT = "securep.c7x8rgc7mug5.us-east-2.rds.amazonaws.com"
PORT = "3306"
USER = "admin"
REGION = "us-east-2"
DBNAME = "securedb"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
token = "Shashi123"

conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']

        cursor = conn.cursor()

        pw_hash = bcrypt.generate_password_hash(password1)
        if re.search('(select|update|delete|drop .+)', username.lower()):
            msg = "invalid chars found, please try again with valid input"
            return render_template('login.html', msg=msg)
        elif re.search('(select|update|delete|drop .+)', password1.lower()):
            msg = "invalid chars found, please try again with valid input"
            return render_template('login.html', msg=msg)
        elif len(username)>16:
            msg =  "length of username is greater than 16 chars please enter required length"
            return render_template('login.html', msg=msg)
        elif len(password1)>16:
            msg = "length of password is greater than 16 chars please enter required length"
            return render_template('login.html', msg=msg)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}' ".format(username))
        account_exist = cursor.fetchone()
        if account_exist == None:
            msg = 'user does not exists'
            return render_template('login.html', msg=msg)
        else:

            cursor.execute("SELECT password FROM users WHERE username = '{}' ".format(username))
            user_account = cursor.fetchone()
            cursor.execute("SELECT * FROM users WHERE username = '{}' ".format(username))
            account = cursor.fetchone()
            cursor.close()
            print(account)


            flag = bcrypt.check_password_hash(user_account[0],password1)
            if flag:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[2]
            # return render_template('index.html')
                return redirect(url_for('group',user_data=username))
            else:
                msg = 'wrong password'
                return render_template('login.html', msg = msg)
    return render_template('login.html',msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        password_has = bcrypt.generate_password_hash(password)

        if re.search('(select|update|delete|drop .+)',name.lower()):
            msg = "invalid chars found, please try again with valid input"
            return render_template('register.html', msg=msg)
        elif re.search('(select|update|delete|drop .+)',username.lower()):
            msg = "invalid chars found, please try again with valid input"
            return render_template('register.html', msg=msg)
        elif re.search('(select|update|delete|drop .+)', password.lower()):
            msg = "invalid chars found, please try again with valid input"
            return render_template('register.html', msg=msg)
        elif len(name)>81:
            msg=  "length of name is greater than 80 chars please enter required length"
            return render_template('register.html', msg=msg)
        elif len(username)>16:
            msg=  "length of username is greater than 16 chars please enter required length"
            return render_template('register.html', msg=msg)
        elif len(password)>16:
            msg=  "length of password is greater than 16 chars please enter required length"
            return render_template('register.html', msg=msg)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}' ".format(username))
        account_exist = cursor.fetchone()
        if len(account_exist)>0:
            msg= 'user already exists'
            return render_template('login.html',msg =msg)
        else:

            cursor.execute(''' INSERT INTO users(name,username,password) VALUES(%s,%s,%s)''', (name,username,password_has))
            conn.commit()
            cursor.close()
            return render_template('login.html')
    return render_template('register.html')

@app.route('/create_group',methods=['GET', 'POST'])
def create_group():
    if session['loggedin'] == True:
        if request.method == 'POST':
            msg= ''
            group_name = request.form['groupname']
            owner_id = session['id']
            if re.search('(select|update|delete|drop .+)', group_name.lower()):
                msg = "invalid chars found, please try again with valid input"
                return render_template('group_creation.html', msg=msg)
                '''print("INSERT INTO securedb.groups(groupname,ownerid) VALUES('{}',{})".format(group_name,owner_id))'''
            elif len(group_name)>16:
                msg = "length of groupname is greater than 16 chars please enter required length"
                return render_template('group_creation.html', msg=msg)
            else:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM securedb.groups WHERE groupname = '{}' ".format(group_name))
                account_exist = cursor.fetchone()
                if len(account_exist) > 0:
                    msg = 'group already exists'
                    return render_template('group_creation.html', msg=msg)
                else:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO securedb.groups(groupname,ownerid) VALUES('{}',{})".format(group_name,owner_id))
                    conn.commit()
                    cursor.close()
                    return redirect(url_for('group',user_data=session['username']))
        return render_template('group_creation.html')
    else :
        msg = 'Error loading page'
        return render_template('login.html', msg=msg)




@app.route('/group/<user_data>', methods=['GET', 'POST'])
def group(user_data):
    msg = ''
    if session['loggedin']:
        username = user_data
        conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
        cursor1 = conn.cursor()
        cursor1.execute("select u.name,g.*,m.* from securedb.users as u, securedb.groups as g,  "
                        "securedb.mapping as m where g.gid=m.gid and "
                        "u.uid=m.uid and m.IsActive=0 and g.ownerid={}".format(session['id']))
        approval_users = cursor1.fetchall()
        cursor1.execute("select * from securedb.groups ")
        groups = cursor1.fetchall()
        cursor1.close()
        return render_template('groups.html',groups=groups, approval_users=approval_users)
    else:
        msg = 'Error loading page'
        return render_template('login.html',msg=msg)


@app.route('/approve/<mapid>', methods=['GET', 'POST'])
def approve(mapid):
    if session['loggedin']:
        conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
        cursor = conn.cursor()
        cursor.execute("select * from securedb.groups as g,  securedb.mapping as m "
                       "where g.gid=m.gid and m.mapid={} and g.ownerid={}".format(mapid, session['id']))
        mapping = cursor.fetchall()
        print("MAPPING")
        print(mapping)
        if(len(mapping)>0):
            cursor.execute(
            "update securedb.mapping set IsActive=1 where mapid={}".format(mapid))
            conn.commit()
        cursor.close()
        return redirect(url_for('group',user_data=session['username']))

@app.route('/upload/<groupid>', methods=['GET', 'POST'])
def upload(groupid):
    if session['loggedin']:
        conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
        cursor1 = conn.cursor()
        cursor1.execute("select * from securedb.files where gid = {}".format(groupid))
        files = []
        files = cursor1.fetchall()
        conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
        cursor2 = conn.cursor()
        cursor2.execute("select * from securedb.mapping where IsActive=1 and uid = {} and  gid = {} ".format(session['id'],groupid))

        users = cursor2.fetchall()
        print('USERS')
        print(users)
        if len(users) > 0:
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
                                  aws_access_key_id="AKIAXZTDUHOENARZFNNC",
                                  aws_secret_access_key="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")
                    bucket_name = "98shashi1"
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


                    res = db_operations(filename, bucket_name, groupid,key)
                    response = s3.upload_file(fullpath, bucket_name, filename)
                    print(response)
                    return render_template('file_upload.html', files = files)
            return render_template('file_upload.html', files = files)
        else:
            cursor = conn.cursor()
            cursor.execute(
                "select * from securedb.mapping where IsActive=0 and uid = {} and  gid = {} ".format(session['id'],
                                                                                                     groupid))
            users = cursor.fetchall()
            if(len(users)>0):
                msg= 'Please wait for admin to authorize your request to join group'
                return render_template('groups.html', msg=msg)
            else:
                cursor = conn.cursor()
                cursor.execute(
                    "insert into securedb.mapping(IsActive, uid, gid) values (0, {}, {})".format(session['id'],
                                                                                                         groupid))
                conn.commit()

                msg = ' You are not part of this group please be added to group'
                return render_template('groups.html', msg=msg)
    else:
        pass


import requests
import re
import json
@app.route('/filedownload', methods=['GET', 'POST'])
def filedownload():
    if session['loggedin']:
        if request.method == 'POST':
            url = request.data.decode("utf-8")
            url = json.loads(url)["url"]
        r = requests.get(url)

        ENDPOINT = "securep.c7x8rgc7mug5.us-east-2.rds.amazonaws.com"
        PORT = "3306"
        USER = "admin"
        DBNAME = ""
        os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

        token = "Shashi123"

        try:
            conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
            cur = conn.cursor()
            cur.execute("select `keys` from securedb.files where fileurl='{}'".format(url))
            query_results = cur.fetchone()
        except Exception as e:
            print("Database connection failed due to {}".format(e))

        with open('keyfile.key', 'rb') as keyfile:
            key = keyfile.read()
        fernet = Fernet(query_results[0].encode('utf-8'))
        r = requests.get(url)
        decrypted = fernet.decrypt(r.content)
        filename = re.search('https:(.*)\/(.*\..*)$', url)
        filename = filename.group(2)
        fullpath = os.path.join(DOWNLOAD_FOLDER, filename)
        with open(fullpath, 'wb') as f:
            f.write(decrypted)
        return fullpath
    else:
        msg='Filedownload error'
        return render_template('groups.html', msg=msg)
    # return render_template('download.html', fullpath=fullpath, username=session['username'])

@app.route('/filedownload/<filename>', methods=['GET', 'POST'])
def filedownload_link(filename):
    fullpath = os.path.join(DOWNLOAD_FOLDER)
    sleep(5)
    return send_from_directory(directory=fullpath, path=filename, as_attachment=True)
    # return render_template('download.html', fullpath=fullpath, username=session['username'])
def db_operations(filename, bucket_name, groupid,key):
    ENDPOINT = "securep.c7x8rgc7mug5.us-east-2.rds.amazonaws.com"
    PORT = "3306"
    USER = "admin"
    REGION = "us-east-2"
    DBNAME = "securedb"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    token = "Shashi123"

    file_url = "https://{}.s3.amazonaws.com/{}".format(bucket_name, filename)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur = conn.cursor()
        key = key.decode("utf-8")
        # print("INSERT INTO `securedb`.`files` (`file_name`,`fileurl`, `timestamp`, `gid`,'key') "
        #            "VALUES ('{}', '{}', '{}', '{}','{}')".format(filename, file_url, date_time, groupid,key))
        cur.execute("INSERT INTO `securedb`.`files` (`file_name`,`fileurl`, `timestamp`, `gid`,`keys`) "
                   "VALUES ('{}', '{}', '{}', '{}','{}')".format(filename, file_url, date_time, groupid, key))
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
    app.run(host="0.0.0.0", port=80)