from pymongo import MongoClient

class Database:
    def __init__(self):
        self._client = MongoClient('mongo')
        # Petstagram Database
        self._db = self._client["PDB"]

        # User Collection
        self._users = self._db["users"]

    def get_user(self, username):
        return self._users.find_one({"username":f"{username}"})
    
    def update_user(self, username, password, salt=b'', token='', listOfPets=''):
        user_data = { "username": f"{username}", "password": password, "salt": salt, "token": token, "listOfPets":f"{listOfPets}"}
        self._users.update({"username":f"{username}"}, user_data, upsert=True)
    
    def get_user_from_cookie(self, cookie):
        return self._users.find({"token":cookie})
    