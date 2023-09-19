from topico import Topico
class Pergunta:
  """Classe que representa uma pergunta e sua resposta."""
  id_pergunta=0

  def __init__(self,id_pergunta, pergunta, resposta, id_topico):
    """Construtor da classe Pergunta.
    Args:
      pergunta: A pergunta.
      resposta: A resposta.
      area_conhecimento: A área de conhecimento da pergunta.
    """
    self.id_pergunta = id_pergunta
    self.pergunta    = pergunta
    self.ativa    = True
    self.resposta    = resposta.copy()
    self.qtdResposta    = [0]*len(self.resposta[1])
    self.id_topico   = id_topico

  def atualizarRespostasDePerguntas(self,respota):
    vetorRespostas=self.resposta[1]
    for pos in range(len(vetorRespostas)) :
        if vetorRespostas[pos] == respota:
            self.qtdResposta[pos]+=1
            break
  def atualizar(self,pergunta, resposta,ativa):
        """Atualiza uma pergunta.

        Args:
          pergunta: A pergunta a ser atulizada.

        Returns:
          A pergunta atualizada, se encontrada.
        """
        self.pergunta    = pergunta
        self.resposta    = resposta.copy()
        self.ativa       = ativa
  def imprimirPerguntas(self, listaPerguntas,topicoList):
    for perguntas in listaPerguntas:
        print("\n=========================")
        print("pergunta: ",perguntas.pergunta)
        print("Resposta: ",perguntas.resposta)
        print("Resposta: ",perguntas.qtdResposta)
        print("Id Topico: ",Topico.retornaTopico(Topico,perguntas.id_topico,topicoList))
        print("=========================")