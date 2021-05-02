from pymongo import MongoClient

class Database:
    def __init__(self):
        self._client = MongoClient('mongo')
        # Petstagram Database
        self._db = self._client["PDB"]

        self._users = self._db["users"]

    def db(self):
        return self._db
    
    def get_user(self, username):
        return self._users.find({"username":f"{username}"})
    
    def update_user(self, username, password, salt=b'', session_cookie=""):
        user_data = { "username": f"{username}", "password": password, "salt": salt, "session_cookie":f"{session_cookie}"}
        self._users.update({"username":f"{username}"}, user_data, upsert=True)