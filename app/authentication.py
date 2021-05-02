import string
import random

def create_auth_token():
    letters = string.ascii_letters
    token = ''.join(random.choice(letters) for i in range(80))
    return token