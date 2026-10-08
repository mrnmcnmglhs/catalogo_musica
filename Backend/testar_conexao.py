from app.database import conectar

with conectar() as conexao:
    resultado = conexao.execute(
        "SELECT id, nome FROM artistas ORDER BY id"
    )
    print(resultado.fetchall())