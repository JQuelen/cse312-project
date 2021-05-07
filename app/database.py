from pymongo import MongoClient

class Database:
    def __init__(self):
        self._client = MongoClient('mongo')
        # Petstagram Database
        self._db = self._client["PDB"]

        # User Collection
        self._users = self._db["users"]

        # Photos Collection
        self._photos = self._db["photos"]


    def get_user(self, username):
        return self._users.find_one({"username":f"{username}"})
    
    def update_user(self, username, password, salt=b'', token='', listOfPets="", logged_in=False, photos=[], messages={}):
        user_data = { "username": f"{username}", "password": password, "salt": salt, "token": token, "listOfPets":listOfPets, "logged_in":logged_in, "photos":photos, "messages":messages}
        self._users.update({"username":f"{username}"}, user_data, upsert=True)
    
    def get_user_from_cookie(self, cookie):
        return self._users.find({"token":cookie})
    
    def get_users_online(self):
        return self._users.find({"logged_in":True}, {"_id":0, "username":1}) 

    def get_photos(self):
        return self._photos.find()

    def update_photo(self, photo_path, username, upload_date=""):
        photo_data = { "photo_path": photo_path, "username": username, "upload_date": upload_date}
        self._photos.update({"photo_path":photo_path}, photo_data, upsert=True)
