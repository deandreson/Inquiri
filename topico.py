
class Topico:
  """Classe que representa uma área de conhecimento."""

  def __init__(self,id_topico, nomeTopico):
    """Construtor da classe topico.

    Args:
      nome: O nome do topico
    """

    self.id_topico=id_topico
    self.nomeTopico = nomeTopico


  def consultar(self,nomeTopico, listaTopicos):
    """Consulta uma pergunta.

    Args:
      pergunta: A pergunta a ser consultada.

    Returns:
      A pergunta consultada, se encontrada.
    """
    for topico in listaTopicos:
        if topico.nomeTopico == nomeTopico:
            return topico.id_topico
    return -1
  def retornaTopico(self,id_topico,listaTopicos):
        return listaTopicos[id_topico].nomeTopico
