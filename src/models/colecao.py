""" Organização e gerenciamento da lista de jogos (CRUD)."""
from typing import Optional
from src.models.jogo import Jogo

class Colecao: 
    """ lista personalida do usuário """
    def __init__(self,nome: str):
        self.nome = nome  
        """ guarda o nome da lista """
        self._jogos: list[Jogo] = [] 
        """ lista vazia que vai guardar os jogos """

    # -=-=-= ENCAPSULAMENTO (@property) -=-=-=

    @property
    def jogos(self) -> list[Jogo]:
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

    def listar_jogos(self) -> list[Jogo]: # read
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
    
    # -=-=-=     FILTROS E ORDENAÇÕES    -=-=-=

    # Todos os três métodos de filtragem seguem a mesma lógica básica: 
    # criar uma lista vazia, percorrer os jogos um a um e guardar apenas os que correspondem ao critério.

    def filtrar_por_genero(self, genero: str) -> list[Jogo]:
        """Retorna apenas os jogos que pertencem ao gênero informado."""
        jogos_filtrados = []
        for jogo in self._jogos: # Percorre cada jogo salvo na coleção.
            if jogo.genero.lower() == genero.lower(): # Compara o gênero do jogo com o gênero buscado.
                jogos_filtrados.append(jogo)
        return jogos_filtrados # Devolve a lista final com os jogos filtrados.

    def filtrar_por_status(self, status: str) -> list[Jogo]:
        """Retorna os jogos filtrados pelo status (ex: 'NÃO INICIADO', 'JOGANDO', 'FINALIZADO')."""
        jogos_filtrados = []
        for jogo in self._jogos:
            if jogo.status.upper() == status.upper():
                jogos_filtrados.append(jogo)
        return jogos_filtrados

    def filtrar_por_plataforma(self, plataforma: str) -> list[Jogo]:
        """Retorna os jogos filtrados pela plataforma."""
        jogos_filtrados = []
        for jogo in self._jogos:
            if jogo.plataforma.lower() == plataforma.lower():
                jogos_filtrados.append(jogo)
        return jogos_filtrados

    def ordenar_por_titulo(self) -> list[Jogo]:
        """Retorna a lista de jogos ordenada alfabeticamente pelo título."""
        def obter_titulo(jogo):
            return jogo.titulo.lower() # recebe um jogo e extrai o seu título em letras minúsculas.

        return sorted(self._jogos, key=obter_titulo) # sorted() pega a lista _jogos e usa a função obter_titulo para comparar os títulos de cada jogo, retornando uma nova lista organizada em ordem alfabética

    def ordenar_por_horas(self, decrescente: bool = True) -> list[Jogo]:
        """Retorna a lista de jogos ordenada pela quantidade de horas jogadas."""
        def obter_horas(jogo):
            return jogo.horas_jogadas

        return sorted(self._jogos, key=obter_horas, reverse=decrescente)

    def ordenar_por_avaliacao(self, decrescente: bool = True) -> list[Jogo]:
        """Retorna a lista de jogos ordenada pela avaliação dada."""
        def obter_avaliacao(jogo):
            if jogo.avaliacao is not None:
                return jogo.avaliacao
            return 0.0

        return sorted(self._jogos, key=obter_avaliacao, reverse=decrescente)

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