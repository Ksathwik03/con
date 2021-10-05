import pymongo


db = []


def data_base():
    global db
    db = pymongo.MongoClient(
        "mongodb+srv://Ksathwik03:Ksathwik03@cluster0.xtzux.mongodb.net/Pythin?retryWrites=true&w=majority")
    db = db['testing']
    db = db['channel']
    return db

def error_data_base():
    error = pymongo.MongoClient(
        "mongodb+srv://Ksathwik03:Ksathwik03@cluster0.xtzux.mongodb.net/Pythin?retryWrites=true&w=majority")
    error = error['testing']
    error = error['error']
    return error


