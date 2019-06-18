__author__ = 'dhamodharan.k'
import pyodbc
from collections import OrderedDict
import warnings


def get_sql_client(server_ip,database,userName,pwd):
    '''db_object = get_sql_client('195.16.40.82', 'SampleDB', 'root', 'password')'''
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server_ip+';DATABASE='+database+';UID='+userName+';PWD='+pwd)
    cursor = cnxn.cursor()
    return cursor

def query_actions(db_object, query, query_type):
    query = query.replace("'NULL'",'NULL')
    if query_type == 'insert' or query_type == 'update':
        db_object.execute(query)
        db_object.commit()
    if query_type == 'select':
        db_object.execute(query)
        rows = db_object.fetchall()
        return rows

def insert_records(connection_obj, table_data:dict, data_dict: dict, unique_columns:list):
    db = table_data.get('db_name')
    table_name = table_data.get('table_name')
    query = "select column_name FROM "+str(db)+".INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'" + table_name + "'"
    rows = query_actions(connection_obj, query, 'select')
    rows = [i[0] for i in rows][1:]
    final_dict = OrderedDict({i: (str(data_dict[i]).replace("'",'"')if i in list(data_dict.keys()) else 'NULL') for i in rows})
    values = list(final_dict.values())
    column = list(final_dict.keys())
    if len(unique_columns) != 0:
        unique_columns = [i + "='" + final_dict[i] + "'" for i in unique_columns]
        unique_columns = ' AND '.join(unique_columns) if len(unique_columns) > 1 else unique_columns[0]
        data_check = "select * from " + table_name + " where " + unique_columns
        data_exists = query_actions(connection_obj, data_check, 'select')
    else: data_exists = []
    if len(data_exists) == 0:
        insert_query = "INSERT INTO " + table_name + " (" + ", ".join(column) + ") VALUES ('" + "', '".join( values) + "')"
        query_actions(connection_obj, insert_query, 'insert')
        scope_id_query = 'SELECT SCOPE_IDENTITY()'
        scope_id_query_result = query_actions(connection_obj, scope_id_query, 'select')
        scope_id = scope_id_query_result[0][0]
    else:
        warnings.warn('Data already Exist in given table')
        scope_id = data_exists[0][0]
    return scope_id


