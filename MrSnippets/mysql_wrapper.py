__author__ = 'dhamodharan.k'
import pymysql

def get_mysql_client(host_ip, username, pwd,db_name):
    connection = pymysql.connect(host=host_ip,user=username,
                                 db=db_name,
                                 password=pwd,
                                 autocommit=True,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8',
                                 max_allowed_packet=16*1024)
    return connection


def execute_mysql_query(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

conn = get_mysql_client('xx.xx.xx.xxx', 'root', 'password', 'profile')
query = 'select * from sample'
result_rows = execute_mysql_query(conn, query)