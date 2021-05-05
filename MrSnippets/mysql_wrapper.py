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


def _get_last_inserted(connection_obj):
    with connection_obj.cursor() as ms_cursor:
        ins_id_query = 'SELECT LAST_INSERT_ID();'
        ins_id = query_actions(connection_obj, ins_id_query, 'select')
    ms_cursor.close()
    return ins_id

def _get_affected_rows(connection_obj):
    with connection_obj.cursor() as ms_cursor:
        ins_id_query = 'SELECT ROW_COUNT();'
        ins_id = query_actions(connection_obj, ins_id_query, 'select')
    ms_cursor.close()
    return ins_id

def query_actions(connection_obj, query, query_type):
    result = None
    with connection_obj.cursor() as cursor:
        cursor.execute(query)
        if query_type == 'select':
            result = cursor.fetchall()
        if query_type == 'insert':
            result = _get_last_inserted(connection_obj)[0]['LAST_INSERT_ID()']
        if query_type == 'update':
            result = str(_get_affected_rows(connection_obj)[0]['ROW_COUNT()']) + 'row(s) affected '
    cursor.close()
    return result
