from model.Classe import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey,update
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for, redirect,jsonify
from sqlalchemy.sql import func
import json 
import os
import pandas as pd
import plotly
import plotly.graph_objs as go


# Cria a engine e conecta ao banco de dados
engine = create_engine('sqlite:///inquiri.db', echo=True)
Base = declarative_base()
Base.metadata = Base.metadata


# Se a base não existir
#Base.metadata.create_all(engine)


#### Execução ###
#   python3 -m venv venv
#	source venv/bin/activate
#	cd Aplicativos/Inquiri
#   export FLASK_ENV=development 
#   export FLASK_APP=Inquiri
###########################################

# Cria uma sessão
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
@app.route('/') 
def index():
    return render_template('index.html',perguntas=consultaTodasPerguntas())
@app.route('/resultados')
def resultados():    
    return render_template('resultados.html',perguntas=consultaPerguntasComTotal())
@app.route('/materia')
def materia():
    return render_template('materia.html')
@app.route('/grafico/<int:id_pergunta>')
def grafico(id_pergunta):
    consulta=consultaPerguntasComTotal_alt(id_pergunta)
    grafico=consultarGrafico(consulta)
    return render_template('grafico.html',viz=grafico,consulta=consulta)
@app.route('/topicos')
def topicos():
    materias = session.query(Materia).all()
    return render_template('topicos.html',materias=materias)
@app.route('/perguntas')
def perguntas():
    topicos = session.query(Topico).all()
    return render_template('perguntas.html',topicos=topicos)
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')
@app.route('/pergunta/<int:id_topico>')
def pergunta(id_topico):
    topicos = session.query(Topico).filter_by(id_topico=id_topico).all()
    return render_template('perguntas.html',topicos=topicos)
@app.route('/editarpergunta/<int:id_pergunta>')
def editarpergunta(id_pergunta):
    pergunta = session.query(Pergunta).filter_by(id_pergunta=id_pergunta).first()
    alternativas = session.query(Alternativa).filter_by(id_pergunta=id_pergunta).all()
    topicos = session.query(Topico).all()
    return render_template('editarpergunta.html',pergunta=pergunta,alternativas=alternativas,topicos=topicos)
#################### Inserção #############################
@app.route('/atualizar_pergunta_forms', methods=['POST'])
def atualizar_pergunta_forms():
    dados = request.form
    radioSelecionado=int(dados['radioEscolha'])

    for lin in dados:
        if lin.startswith("pergunta"):
            id_pergunta = int(lin.split("_")[1])
            pergunta = dados[lin]
            atualizar_pergunta(id_pergunta,pergunta)
        elif lin!= "radioEscolha":
            id_alternativa=int(lin)
            alternativa=dados[lin]
            correta=False
            if int(lin)==radioSelecionado:
                correta=True
            atualizar_alternativa(id_alternativa,alternativa,correta)
    return jsonify({'message': 'Pergunta e alternativas atualizadas com sucesso!'}),200

@app.route('/inserir_materia', methods=['POST'])
def inserir_materia():
    data = request.json
    nm_materia = data['nm_materia']
    id_usuario = data['id_usuario']

    if 'nm_materia' not in data or 'id_usuario' not in data:
        return jsonify({'message': 'Os campos nm_materia e id_usuario são obrigatórios'}), 400
    materia =Materia(nm_materia=nm_materia,id_usuario=id_usuario)
    session.add(materia)
    session.commit()

    # Adicionando a nova matéria ao banco de dados
    
    return jsonify({'message': 'Matéria inserida com sucesso!'}), 201

@app.route('/inserir_topico', methods=['POST'])
def inserir_topico():
    data = request.json
    id_materia = data['id_materia']
    nm_topico = data['nm_topico']
    id_usuario = data['id_usuario']
    print("=================== Inserir Topico")
    print(id_materia,nm_topico)

    if 'id_materia' not in data or 'nm_topico' not in data or 'id_usuario' not in data:
        return jsonify({'message': 'Os campos são obrigatórios'}), 400
    topico =Topico(id_materia=id_materia,nm_topico=nm_topico,id_usuario=id_usuario)
    session.add(topico)
    session.commit()    
    return jsonify({'message': 'Tópico inserido com sucesso!'}), 201

@app.route('/inserir_resposta', methods=['POST'])
def inserir_resposta():
    data = request.json
    id_pergunta = data['id_pergunta']
    id_alternativa  =  data['id_alternativa']
    id_usuario = data['id_usuario']

    if 'id_pergunta' not in data or 'id_alternativa' not in data or 'id_usuario' not in data:
        return jsonify({'message': 'Os campos são obrigatórios'}), 400
    resposta =Resposta(id_pergunta=id_pergunta,id_alternativa=id_alternativa,id_usuario=id_usuario)
    session.add(resposta)
    session.commit()    
    consulta = consultaPerguntaX(id_pergunta,id_alternativa)

    return jsonify({'message': consulta}), 201
@app.route('/inserir_pergunta', methods=['POST'])
def inserir_pergunta():
    data = request.json
    id_topico = data['id_topico']
    pergunta = data['pergunta']
    dados = data['dados']
    print(dados)

    if 'id_topico' not in data or 'pergunta' not in data :
        return jsonify({'message': 'Os campos são obrigatórios'}), 400
    pergunta =Pergunta(id_topico=id_topico,pergunta=pergunta,id_usuario=10145310)
    session.add(pergunta)
    session.commit()    
    id_nova_pergunta = pergunta.id_pergunta
    session.add(Alternativa(alternativa=dados['0'],id_pergunta=id_nova_pergunta,correta= (0==int(dados['radio'])),id_usuario=10145310))
    session.add(Alternativa(alternativa=dados['1'],id_pergunta=id_nova_pergunta,correta= (1==int(dados['radio'])),id_usuario=10145310))
    session.add(Alternativa(alternativa=dados['2'],id_pergunta=id_nova_pergunta,correta= (2==int(dados['radio'])),id_usuario=10145310))
    session.add(Alternativa(alternativa=dados['3'],id_pergunta=id_nova_pergunta,correta= (3==int(dados['radio'])),id_usuario=10145310))
    session.commit()    
    return jsonify({'message': 'Tópico inserida com sucesso!'}), 201
########## Consulta @@@@@@@@@@@@@

def consultarGrafico(pergunta):
    x=[pos for pos in range(1,5)]
    y=[]
    for pos in pergunta[0]['alternativas']:
        y.append(pos['total_resposta_alternativa'])
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    viz = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graphJSON = json.dumps(viz, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    return graphJSON
@app.route('/pergunta_con')
def pergunta_con():
    # Consulta para obter perguntas com suas alternativas   
    consulta = session.query(Pergunta).join(Alternativa).all()
    return render_template('index.html',consulta=consulta)
@app.route('/topico_con')
def topico_con():
    topicos = session.query(Topico, func.count(Pergunta.id_pergunta).label('total_perguntas')) \
            .outerjoin(Pergunta, Pergunta.id_topico == Topico.id_topico) \
            .group_by(Topico.id_topico) \
            .all()
    perguntas_json = [{'id_topico': topico.id_topico,'id_materia': topico.id_materia,                    'nm_topico': topico.nm_topico,                    'id_usuario': topico.id_usuario,                    'dt_criacao_top': topico.dt_criacao_top,                    'total_perguntas': total_perguntas} for topico, total_perguntas in topicos]
  
    return jsonify(perguntas_json)

@app.route('/materia_con')
def materia_con():
    materias = session.query(Materia).all() # Recupere todas as matérias do banco de dados
    materia_json = [{'id_materia': materia.id_materia,'nm_materia': materia.nm_materia, 'id_usuario': materia.id_usuario, 'dt_criacao_top': materia.dt_criacao_mat} for materia in materias]  
    return jsonify(materia_json)

@app.route('/materia_topico_con')
def materia_topico_con():
    consulta=consultaTopicosMaterias()
    return jsonify(consulta)

######### Consultas Funcao
@app.route("/consultaTopicosMaterias")
def consultaTopicosMaterias():
    consulta = session.query(
        Materia,
        Topico,
        func.count(Pergunta.id_pergunta).label('total_perguntas')
    ).outerjoin(
        Topico,
        Topico.id_materia == Materia.id_materia
    ).outerjoin(
        Pergunta,
        Pergunta.id_topico == Topico.id_topico
    ).group_by(
        Materia.id_materia,
        Topico.id_topico
    ).all()
    materias_e_topicos = {}
    for materia,topico,total_perguntas in consulta:
        if materia.id_materia not in materias_e_topicos:
            materias_e_topicos[materia.id_materia] = {
                'id_materia': materia.id_materia,
                'nm_materia': materia.nm_materia,
                'topicos': []
            }
        if not(isinstance(topico, type(None))):
            if topico.id_materia == materia.id_materia:
                print(materias_e_topicos[materia.id_materia]['topicos'], type(topico),type(topico) is None)
                materias_e_topicos[materia.id_materia]['topicos'].append({
                    'id_topico': topico.id_topico,
                    'id_materia': topico.id_materia,
                    'nm_topico': topico.nm_topico,
                    'total_perguntas': total_perguntas
                })
    return materias_e_topicos
def consultaPerguntaX(id_pergunta,id_alternativa):
    consulta = session.query(Alternativa.id_pergunta,Alternativa.id_alternativa,Alternativa.correta).\
    filter(Alternativa.id_pergunta == id_pergunta).\
    filter(Alternativa.id_alternativa == id_alternativa).all()
    retorno = {}
    # Iterar sobre os resultados da consulta e adicionar ao dicionário
    for cons in consulta:
        retorno['correta'] = cons.correta
    return retorno
@app.route("/consultaPerguntaXTotal/<int:id_pergunta>")
def consultaPerguntaXTotal(id_pergunta):
    contagem_respostas = session.query(Alternativa,
                                    func.count(Resposta.id_resposta).label('total_respostas')).filter(
        Alternativa.id_pergunta == id_pergunta, Alternativa.id_alternativa == Resposta.id_alternativa).group_by(Alternativa.id_pergunta,
                                Alternativa.id_alternativa,Alternativa.correta).all()
    contagem_respostas_json = [
    {
        'id_pergunta': alternativa.id_pergunta,
        'id_alternativa': alternativa.id_alternativa,
        'correta': alternativa.correta,
        'total_respostas': total_respostas
    } for alternativa, total_respostas in contagem_respostas]
    return contagem_respostas_json 

@app.route("/consultaTodasPerguntas")
def consultaTodasPerguntas():
    perguntas = session.query(Pergunta, Alternativa,Topico,Materia).\
    join(Alternativa, Pergunta.id_pergunta == Alternativa.id_pergunta).\
    join(Topico, Pergunta.id_topico == Topico.id_topico).\
    join(Materia, Topico.id_materia == Materia.id_materia).\
    all()
   
    perguntas_e_alternativas = {}

    for pergunta, alternativa,topico, materia  in perguntas:
        if pergunta.id_pergunta not in perguntas_e_alternativas:
            perguntas_e_alternativas[pergunta.id_pergunta] = {
                'id_pergunta': pergunta.id_pergunta,
                'pergunta': pergunta.pergunta,
                'id_topico': topico.id_topico,
                'nm_topico': topico.nm_topico,
                'id_materia': topico.id_materia,                
                'nm_materia': materia.nm_materia,
                'alternativas': []
            }
        perguntas_e_alternativas[pergunta.id_pergunta]['alternativas'].append({
            'id_alternativa': alternativa.id_alternativa,
            'alternativa': alternativa.alternativa,
            'correta': alternativa.correta
        })
    return  list(perguntas_e_alternativas.values())

def consultaTodasPerguntas_():
    perguntas = session.query(Pergunta, Alternativa, Topico, Materia).\
    join(Alternativa, Pergunta.id_pergunta == Alternativa.id_pergunta).\
    join(Topico, Pergunta.id_topico == Topico.id_topico).\
    join(Materia, Topico.id_materia == Materia.id_materia).\
    all()
    perguntas_e_alternativas = {}
    for pergunta, alternativa, topico, materia in perguntas:
        if pergunta.id_pergunta not in perguntas_e_alternativas:
            perguntas_e_alternativas[pergunta.id_pergunta] = {
                'id_pergunta': pergunta.id_pergunta,
                'pergunta': pergunta.pergunta,
                'id_topico': topico.id_topico,
                'nm_topico': topico.nm_topico,
                'nm_materia': materia.nm_materia,
                'alternativas': []
            }
        perguntas_e_alternativas[pergunta.id_pergunta]['alternativas'].append({
            'id_alternativa': alternativa.id_alternativa,
            'alternativa': alternativa.alternativa,
            'correta': alternativa.correta
        })
    return  list(perguntas_e_alternativas.values())
def consultaPerguntasComTotal():
    perguntas_alternativas_com_total_respostas = session.query(
        Pergunta,    
        Alternativa,
        func.count(Resposta.id_alternativa).label('total_resposta_alternativa'),
    ).outerjoin(
        Alternativa,
        Pergunta.id_pergunta == Alternativa.id_pergunta
    ).outerjoin(
        Resposta,
        Resposta.id_alternativa == Alternativa.id_alternativa
    ).group_by(
        Pergunta.id_pergunta,
        Alternativa.id_alternativa,
    ).all()
    perguntas_json = []
    
    # Iterar sobre os resultados da consulta
    for pergunta, alternativa, total_resposta_alternativa in perguntas_alternativas_com_total_respostas:
        # Verificar se a pergunta já foi adicionada à lista
        pergunta_existente = next((p for p in perguntas_json if p['id_pergunta'] == pergunta.id_pergunta), None)
        # Se a pergunta não estiver na lista, adicioná-la
        if not pergunta_existente:
            pergunta_existente = {
                'id_pergunta': pergunta.id_pergunta,
                'pergunta': pergunta.pergunta,
                'alternativas': []
            }
            perguntas_json.append(pergunta_existente)

        # Adicionar alternativa à pergunta
        if alternativa:
            alternativa_json = {
                'id_alternativa': alternativa.id_alternativa,
                'alternativa': alternativa.alternativa,
                'correta': alternativa.correta,
                'total_resposta_alternativa':total_resposta_alternativa
            }
            pergunta_existente['alternativas'].append(alternativa_json)
    return perguntas_json
def consultaPerguntasComTotal_alt(id_pergunta):
    perguntas_alternativas_com_total_respostas = session.query(
    Pergunta,                
    Alternativa,
    func.count(Resposta.id_pergunta).label('total_resposta_alternativa')
    ).outerjoin(
        Alternativa,
        Pergunta.id_pergunta == Alternativa.id_pergunta
    ).outerjoin(
        Resposta,
        Alternativa.id_alternativa == Resposta.id_alternativa
    ).filter(
        Pergunta.id_pergunta == id_pergunta
    ).group_by(
        Pergunta.id_pergunta,
        Alternativa.id_alternativa,
    ).all()
    perguntas_json = []    
    # Iterar sobre os resultados da consulta
    for pergunta,alternativa,total_resposta_alternativa in perguntas_alternativas_com_total_respostas:
        # Verificar se a pergunta já foi adicionada à lista
        pergunta_existente = next((p for p in perguntas_json if p['id_pergunta'] == pergunta.id_pergunta), None)
        # Se a pergunta não estiver na lista, adicioná-la
        if not pergunta_existente:
            pergunta_existente = {
                'id_pergunta': pergunta.id_pergunta,
                'pergunta': pergunta.pergunta,                
                'alternativas': []
            }
            perguntas_json.append(pergunta_existente)

        # Adicionar alternativa à pergunta
        if alternativa:
            alternativa_json = {
                'id_alternativa': alternativa.id_alternativa,
                'alternativa': alternativa.alternativa,
                'correta': alternativa.correta,
                'total_resposta_alternativa':total_resposta_alternativa
                
            }
            pergunta_existente['alternativas'].append(alternativa_json)
    return perguntas_json

def atualizar_alternativa(id_alternativa,alternativa,correta):
    alternativa_id = session.query(Alternativa).filter_by(id_alternativa=id_alternativa).first()
    alternativa_id.alternativa =alternativa
    alternativa_id.correta = correta
    session.commit()

    
def atualizar_pergunta(id_pergunta,pergunta):
    pergunta_id = session.query(Pergunta).filter_by(id_pergunta=id_pergunta).first()
    pergunta_id.pergunta = pergunta
    session.commit()



if __name__ == '__main__':
    app.run(debug=True)