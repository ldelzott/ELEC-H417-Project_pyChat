
# Use this to reset/DEBUG the database

from tinydb import TinyDB, Query
db = TinyDB('db.json')

#db.drop_tables() # Clean the db

userdb = db.table('authTable')
#userdb.insert({'user': 'dummy_username', 'hpassword': 'pwd'}) # To remove
passwd = Query()
tempDict = userdb.search(passwd.user=='sacha')
print(tempDict[0]["hpassword"])

#for item in userdb:
#    print(item)