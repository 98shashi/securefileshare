import mysql.connector
import os

ENDPOINT = "securep.c7x8rgc7mug5.us-east-2.rds.amazonaws.com"
PORT = "3306"
USER = "admin"
REGION = "us-east-2"
DBNAME = "securedb"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'


token = "Shashi123"

try:
    conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))


