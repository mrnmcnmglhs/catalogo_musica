from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import conectar

class ArtistaEntrada(BaseModel):
    nome: str
    
class AlbumEntrada(BaseModel):
    titulo: str
    artista_id: int

app = FastAPI(title="Catálogo Musical")

@app.get("/")
def inicio():
    return{"mensagem":"API do Catalog de música funcionando"}

@app.get("/artistas")
def listar_artistas():
    with conectar() as conexao:
        resultado = conexao.execute("SELECT id, nome FROM artistas ORDER BY id")
        return resultado.fetchall()


def buscar_artista(artista_id: int):
    with conectar() as conexao:
        resultado = conexao.execute(
            "SELECT id, nome FROM artistas WHERE id = %s", 
            (artista_id,),
        )
        return resultado.fetchone()


@app.get("/artistas/{artista_id}")
def obter_artista(artista_id: int):
    artista = buscar_artista(artista_id)
    

    if artista is None:
        raise HTTPException(
            status_code=404,
            detail="Artista não encontrado"
        )

    return artista


@app.get("/albuns")
def listar_albuns():
    with conectar() as conexao:
        resultado = conexao.execute(
            "SELECT id, titulo, artista_id FROM albuns ORDER BY id"
        )
        return resultado.fetchall()


def buscar_albuns_artista(artista_id: int):
    with conectar() as conexao:
        resultado = conexao.execute(
            "SELECT id, titulo, artista_id FROM albuns WHERE artista_id = %s ORDER BY id",
            (artista_id,),
        )
        return resultado.fetchall()


@app.get("/artistas/{artista_id}/albuns")
def listar_albuns_do_artista(artista_id: int):
    artista = buscar_artista(artista_id)
    
    if artista is None:
        raise HTTPException(
            status_code=404,
            detail="Artista não encontrado"
        )
    return buscar_albuns_artista(artista_id)



def criar_artista(nome: str):
    nome = nome.strip()
    
    if nome == "":
        return None
    
    with conectar() as conexao:
        resultado = conexao.execute(
            """INSERT INTO artistas (nome) VALUES (%s) RETURNING id, nome""",
            (nome,),
        )
        return resultado.fetchone()

@app.post("/artistas", status_code=201)
def cadastrar_artista(dados: ArtistaEntrada):
    artista = criar_artista(dados.nome)
    
    if artista is None:
        raise HTTPException(
            status_code=400,
            detail="O nome do artista é obrigatório"
        )
    return artista



@app.post("/albuns", status_code=201)
def cadastrar_album(dados: AlbumEntrada):
    artista = buscar_artista(dados.artista_id)
    
    if artista is None:
        raise HTTPException(
            status_code=404,
            detail="Artista não encontrado"
        )
        
    titulo = dados.titulo.strip()
    if titulo == "":
        raise HTTPException(
            status_code=400,
            detail="O titulo do álbum é obrigatório"
        )
        
    with conectar() as conexao:
        resultado = conexao.execute(
            """INSERT INTO albuns (titulo, artista_id) VALUES (%s, %s) RETURNING id, titulo, artista_id""",
            (titulo, dados.artista_id),
        )
        return resultado.fetchone()