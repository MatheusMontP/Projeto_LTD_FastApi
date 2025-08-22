from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Enum as DBEnum, Boolean
from sqlalchemy.orm import declarative_base
import datetime
import os
from enums import StatusProjeto

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "matheus2004")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "BancoLTD")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column("id", Integer, primary_key = True, index = True)
    name = Column("nome", String, nullable = False)
    description = Column("descricao", Text)
    status = Column(DBEnum(StatusProjeto), nullable = False)
    created = Column("data", DateTime, default = datetime.datetime.utcnow)

    def __init__(self, name, description, status='Ativo'):
        self.name = name
        self.description = description
        self.status = status

class Users(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key = True, autoincrement = True)
    name_user = Column("nome", String)
    email = Column("email", String, nullable = False)
    password = Column("senha", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default = False)

    def __init__(self, email, password, active = True, admin = False):
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin
