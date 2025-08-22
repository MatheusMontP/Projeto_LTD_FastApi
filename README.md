# Gerenciador de Projetos LTD

Sistema web para gerenciamento de projetos, com autenticação de usuários, desenvolvido em Python (FastAPI) no backend e HTML/CSS/JavaScript no frontend.

## Funcionalidades

- Cadastro e login de usuários com autenticação JWT
- Criação, edição, listagem e exclusão de projetos
- Status do projeto: Ativo, Pausado, Finalizado
- Integração com banco de dados PostgreSQL
- Migrações de banco com Alembic

## Estrutura do Projeto

```
.
├── .env
├── alembic/
├── alembic.ini
├── dependencies.py
├── enums.py
├── main.py
├── models.py
├── requirements.txt
├── routes.py
├── schemas.py
├── frontend/
│   ├── index.html
│   ├── projetos.html
│   ├── css/
│   │   ├── style.css
│   │   └── projetos.css
│   └── js/
│       ├── script.js
│       └── projetos.js
└── ...
```

## Instalação

### 1. Clone o repositório

```sh
git clone https://github.com/MatheusMontP/Projeto_LTD_FastApi.git
cd Projeto_LTD/PROJETOFINAL
```

### 2. Crie e ative um ambiente virtual

```sh
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```sh
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Edite o arquivo [.env](.env) com sua `SECRET_KEY` e dados do banco PostgreSQL:

```
SECRET_KEY = sua_chave_secreta
ALGORITHM = HS256
ACESS_TOKEN_EXPIRE_MINUTES = 60
```

No arquivo [models.py](models.py), ajuste as variáveis de conexão do banco se necessário.

### 5. Configure o banco de dados

Certifique-se de ter um banco PostgreSQL rodando e crie o banco:

```sh
# Exemplo usando psql
psql -U postgres
CREATE DATABASE "BancoLTD";
```

### 6. Execute as migrações

```sh
alembic upgrade head
```

## Execução

### Backend (FastAPI)

```sh
uvicorn main:app --reload
```

A API estará disponível em http://127.0.0.1:8000

### Frontend

Abra o arquivo [frontend/index.html](frontend/index.html) no navegador ou utilize uma extensão de servidor local (ex: Live Server no VSCode).

## Endpoints Principais

- `POST /auth/criar_conta` — Criação de usuário
- `POST /auth/login` — Login e obtenção do token JWT
- `GET /projetos/all_projects` — Listar todos os projetos
- `GET /projetos/projects/{id}` — Detalhes de um projeto
- `POST /projetos/create_projects` — Criar projeto
- `PUT /projetos/edit_project/{id}` — Editar projeto
- `DELETE /projetos/projects/{id}` — Excluir projeto

## Estrutura dos Principais Arquivos

- [main.py](main.py): Inicialização do FastAPI, configuração de CORS e inclusão das rotas.
- [models.py](models.py): Modelos ORM do SQLAlchemy para usuários e projetos.
- [schemas.py](schemas.py): Schemas Pydantic para validação de dados.
- [routes.py](routes.py): Rotas de autenticação e gerenciamento de projetos.
- [dependencies.py](dependencies.py): Dependências de sessão e autenticação.
- [frontend/](frontend/): Interface web (HTML, CSS, JS).

## Telas

- **Login/Cadastro:** [frontend/index.html](frontend/index.html)
- **Gerenciamento de Projetos:** [frontend/projetos.html](frontend/projetos.html)

## Observações

- O frontend espera que o backend esteja rodando em `http://127.0.0.1:8000`.
- O token JWT é salvo no `localStorage` e usado para acessar as páginas protegidas.
- Para acessar a tela de projetos, é necessário estar autenticado.
