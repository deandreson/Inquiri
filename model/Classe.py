from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

engine = create_engine('sqlite:///inquiri.db', echo=True)
Base = declarative_base()

# Define a classe Usuario
class Usuario(Base):
    __tablename__ = 'Usuario'

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    #usuario_ativo = Column(Boolean, default=True)
    #id_materia = Column(Integer, ForeignKey('Materia.id_materia'))


# Define a classe Materia
class Materia(Base):
    __tablename__ = 'Materia'

    id_materia = Column(Integer, primary_key=True)
    dt_criacao_mat = Column(DateTime(timezone=True), default=func.now())
    nm_materia = Column(String(100), nullable=False)
    id_usuario = Column(Integer)



# Define a classe Topico
class Topico(Base):
    __tablename__ = 'Topico'

    id_materia = Column(Integer, ForeignKey('Materia.id_materia'), nullable=False)
    id_topico = Column(Integer, primary_key=True)
    dt_criacao_top = Column(DateTime(timezone=True), default=func.now())
    nm_topico = Column(String(100), nullable=False)
    id_usuario = Column(Integer)

# Define a classe Pergunta
class Pergunta(Base):
    __tablename__ = 'Pergunta'

    id_topico = Column(Integer, ForeignKey('Topico.id_topico'), nullable=False)
    id_pergunta = Column(Integer, primary_key=True)
    dt_criacao_per = Column(DateTime(timezone=True), default=func.now())
    pergunta = Column(String(255), nullable=False)
    id_usuario = Column(Integer)
    #status_pergunta = Column(Boolean, default=True)
    #Comentário sobre a pergunta

# Define a classe Alternativa
class Alternativa(Base):
    __tablename__ = 'Alternativa'

    id_alternativa = Column(Integer, primary_key=True)
    dt_criacao_alt = Column(DateTime(timezone=True), default=func.now())
    alternativa = Column(String(255), nullable=False)
    id_usuario = Column(Integer)
    id_pergunta = Column(Integer, ForeignKey('Pergunta.id_pergunta'), nullable=False)
    correta = Column(Boolean, default=False)


# Define a classe Resposta
class Resposta(Base):
    __tablename__ = 'Resposta'

    id_resposta = Column(Integer, primary_key=True)
    id_usuario = Column(Integer)
    timesdt_criacao_res = Column(DateTime(timezone=True), default=func.now())
    id_pergunta = Column(Integer, ForeignKey('Pergunta.id_pergunta'), nullable=False)
    id_alternativa = Column(Integer, ForeignKey('Alternativa.id_alternativa'), nullable=False)

# Se a base não existir
#Base.metadata.create_all(engine)