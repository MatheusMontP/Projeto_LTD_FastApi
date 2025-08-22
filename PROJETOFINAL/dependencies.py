from models import db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import Users
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token:str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao) ):
        try:
            dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
            id_usuario = int(dic_info.get("sub"))
        except JWTError:
            raise HTTPException(status_code = 401, detail= "Acesso negado, verifique a validade do token")
        usuario = session.query(Users).filter(Users.id == id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Acesso invalido")
        return usuario