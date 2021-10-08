import os

import pymongo


db = []

Password = os.getenv('Password')
def data_base():
    global db
    db = pymongo.MongoClient(
        f'mongodb+srv://Ksathwik03:{Password}@cluster0.xtzux.mongodb.net/Pythin?retryWrites=true&w=majority')
    db = db['testing']
    db = db['channel']
    return db

def error_data_base():
    error = pymongo.MongoClient(
        f"mongodb+srv://Ksathwik03:{Password}@cluster0.xtzux.mongodb.net/Pythin?retryWrites=true&w=majority")
    error = error['testing']
    error = error['error']
    return error


