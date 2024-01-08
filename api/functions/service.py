from tinydb import Query
from config import db_user

User = Query()

def new_user(username:str, code:str, password:str):
    data_query = db_user.search(User.username == username)
    if data_query or code != "123":
        return False
    else:
        db_user.insert({'username': username,
                        'password': password})
        return True