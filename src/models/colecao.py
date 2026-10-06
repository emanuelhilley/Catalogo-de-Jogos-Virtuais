""" Organização e gerenciamento da lista de jogos (CRUD)."""
from typing import List, Optional
from src.models.jogo import Jogo

class Colecao: 
    """ lista personalida do usuário """
    def __init__(self,nome: str):
        self.nome = nome  
        """ guarda o nome da lista """
        self._jogos: List[Jogo] = [] 
        """ lista vazia que vai guardar os jogos """

    # -=-=-= ENCAPSULAMENTO (@property) -=-=-=

    @property
    def jogos(self) -> List[Jogo]:
        """Getter: Retorna uma cópia da lista de jogos para proteger o atributo interno."""
        return self._jogos.copy()

    # -=-=-= MÉTODOS CRUD -=-=-=

    def adicionar_jogo(self, jogo: Jogo) -> None: 
        """ 
        Adiciona um objeto Jogo à coleção (Create).

        Levanta ValueError se o jogo já existir na coleção (baseado no __eq__).
        """
        if not isinstance(jogo,Jogo):
            raise TypeError("O objeto a ser adicionado deve ser do tipo jogo.")

        if jogo in self._jogos:
            raise ValueError(f"O jogo '{jogo.titulo}' já está presente na coleção.")

        self._jogos.append(jogo)

    def remover_jogo(self, titulo: str) -> bool: 
        """ 
        Remove um jogo buscando pelo seu título. 
        Retorna True se removido com sucesso, retorna False se não encontrar o jogo. 
        """
        jogo_encontrado = self.buscar_por_titulo(titulo)
        if jogo_encontrado:
            self._jogos.remove(jogo_encontrado)
            return True
        return False

    def listar_jogos(self) -> List[Jogo]: # read
        """ retorna todos os jogos guardados na coleção """
        return self.jogos


    def buscar_por_titulo(self, titulo:str) -> Optional[Jogo]:
        # Utilizar o Optinal para quando buscar um jogo pelo título, a função retornar um objeto do tipo Jogo (se ele for encontrado na lista) ou vai retornar None (se o jogo não existir na coleção).
        """Busca e retorna um jogo específico na coleção pelo título."""
        for jogo in self._jogos:
            if jogo.titulo.lower() == titulo.lower():
                return jogo
        return None


    def atualizar_jogo(self, titulo:str, **kwargs) -> bool: 
        # **kwargs permite que passe qualquer quantidade de alterações de uma só vez, sem precisares criar uma função para cada tipo de alteração.
        """
        Atualiza os dados de um jogo existente na coleção buscando pelo título.
        Retorna True se atualizado com sucesso, retorna False se não tiver encontrado o jogo.
        """
        jogo = self.buscar_por_titulo(titulo)
        if not jogo:
            return False
        for atributo, valor in kwargs.items():
            if hasattr(jogo, atributo):
                setattr(jogo, atributo, valor)
            else:
                raise AttributeError(f"O jogo não possui o atributo {atributo}.")
        return True

    # -=-=-= MÉTODOS ESPECIAIS E ESTATÍSTICAS -=-=-=

    def total_jogos(self) -> int:
        """Retorna o total de jogos na coleção."""
        return len(self._jogos)

    def total_horas_jogadas(self) -> float:
        """Retorna o total de horas jogadas da coleção."""
        return sum(jogo.horas_jogadas for jogo in self._jogos)

    def __str__(self) -> str:
        """Representação em texto da coleção."""
        return f"Coleção '{self.nome}' com {self.total_jogos()} jogo(s)."