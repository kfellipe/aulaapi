from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import json
from typing import List

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define o modelo de dados dos usuários
class Usuario(BaseModel):
    Nome: str
    Idade: int
    Email: str

# Caminho para o arquivo JSON que armazenará os usuários
USUARIOS_FILE = "usuarios.json"

# Função para carregar os usuários do arquivo JSON
def carregar_usuarios():
    try:
        with open(USUARIOS_FILE, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

# Função para salvar os usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

@app.post("/token")
async def logar(data: OAuth2PasswordRequestForm = Depends()):
    if data.username == "kaua" and data.password == "cisco":
        return {"access_token": "tokensecreto", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Rota para listar todos os usuários
@app.get("/usuarios", response_model=List[Usuario])
async def listar_usuarios(token: str = Depends(oauth2_scheme)):
    usuarios = carregar_usuarios()
    return usuarios

# Rota para adicionar um novo usuário
@app.post("/usuarios")
async def adicionar_usuario(usuario: Usuario, token: str = Depends(oauth2_scheme)):
    usuarios = carregar_usuarios()
    
    # Verifica se o usuário já existe pelo email
    for u in usuarios:
        if u["Email"] == usuario.Email:
            raise HTTPException(status_code=400, detail="Usuário já existe")
    
    # Adiciona o novo usuário
    usuarios.append(usuario.dict())
    salvar_usuarios(usuarios)
    return {"message": "Usuário adicionado com sucesso"}

# Rota para atualizar um usuário existente
@app.put("/usuarios/{email}")
async def atualizar_usuario(email: str, usuario_atualizado: Usuario, token: str = Depends(oauth2_scheme)):
    usuarios = carregar_usuarios()
    for i, u in enumerate(usuarios):
        if u["Email"] == email:
            usuarios[i] = usuario_atualizado.dict()  # Atualiza o usuário
            salvar_usuarios(usuarios)
            return {"message": "Usuário atualizado com sucesso"}
    
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# Rota para deletar um usuário
@app.delete("/usuarios/{email}")
async def deletar_usuario(email: str, token: str = Depends(oauth2_scheme)):
    usuarios = carregar_usuarios()
    
    # Filtra a lista de usuários para remover o que corresponde ao email
    usuarios_filtrados = [u for u in usuarios if u["Email"] != email]
    
    if len(usuarios) == len(usuarios_filtrados):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Salva a nova lista de usuários
    salvar_usuarios(usuarios_filtrados)
    return {"message": "Usuário deletado com sucesso"}
