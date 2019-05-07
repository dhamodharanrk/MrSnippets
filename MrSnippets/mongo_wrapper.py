__author__ = 'dhamodharan.k'
from pymongo import MongoClient

MONGO_CLIENT_IP = 'xx.xx.xx.xxx:27017'
MONGO_CLIENT = MongoClient(MONGO_CLIENT_IP)

def get_mongo_client(database_name, collection_name):
    db = MONGO_CLIENT[database_name]
    db_result = db[collection_name]
    return db_result

def list_database():
    db_list = MONGO_CLIENT.list_database_names()
    return db_list

def list_collection(db:str):
    _db = MONGO_CLIENT[db]
    return _db.list_collection_names()

def get_collection_summary(db:str,collection:str):
    connection = get_mongo_client(db,collection)
    out_dict = {}
    out_dict['DatabaseName'] = db
    out_dict['CollectionName'] = collection
    out_dict['TotalRecords'] = connection.count_documents({})
    return out_dict

def get_sample_records(db:str,collection:str,query_by:str,value:str,limit:int=1):
    connection = get_mongo_client(db,collection)
    if str(query_by).lower().__contains__('id'):
        record = [i for i in connection.find({query_by:int(value)},{'_id':0},limit=limit)]
    else:
        record = [i for i in connection.find({query_by: value}, {'_id': 0}, limit=limit)]
    return record

def update_record(connection:dict,query_by:str,query_by_value,data:dict):
    if 'db' and 'collection' in connection:
        connection = get_mongo_client(connection['db'],connection['collection'])
        try:
            if connection.find_one({query_by: query_by_value}):
                connection.update_one({query_by: query_by_value},{'$set':data})
                return True
            else : return False
        except Exception as error:
            return error
    else:
        assert connection