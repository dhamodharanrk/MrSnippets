__author__ = 'dhamodharan.k'
from pymongo import MongoClient

MONGO_CLIENT_IP = 'xx.xx.xx.xxx:27017'
MONGO_CLIENT = MongoClient(MONGO_CLIENT_IP)

def get_mongo_client(database_name, collection_name):
    """
    :param database_name: database name in string
    :param collection_name: collection name in string
    :return: mongo cursor object
    """
    db = MONGO_CLIENT[database_name]
    db_result = db[collection_name]
    return db_result

def list_db():
    """
    :return:
    """
    db_list = MONGO_CLIENT.list_database_names()
    return db_list

def list_collections(db:str):
    """
    :param db: database name
    :return:
    """
    _db = MONGO_CLIENT[db]
    return _db.list_collection_names()

def get_summarize(db:str,collection:str):
    """

    :param db: database name
    :param collection: collection name
    :return: returns dict with total no of records in given collection
    """
    connection = get_mongo_client(db,collection)
    out_dict = {}
    out_dict['DatabaseName'] = db
    out_dict['CollectionName'] = collection
    out_dict['TotalRecords'] = connection.count_documents({})
    return out_dict

def get_sample(db:str,collection:str,query_by:str,value:str,limit:int=1):
    """
    :param db: db name
    :param collection: collection name
    :param query_by: key
    :param value: value
    :param limit: int value and defult is 1
    :return: returns list of values
    """
    connection = get_mongo_client(db,collection)
    if str(query_by).lower().__contains__('id'):
        record = [i for i in connection.find({query_by:int(value)},{'_id':0},limit=limit)]
    else:
        record = [i for i in connection.find({query_by: value}, {'_id': 0}, limit=limit)]
    return record

def update_record(connection:dict,query_by:str,query_by_value,data:dict):
    """

    :param connection: collection name
    :param query_by: key
    :param query_by_value: value
    :param data: dict records
    :return: None
    """
    assert ('db' and 'collection' in list(connection.keys())), 'Required attributes not found!'
    try:
        connection = get_mongo_client(connection['db'], connection['collection'])
        if connection.find_one({query_by: query_by_value}):
            connection.update_one({query_by: query_by_value},{'$set':data})
            return True
        else : return False
    except Exception as error: raise Exception(error)

def update_attribute(connection:dict,query_by:str,query_by_value,data:dict,attributes:list):
    """
    :param connection: connection object
    :param query_by: query by key
    :param query_by_value: value
    :param data: data dict
    :param attributes: list of multi valued variable's
    :return: None
    """
    connection = get_mongo_client(connection['db'], connection['collection'])
    exist_check = connection.find_one({query_by: query_by_value})
    if exist_check:
        _id = exist_check['_id']
        for update_key in attributes:
            old_value = exist_check.get(update_key,[])
            current_value = data.get(update_key,[])
            if type(old_value) == list and type(current_value) == list:
                new_without_Dup = set(old_value + current_value)
                connection.update_one({'_id': _id}, {'$set': {update_key: list(new_without_Dup)}})
    else: connection.insert_one(data)

def create_index(connection:dict,index_attributes:list,ascending:bool=True):
    """
    :param connection: connection object
    :param index_attributes: list of variable names
    :param ascending: bool value
    :return: None
    """
    assert ('db' and 'collection' in list(connection.keys())),'Required attributes not found!'
    try:
        connection = get_mongo_client(connection['db'],connection['collection'])
        index_dict = {i: 1 if ascending else -1 for i in index_attributes}
        connection.create_index(index_dict)
    except Exception as error:
        return error