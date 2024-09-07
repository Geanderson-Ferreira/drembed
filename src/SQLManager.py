from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from os import environ
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
# # Definir a URL do banco de dados
# DATABASE_URL = environ['DATABASE_URL']

# # Criar a engine do banco de dados
# engine = create_engine(DATABASE_URL, echo=False)

# Definir a base para as classes
Base = declarative_base()

# Definir a classe User
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    last_access = Column(DateTime, nullable=True)

# Definir a classe Report
class Report(Base):
    __tablename__ = 'Reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_name = Column(String(255), nullable=False)
    report_content = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

# Criar as tabelas no banco de dados
def create_tables():
    Base.metadata.create_all(engine)

# Criar as tabelas
# if __name__ == "__main__":
#     create_tables()


def get_valid_reports(session):
    reports_dict = {}
    try:
        # Consultar todos os relatórios ativos
        reports = session.query(Report).filter(Report.is_active == True).all()
        
        for report in reports:
            # Usar report_name como chave e report_content como valor
            reports_dict[report.report_name] = report.report_content
        
        return reports_dict
    
    except Exception as e:
        print(f"Erro ao obter relatórios: {e}")
        return {}


def verify_user_credentials(username: str, password: str, session):
    try:
        # Encontrar o usuário pelo username
        user = session.query(User).filter(User.user_name == username).one()
        
        if user.password == password:
            return True
        else:
            return False
    except:
        return False

def get_session(DATABASE_URL):

    engine = create_engine(DATABASE_URL, echo=False)
    # Configurar a sessão
    Session = sessionmaker(bind=engine)
    return Session()

def register_user_access(session, user):
    try:
        
        # Atualizar o campo last_access com a data e hora atual
        user.last_access = datetime.now()
        
        # Commit para salvar as alterações no banco de dados
        session.commit()
        
        print(f"Acesso registrado para o usuário {user.user_name}.")
        
    except:
        print(f"Usuário {user.user_name} não encontrado.")
