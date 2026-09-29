""" Organização e gerenciamento da lista de jogos (CRUD)."""
from typing import List, Optional
from src.models.jogo import Jogo

class colecao: 
    """ lista personalida do usuário """
    def __init__(self,nome: str):
        self.nome = nome  
        """ guarda o nome da lista """
        self.jogos: List[Jogo] = [] 
        """ lista vazia que vai guardar os jogos """

    def adicionar_jogo(self, jogo: Jogo) -> None: # Create
        """ adiciona um jogo na coleção """
        pass

    def remover_jogo(self, titulo: str) -> bool: # delete
        """ 
        Remove um jogo buscando pelo seu título. 
        Retorna True se removido com sucesso, retorna False se não encontrar o jogo. 
        """
        pass

    def listar_jogos(self) -> List[Jogo]: # read
        """ retorna todos os jogos guardados na coleção """
        pass

    def buscar_por_titulo(self, titulo:str) -> Optional[Jogo]: # read
        # Utilizar o Optinal para quando buscar um jogo pelo título, a função retornar um objeto do tipo Jogo (se ele for encontrado na lista) ou vai retornar None (se o jogo não existir na coleção).
        """Busca e retorna um jogo específico na coleção pelo título."""
        pass

    def atualizar_jogo(self, titulo:str, **kwargs) -> bool: # update
        # **kwargs permite que passe qualquer quantidade de alterações de uma só vez, sem precisares criar uma função para cada tipo de alteração.
        """
        Atualiza os dados de um jogo existente na coleção buscando pelo título.
        Retorna True se atualizado com sucesso, retorna False se não tiver encontrado o jogo.
        """
        pass