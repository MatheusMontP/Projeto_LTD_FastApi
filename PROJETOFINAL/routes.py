from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Project, db, Users
from main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import ProjetoCreate, ProjetoEdit, UsersSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix = "/auth",tags = ["Auth"])
projects_router = APIRouter(prefix = "/projetos", tags = ["Projects"])

def criar_token(id_usuario, timer_token = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + timer_token
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, password, session):
    usuario_encontrado = session.query(Users).filter(Users.email == email).first()
    if not usuario_encontrado:
        return False
    if not bcrypt_context.verify(password, usuario_encontrado.password):
        return False
    return usuario_encontrado



@auth_router.post("/criar_conta", status_code=status.HTTP_201_CREATED)
async def criar_conta(UsersSchemas: UsersSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Users).filter(Users.email == UsersSchemas.email).first()
    if usuario:
        raise HTTPException(status_code = 400, detail = "Já existe um usuario com esse email")
    else:
        senha_criptografada = bcrypt_context.hash(UsersSchemas.password)
        novo_usuario = Users(
            email = UsersSchemas.email, 
            password = senha_criptografada, 
            active = UsersSchemas.active, 
            admin = UsersSchemas.admin
            )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuario cadastrado."}
    
@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(form_data.username, form_data.password, session = session)
    if not usuario:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    acess_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, timer_token=timedelta(days=7))
    
    return {
        "acess_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.get("/refresh")
async def refresh_token_user(usuario: Users = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return {
           "acess_token": acess_token,
           "token_type:": "Bearer"
        }


@projects_router.get("/all_projects")
async def listar_projetos(session: Session = Depends(pegar_sessao)):
    """
    Método responsavel por buscar e exibir todos os projetos presentes na DB.
    """
    projetos = session.query(Project).all()
    return projetos

@projects_router.get("/projects/{id}")
async def detalhes_projeto(id: int, session: Session = Depends(pegar_sessao)):
    """
    Método responsavel por buscar apenas um projeto na DB.
    """
    projeto = session.query(Project).filter(Project.id == id).first()
    if projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    
    return projeto

@projects_router.post("/create_projects")
async def criar_projeto(ProjetoCreate: ProjetoCreate, session: Session = Depends(pegar_sessao)):
    """
    Método responsavel por criar um projeto e salva-lo na DB.
    """
    novo_projeto = Project(name = ProjetoCreate.name, description = ProjetoCreate.description)
    session.add(novo_projeto)
    session.commit()
    return {"mensagem": "Projeto criado com sucesso."}

@projects_router.put("/edit_project/{id}")
async def editar_projeto(id: int, ProjetoEdit: ProjetoEdit, session: Session = Depends(pegar_sessao)):
    """
    Método responsavel por editar um projeto já existente.
    """
    projeto = session.query(Project).filter(Project.id == id).first()

    if projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    
    ProjetoEdit = ProjetoEdit.model_dump(exclude_unset=True)
    for key, value in ProjetoEdit.items():
        setattr(projeto, key, value)

    session.commit()
    session.refresh(projeto)
    return projeto
    
@projects_router.delete("/projects/{id}")
async def deletar_projeto(id: int, session: Session = Depends(pegar_sessao)):
    """
    Método responsavel por deletar um projeto na DB.
    """
    projeto = session.query(Project).filter(Project.id == id).first()
    if projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    
    session.delete(projeto)
    session.commit()
    return None