""" gerenciamento do perfil do usuário e suas coleções."""
from typing import List, Optional
from src.models.colecao import Colecao

class Usuario: 
    """ 
    representa o perfil do usuario e suas coleções pessoais.
    nome (str): nome ou apelido do jogador.
    colecoes (List[Colecao]): Lista das coleções criadas pelo usuário.
    """

    def __init__(self, nome: str):
        self.nome = nome
        self.colecoes: List[Colecao] = []

    def criar_colecao(self, nome_colecao: str) -> None:
        """ instância que adiciona uma nova coleção para o perfil do usuário """
        pass

    def listar_colecoes(self) -> List[Colecao]:
        """Retorna a lista de todas as coleções do usuário."""
        pass

    def remover_colecao(self, nome_colecao: str) -> None:
        """elimina uma coleção existente no perfil do usuário"""
        pass 

    def buscar_colecao(self, nome_colecao: str) -> Optional[Colecao]:
        """ Busca e retorna uma coleção específica pelo nome. """
        pass