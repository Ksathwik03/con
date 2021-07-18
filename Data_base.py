import pymongo

db = []


def data_base():
    global db
    db = pymongo.MongoClient(
        "mongodb+srv://Ksathwik03:Ksathwik03@cluster0.xtzux.mongodb.net/Pythin?retryWrites=true&w=majority")
    db = db['Python']
    db = db['channel']
    return db

def error_data_base():
    error = pymongo.MongoClient(
        "mongodb+srv://Ksathwik03:Ksathwik03@cluster0.xtzux.mongodb.net/Pythin?retryWrites=true&w=majority")
    error = error['Python']
    error = error['error']
    return error


