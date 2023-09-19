from flask import Flask, render_template, request, url_for, flash, redirect,Markup
from werkzeug.exceptions import abort
import pickle
import json
import plotly
import pandas as pd
import plotly.graph_objs as go
from perguntaAPI import PerguntaAPI
from topico import Topico
from pergunta import Pergunta

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"

def salvarBase(tipoAcaoEscrita,basePerguntas):
    if tipoAcaoEscrita:
        try:
            with open('PerguntaAPI_base.pkl', 'wb+') as f:
                pickle.dump(basePerguntas, f)
                print("Salvo")
            f.close()
        except :
            print("erro")
            return []
    else:
        try:
            with open('PerguntaAPI_base.pkl', 'rb') as f:
                basePerguntas = pickle.load(f)
            f.close()
            return basePerguntas
        except :
            return []
    return []

# Inicializa a API e a base de perguntas, se não houver, gera a primeira por padrão
perguntas_api = PerguntaAPI([],[])
apiAuxiliar=PerguntaAPI([],[])
apiAuxiliar=salvarBase(False,0)
print(type(apiAuxiliar),apiAuxiliar)
if type(apiAuxiliar)==list:
    perguntas_api.iniciaBaseValoresPadrao()
    apiAuxiliar=salvarBase(True,perguntas_api)
else:
    perguntas_api=apiAuxiliar

# Variaveis auxilizares para filtros de perguntas e tópicos
listaTopicosAux=[True for pos in range(len(perguntas_api.topicoList))]
listaPerguntasAux=[True for pos in range(len(perguntas_api.perguntasList))]


@app.route("/")
def index():

    """ Página inicial de perguntas
    Args:
      Não é necessário
    Returns:
      Retorna um lista de perguntas ativas e os tópicos
    """
    salvarBase(True,perguntas_api)
    perguntas,topicos = perguntas_api.consultar_todos_TopicosOrdenados(filtroAtivas=True)
    return render_template("index.html", perguntas=(perguntas.copy(),topicos.copy()))
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/topicos", methods=('GET', 'POST'))
def topicos():
    """ Método que Cadastra e Filtra tópicos
    Args:
      forms: Recebe o nome do novo tópico a ser cadastrado.
    Returns:
      Retorna uma lista de tópicos, o total de perguntas em cada tópico e todas as perguntas ativas e inativas
    """
    listaTopicosAux=[True for pos in range(len(perguntas_api.topicoList))]
    salvarBase(True,perguntas_api)
    if request.method == 'POST':
        lista=list(request.form)
        if len(lista)>0 and lista[0]=="nomeTopico":
            nomeTopico = request.form['nomeTopico']
            if not nomeTopico:
               flash('O nome do Topico é necessário!')
            else:
               perguntas_api.incluirTopico( nomeTopico)
               listaTopicosAux=[True for pos in range(len(perguntas_api.topicoList))]
               return redirect(url_for('topicos'))
        else:
            listaTopicosAux=[False for pos in range(len(perguntas_api.topicoList))]
            for pos in range(len(lista)):
                if lista[pos]!="":
                    valor=int(lista[pos])
                    listaTopicosAux[valor]=True
    perguntas,topicos = perguntas_api.consultar_todos_Topicos()
    listaTopicos=[0 for pos in range(len(topicos))]
    for pergu in perguntas:
        listaTopicos[pergu.id_topico]+=1
    return render_template("topicos.html", topicos=(topicos,listaTopicos,perguntas,listaTopicosAux))


@app.route('/editar/<int:id_pergunta>', methods=('GET', 'POST'))
def editar(id_pergunta):
    """ Método que faz a edição de uma pergunta
    Args:
      forms: Recebe informações atualizadas de uma pergunta e salva.
    Returns:
      Retorna a pergunta atualizada com as novas informações
    """
    salvarBase(True,perguntas_api)
    if request.method == 'POST':
        pergunta_ret = request.form['_'+str(id_pergunta)]
        respostas_ret=[]
        respotaPos=[]
        lista=list(request.form)
        ativa=False
        for pos in range(len(lista)):
            if lista[pos]=="radioEscolha":
                   respotaPos.append(int(lista[pos+1]))
            if lista[pos]=="status":
                ativa=True
            if pos<4:
                respostas_ret.append(request.form[str(pos)])
        resposta_list = [respotaPos,respostas_ret]
        perguntas_api.atualizarPergunta(id_pergunta, pergunta_ret, resposta_list,ativa)
        flash('Atualização concluída')
        return redirect(url_for('editar',id_pergunta=id_pergunta))

    pergunta_consultada = perguntas_api.consultar("",id_pergunta)
    return render_template('editar.html',pergu=pergunta_consultada, tamResposta=len(pergunta_consultada.resposta[1]))

@app.route('/IncluirPergunta', methods=('GET', 'POST'))
def IncluirPergunta():
    """ Método que faz a inclusão de uma nova pergunta
    Args:
      forms: Recebe informações de uma pergunta e salva.
    Returns:
      Redireciona para a página de visualização de perguntas
    """
    salvarBase(True,perguntas_api)
    if request.method == 'POST':
        pergunta_ret = request.form['pergunta']
        idTopico_ret = int(request.form['idTopico'])
        respostas_ret=[]
        respotaPos=[]
        lista=list(request.form)[2:len(request.form)]
        for pos in range(len(request.form)-3):
            if lista[pos]=="radioEscolha":
                respotaPos.append(int(lista[pos+1]))
            respostas_ret.append(request.form[str(pos)])
        resposta_list = [respotaPos,respostas_ret]
        if len(respotaPos)==0:
            flash('A resposta é necessária!')
        else:
            perguntas_api.incluirPergunta( pergunta_ret, resposta_list, idTopico_ret)
            listaPerguntasAux.append(True)
            return redirect(url_for('index'))
    perguntas_,topicos =perguntas_api.consultar_todos_Topicos()
    return render_template('IncluirPergunta.html',topicos=topicos)

@app.route('/<int:id_pergunta>/resposta/<escolha>')
def resposta(id_pergunta,escolha):
    """ Método que recebe uma resposta da pergunta
    Args:
      id_pergunta e escolha: Recebe informações do id e a escolha da resposta.
    Returns:
      Redireciona para a página de visualização de resultados
    """
    perguntas = perguntas_api.consultar_todas()
    perguntas_api.atualizarRespostasDePerguntas(id_pergunta,str(escolha))
    salvarBase(True,perguntas_api)
    if len(perguntas)==0:
        return redirect(url_for('index'))
    listaPerguntasAux[id_pergunta]=False
    perguntas,topicos = perguntas_api.consultar_todos_TopicosOrdenados(filtroAtivas=True)
    listaNovaPerguntas=[]
    for pergu in perguntas:
        if listaPerguntasAux[pergu.id_pergunta]:
            listaNovaPerguntas.append(pergu)
    if len(listaNovaPerguntas)>0:
        return render_template("index.html", perguntas=(listaNovaPerguntas.copy(),topicos.copy()))
    print(listaPerguntasAux)
    for pos in range(len(listaPerguntasAux)):
        listaPerguntasAux[pos]=True
    print(listaPerguntasAux)
    return redirect(url_for('resultados'))

@app.route("/resultados")
def resultados():
    """ Faz a consulta de todas as perguntas e tópicos
    Args:
      Não é necessário
    Returns:
      Retorna um lista de perguntas ativas e inativas, Além dos tópicos
    """
    salvarBase(True,perguntas_api)
    perguntas,topicos = perguntas_api.consultar_todos_Topicos()
    return render_template("resultados.html", perguntas=perguntas.copy(),topicos = topicos.copy())

@app.route('/graficos/<int:id_pergunta>')
def graficos(id_pergunta):
    """ Método que gera um gráfico das respostas de uma pergunta
    Args:
      id_pergunta: Recebe informações do id da pergunta
    Returns:
      Redireciona para a página de visualização de resultados com um gráfico de barras e a pergunta
    """
    pergunta_consultada = perguntas_api.consultar("",id_pergunta)
    x=[pos for pos in range(1,len(pergunta_consultada.qtdResposta)+1)]
    y=pergunta_consultada.qtdResposta
    #viz = plot(fig, include_plotlyjs = True, output_type = 'div')
    #viz = Markup(viz)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    viz = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graphJSON = json.dumps(viz, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graficos.html', viz = graphJSON,pergu=pergunta_consultada)

if __name__ == "__main__":
  app.run(debug=True)
