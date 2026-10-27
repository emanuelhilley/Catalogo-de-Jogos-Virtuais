""" gerenciamento do perfil do usuário e suas coleções."""
from typing import Optional
from src.models.colecao import Colecao

class Usuario: 
    """ 
    representa o perfil do usuario e suas coleções pessoais.
    nome (str): nome ou apelido do jogador.
    email (str): O email do jogador.
    meta_jogos_ano: A meta de jogos por ano do jogador.
    colecoes (List[Colecao]): Lista das coleções criadas pelo usuário.
    """

    def __init__(self, nome: str, email:str, meta_jogos_ano: int = 0):
        """Inicializa o utilizador com nome, e-mail validado e lista de coleções."""
        self.nome = nome
        self.email = email # usa o setter para validar.
        self.meta_jogos_ano = max(0, meta_jogos_ano) # Garante que a meta de jogos nunca fica negativa logo na criação do objeto
        self._colecoes: list[Colecao] = []

# -=-=-= ENCAPSULAMENTO (@property) -=-=-=

    @property
    def meta_jogos_ano(self) -> int:
        return self._meta_jogos_ano

    @meta_jogos_ano.setter
    def meta_jogos_ano(self, valor: int) -> None:
     if valor < 0:
        raise ValueError("A meta de jogos por ano não pode ser negativa.")
     self._meta_jogos_ano = valor

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
    def colecoes(self) -> list[Colecao]:
        """Getter: Retorna uma cópia da lista de coleções.;"""
        return self._colecoes.copy()
    
# -=-=-=      REGRAS DE NEGÓCIO E METAS      -=-=-=

    def total_jogos_finalizados(self) -> int:
        """Conta quantos jogos das coleções foram finalizados."""
        total = 0
        for col in self._colecoes:
            total += len(col.filtrar_por_status("FINALIZADO"))
        return total

    def progresso_meta(self) -> dict:
        """Retorna as estatísticas do progresso em relação à meta anual."""
        finalizados = self.total_jogos_finalizados()
        if self._meta_jogos_ano > 0:
          atingida = finalizados >= self._meta_jogos_ano
          percentual = (finalizados / self._meta_jogos_ano) * 100
        else:
          atingida = False
          percentual = 0.0

        return {
            "meta": self._meta_jogos_ano,
            "finalizados": finalizados,
            "percentual": round(percentual, 1),
            "atingida": atingida
        }

# -=-=-= MÉTODOS DE GERENCIAMENTO DE COLEÇÕES -=-=-=

    def criar_colecao(self, nome_colecao: str) -> Colecao:
        """ instância que adiciona uma nova coleção para o perfil do usuário """
        if self.buscar_colecao(nome_colecao) is not None:
            raise ValueError(f"A coleção {nome_colecao} já existe.")

        nova_colecao = Colecao(nome_colecao)
        self._colecoes.append(nova_colecao)
        return nova_colecao
    
    def listar_colecoes(self) -> list[Colecao]:
        """Retorna a lista de todas as coleções do usuário."""
        return self.colecoes

    def remover_colecao(self, nome_colecao: str) -> bool:
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