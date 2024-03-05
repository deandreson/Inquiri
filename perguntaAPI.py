from topico import Topico
from pergunta import Pergunta
import numpy as np

"""API para consultar, incluir e alterar perguntas e respostas."""
class PerguntaAPI:
  def __init__(self, perguntasList,topicoList,respostaRealizadas=[]):
    """Construtor da classe PerguntaAPI.
    Args:
      perguntas: Uma lista de perguntas.
    """
    self.perguntasList = perguntasList
    self.topicoList = topicoList




  def consultar(self, pergunta,id_pergunta):
    """Consulta uma pergunta.
    Args:
      pergunta: O texto ou Identificador da pergunta a ser consultada.
    Returns:
      A pergunta consultada, se encontrada.
    """
    for pergunta_atual in self.perguntasList:
        if pergunta_atual.id_pergunta == id_pergunta:
            return pergunta_atual
        if pergunta_atual.pergunta == pergunta:
            return pergunta_atual
    return None

  def atualizarRespostasDePerguntas(self,id_pergunta,respota):
    self.perguntasList[id_pergunta].atualizarRespostasDePerguntas(respota)

  def iniciaBaseValoresPadrao(self):
    pergunta="Qual a fórmula de Báscara?"
    op_1="A fómula correta é dada por \(ax^2 + bx + c = 0\) : $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$ "
    op_2="A fómula  correta é dada por \(ax^3 + bx - c = 0\) : $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$ "
    op_3="A fómula  correta é dada por \(  bx - cx^3 = 0\) : $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$ "
    op_4="A fómula  correta é dada por \(ax^2 + bx  = - c(x^3-1)\) : $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$ "
    resposta=[[0],[op_1,op_2,op_3,op_4]]
    nomeTopico="Matemática"
    self.topicoList.append(Topico(len(self.topicoList),nomeTopico))
    self.incluirPergunta(pergunta, resposta, self.topicoList[-1].id_topico)

  def consultar_todas(self):
        return self.perguntasList.copy()
  def consultar_todos_Topicos(self):
     return self.perguntasList.copy(),self.topicoList.copy()
  def consultar_todos_TopicosOrdenados(self,filtroAtivas):
        vetorRespostas=[]
        for pergun in self.perguntasList:
            if (filtroAtivas and pergun.ativa ):
                vetorRespostas.append(int(pergun.qtdResposta[pergun.resposta[0][0]]))
        vetorOrdenado=[]

        for  pos in np.argsort(vetorRespostas):
              vetorOrdenado.append(self.perguntasList[pos])
        return vetorOrdenado.copy(),self.topicoList.copy()

  def atualizarPergunta(self, id_pergunt,pergunta, resposta,ativa):
    self.perguntasList[id_pergunt].atualizar(pergunta,resposta,ativa)

  def incluirPergunta(self, pergunta, resposta, id_Topico):
      id_pergunta=len(self.perguntasList)
      pergunta_nova = Pergunta(id_pergunta,pergunta, resposta, id_Topico)
      self.perguntasList.append(pergunta_nova)
  def imprimirPerguntas(self):
    Pergunta.imprimirPerguntas(Pergunta,self.perguntasList,self.topicoList)
  def incluirTopico(self,nomeTopico):
    numTopico=Topico.consultar(Topico,nomeTopico,self.topicoList)
    if numTopico==-1:
        self.topicoList.append(Topico(len(self.topicoList),nomeTopico))
