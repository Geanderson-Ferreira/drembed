from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from src.SQLManager import User, register_user_access
from os import environ
from dotenv import load_dotenv

load_dotenv()

# Definir a URL do banco de dados
DATABASE_URL = environ['DATABASE_URL']

# Criar a engine do banco de dados
engine = create_engine(DATABASE_URL, echo=False)

# Criar a fábrica de sessões
SessionFactory = sessionmaker(bind=engine)

def auth(user_name, password):
    """
    Verifica as credenciais do usuário e registra o acesso se válido.
    
    :param user_name: Nome do usuário.
    :param password: Senha do usuário.
    :return: True se as credenciais forem válidas, False caso contrário.
    """
    session = SessionFactory()  # Cria uma nova sessão
    
    try:
        # Encontrar o usuário pelo username
        user = session.query(User).filter(User.user_name == user_name).one()
        
        if user.password == password:
            register_user_access(user)
            session.commit()  # Confirma as alterações
            return True
        else:
            return False
    except NoResultFound:
        return False
    finally:
        session.close()  # Garante que a sessão seja fechada
