import ZODB, ZODB.FileStorage
import os
import transaction
storage = ZODB.FileStorage.FileStorage('data' + os.sep + 'mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

def saveData(key,data):
    root[key] = data
    transaction.commit()
    #connection.close()


def getData(key):
    #storage = ZODB.FileStorage.FileStorage('data' + os.sep + 'mydata.fs')
    #db = ZODB.DB(storage)
    #connection = db.open()
    root = connection.root()
    data = root[key]
    #connection.close()
    return data