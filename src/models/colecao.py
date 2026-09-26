""" Organização e gerenciamento da lista de jogos."""
from typing import List
from src.models.jogo import Jogo

class colecao: 
    """ lista personalida do usuário """
    def __init__(self,nome: str):
        self.nome = nome  
        """ guarda o nome da lista """
        self.jogos: List[Jogo] = [] 
        """ lista vazia que vai guardar os jogos """

    def adicionar_jogo(self, jogo: Jogo) -> None: 
        """ adiciona um jogo na coleção """
        pass

    def remover_jogo(self, titulo: str) -> None: 
        """ remove um jogo da coleção """
        pass

    def listar_jogos(self) -> List[Jogo]: 
        """ retorna todos os jogos guardados na coleção """
        pass