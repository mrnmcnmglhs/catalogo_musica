CREATE TABLE artistas (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0)
)

CREATE TABLE albuns (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo TEXT NOT NULL CHECK (length(trim(titulo)) > 0),
    artista_id INTEGER NOT NULL REFERENCES artistas(id)
)