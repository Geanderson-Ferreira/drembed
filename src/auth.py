import requests
from os import environ
from dotenv import load_dotenv
from src.SQLManager import User, register_user_access

load_dotenv()

def auth(user, password, session):

    try:
        # Encontrar o usuário pelo username
        user = session.query(User).filter(User.user_name == user).one()
        
        if user.password == password:
            register_user_access(session, user)
            return True
        else:
            return False
    except:
        return False
