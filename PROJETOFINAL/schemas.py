from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enums import StatusProjeto

class ProjetoBase(BaseModel):
    name: str
    description: str | None = None 

class ProjetoCreate(ProjetoBase):
    pass

class Projetos(ProjetoBase):
    id: int
    status: StatusProjeto
    created: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjetoEdit(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusProjeto] = None

    model_config = ConfigDict(from_attributes=True)

class UsersSchema (BaseModel):
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    model_config = ConfigDict(from_attributes=True)

class LoginSchema (BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)