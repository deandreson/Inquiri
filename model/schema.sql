DROP TABLE IF EXISTS Alternativa;
DROP TABLE IF EXISTS Resposta;
DROP TABLE IF EXISTS Pergunta;
DROP TABLE IF EXISTS Topico;
DROP TABLE IF EXISTS Materia;
DROP TABLE IF EXISTS Usuario;

-- Tabela Usuario
CREATE TABLE Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);
-- Tabela Materia
CREATE TABLE Materia (
    id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
    dt_criacao_mat DATETIME DEFAULT CURRENT_TIMESTAMP,
    nm_materia TEXT NOT NULL,
    id_usuario INTEGER
);

-- Tabela Topico
CREATE TABLE Topico (
    id_materia INTEGER,
    id_topico INTEGER PRIMARY KEY AUTOINCREMENT,
    dt_criacao_top DATETIME DEFAULT CURRENT_TIMESTAMP,
    nm_topico TEXT NOT NULL,
    id_usuario INTEGER,
    FOREIGN KEY (id_materia) REFERENCES Materia(id_materia)
);

-- Tabela Pergunta
CREATE TABLE Pergunta (
    id_topico INTEGER,
    id_pergunta INTEGER PRIMARY KEY AUTOINCREMENT,
    dt_criacao_per DATETIME DEFAULT CURRENT_TIMESTAMP,
    pergunta TEXT NOT NULL,
    id_usuario INTEGER,
    FOREIGN KEY (id_topico) REFERENCES Topico(id_topico)
);

-- Tabela Alternativa
CREATE TABLE Alternativa (
    id_alternativa INTEGER PRIMARY KEY AUTOINCREMENT,
    dt_criacao_alt DATETIME DEFAULT CURRENT_TIMESTAMP,
    alternativa TEXT NOT NULL,
    id_usuario INTEGER,
    id_pergunta INTEGER,
    correta BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_pergunta) REFERENCES Pergunta(id_pergunta)
);

-- Tabela Resposta
CREATE TABLE Resposta (
    id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    timesdt_criacao_res DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_pergunta INTEGER,
    id_alternativa INTEGER,
    FOREIGN KEY (id_pergunta) REFERENCES Pergunta(id_pergunta),
    FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa)
);
