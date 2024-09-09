from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from os import environ
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = environ['DATABASE_URL']

# Criar a engine do banco de dados e configurar o Session
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,  # Número de conexões no pool
    max_overflow=20,
    pool_recycle=1800  # Número máximo de conexões adicionais que o pool pode criar
)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    last_access = Column(DateTime, nullable=True)

class Report(Base):
    __tablename__ = 'Reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_name = Column(String(255), nullable=False)
    report_content = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    rep_type = Column(String(255))

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()

def get_valid_reports():
    reports_dict = {}
    reports_types = {}
    li = []
    with Session() as session:
        try:
            reports = session.query(Report).filter(Report.is_active == True).all()
            for report in reports:
                reports_dict[report.report_name] = report.report_content
                reports_types[report.report_name] = report.rep_type
            li.append(reports_dict)
            li.append(reports_types)
            return li
        except Exception as e:
            print(f"Erro ao obter relatórios: {e}")
            return {}

def verify_user_credentials(username: str, password: str):
    with Session() as session:
        try:
            user = session.query(User).filter(User.user_name == username).one()
            return user.password == password
        except:
            return False

def register_user_access(user):
    with Session() as session:
        try:
            user.last_access = datetime.now()
            session.commit()
            print(f"Acesso registrado para o usuário {user.user_name}.")
        except:
            print(f"Usuário {user.user_name} não encontrado.")
