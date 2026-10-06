""" gerenciamento do perfil do usuário e suas coleções."""
from typing import List, Optional
from src.models.colecao import Colecao

class Usuario: 
    """ 
    representa o perfil do usuario e suas coleções pessoais.
    nome (str): nome ou apelido do jogador.
    colecoes (List[Colecao]): Lista das coleções criadas pelo usuário.
    """

    def __init__(self, nome: str, email:str):
        """Inicializa o utilizador com nome, e-mail validado e lista de coleções."""
        self.nome = nome
        self.email = email # usa o setter para validar.
        self._colecoes: List[Colecao] = []

# -=-=-= ENCAPSULAMENTO (@property) -=-=-=

    @property
    def email(self) -> str:
        """Getter: Retorna o email do usuário."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Setter: Valida o formato básico do email."""
        if not "@" in valor or "." not in valor:
            raise ValueError("O e-mail fornecido é inválido.")
        self._email = valor

    @property
    def colecoes(self) -> List[Colecao]:
        """Getter: Retorna uma cópia da lista de coleções.;"""
        return self._colecoes.copy()

# -=-=-= MÉTODOS DE GERENCIAMENTO DE COLEÇÕES -=-=-=

    def criar_colecao(self, nome_colecao: str) -> None:
        """ instância que adiciona uma nova coleção para o perfil do usuário """
        if self.buscar_colecao(nome_colecao) is not None:
            raise ValueError(f"A coleção {nome_colecao} já existe.")

        nova_colecao = Colecao(nome_colecao)
        self._colecoes.append(nova_colecao)
        return nova_colecao
    
    def listar_colecoes(self) -> List[Colecao]:
        """Retorna a lista de todas as coleções do usuário."""
        return self.colecoes

    def remover_colecao(self, nome_colecao: str) -> None:
        """elimina uma coleção existente no perfil do usuário"""
        colecao = self.buscar_colecao(nome_colecao)
        if colecao:
            self._colecoes.remove(colecao) 
            return True
        return False

    def buscar_colecao(self, nome_colecao: str) -> Optional[Colecao]:
        """ Busca e retorna uma coleção específica pelo nome. """
        for colecao in self._colecoes:
            if colecao.nome.lower() == nome_colecao.lower():
                return colecao
        return None
    
    def __str__(self) -> str:
        """Representação em texto do usuário."""
        return f"Usuário: {self.nome} ({self.email}) - {len(self._colecoes)} coleção(ões)"