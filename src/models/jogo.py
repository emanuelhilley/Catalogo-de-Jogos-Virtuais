""" Classe base |Jogo| e suas Subclasses. """
from datetime import date
from typing import Optional
from src.models.excecoes import (
    TituloInvalidoError,
    HorasInvalidasError,
    StatusInvalidoError,
    AvaliacaoInvalidaError
)

STATUS_VALIDOS = ("NÃO INICIADO", "JOGANDO", "FINALIZADO")
HORAS_MINIMAS_FINALIZAR = 1.0 # mínimo de horas registradas para poder finalizar um jogo

class Jogo: 
    """ classe que representa um jogo genérico no catágolo

    atributos da Classe Jogo:
    titulo (str): Nome do jogo (não pode ser vazio).
    genero (str): Gênero Principal (ex: RPG, FPS, Ação)
    plataforma (str): Plataforma em que o jogo é jogado (PC, Console, Mobile)
    status (str): Estado atual ("NÃO INICIADO", "JOGANDO", "FINALIZADO")
    horas_jogadas (float): Total de horas acumuladas de jogo (>= 0)
    avaliacao (float): Nota dada ao jogo de 0 a 10 (apenas se FINALIZADO)
    ano_lancamento (int): Ano em que o jogo foi lançado (opcional).
    data_inicio (date): Data em que o jogo começou a ser jogado (opcional).
    data_termino (date): Data em que o jogo foi finalizado (opcional).
    """
    def __init__(self, titulo: str, genero: str,plataforma: str):
        """inicializa os atributos básicos de um jogo."""
        self.titulo = titulo # usa o setter para validar
        self.genero = genero         
        self.plataforma = plataforma 
        self._status = "NÃO INICIADO" 
        self._horas_jogadas = 0.0    
        self._avaliacao = None  
        self.ano_lancamento: Optional[int] = None
        self.data_inicio: Optional[date] = None
        self.data_termino: Optional[date] = None

    # ENCAPSULAMENTO

    @property
    def titulo(self) -> str:
        """Getter: Retorna o título do jogo."""
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        """Setter: Valida se o título não está vazio."""
        if not isinstance(valor, str) or not valor.strip():
            raise TituloInvalidoError("O título do jogo não pode ser vazio.")
        self._titulo = valor.strip()

    @property
    def status(self) -> str:
        """Getter: Retorna o status atual do jogo."""
        return self._status

    @status.setter
    def status(self, valor: str) -> None:
        """Setter: Valida se o status é um dos três permitidos."""
        if isinstance(valor, str):
            valor = valor.upper()
        if valor not in STATUS_VALIDOS:
            raise StatusInvalidoError(f"Status inválido: '{valor}'. Use: {', '.join(STATUS_VALIDOS)}.")
        self._status = valor

    @property 
    def horas_jogadas(self) -> float:
        """Getter: Retorna o total de horas jogadas."""
        return self._horas_jogadas

    @horas_jogadas.setter
    def horas_jogadas(self, valor: float) -> None:
        """Setter: Valida se as horas são maiores ou iguais a 0."""
        if valor < 0:
            raise HorasInvalidasError("O total de horas jogadas não pode ser negativo")
        self._horas_jogadas = valor    

    @property
    def avaliacao(self) -> float | None:
       """Getter: Retorna a avaliação do jogo. """
       return self._avaliacao

    @avaliacao.setter
    def avaliacao(self,nota:float) -> None:
        """Setter: Valida se o jogo está finalizado e se a nota está entre 0 e 10."""
        if self.status != "FINALIZADO":
            raise AvaliacaoInvalidaError("Apenas jogos com o status 'FINALIZADO' podem ser avaliados.") # dispara um erro customizado se não seguir as normas
        if not (0.0 <= nota <= 10):
            raise AvaliacaoInvalidaError("A nota deve estar entre 0.0 e 10.0.")
        self._avaliacao = nota

    # -=-=-= MÉTODOS DE NEGÓCIOS -=-=-=
        
    def atualizar_progresso(self, horas: float) -> None:
        """Soma horas jogadas e altera o status para 'JOGANDO' se estiver em 'NÃO INICIADO'"""
        if horas <= 0:
            raise HorasInvalidasError("Não pode atribuir um número negativo! As horas devem ser maiores que zero.")

        self.horas_jogadas += horas # usa o setter para validar
        if self.status == "NÃO INICIADO":
            self.status = "JOGANDO"
            self.data_inicio = date.today() # registra o dia em que começou a jogar

    def finalizar(self) -> None:
        """Marca o jogo como 'FINALIZADO'. Só é permitido se tiver pelo menos 1h registrada."""
        if self.horas_jogadas < HORAS_MINIMAS_FINALIZAR:
            raise StatusInvalidoError(
                f"Não é possível finalizar '{self.titulo}': é necessário ter pelo menos "
                f"{HORAS_MINIMAS_FINALIZAR}h registrada (atual: {self.horas_jogadas:.1f}h)."
            )
        self.status = "FINALIZADO"
        self.data_termino = date.today() # registra o dia em que terminou
        if self.data_inicio is None:
            self.data_inicio = self.data_termino
        
    def reiniciar(self) -> None:
        """Permite zerar as horas e mudar status para "JOGANDO"""
        self._horas_jogadas = 0.0
        self._avaliacao = None
        self.status = "JOGANDO" 
        self.data_inicio = date.today()
        self.data_termino = None

    def avaliar(self, nota: float) -> None:
        """Atribui nota ao jogo (chama o setter de avaliação)."""
        self.avaliacao = nota 

    # -=-=-= MÉTODOS ESPECIAIS -=-=-=-=

    def __str__(self) -> str:
        """Define a representação em texto do jogo para 'print'"""
        nota_txt = f"{self.avaliacao}/10" if self.avaliacao is not None else "Sem nota."
        return f"{self.titulo} [{self.plataforma}] - {self.genero} | Status: {self.status} | Horas: {self.horas_jogadas}h | Nota:  {nota_txt}"

    def __repr__(self) -> str:
        """Define a exibição detalhada do jogo (útil para debug)."""
        return (
            f"{self.__class__.__name__}(titulo={self.titulo!r}, genero={self.genero!r}, "
            f"plataforma={self.plataforma!r}, status={self.status!r}, "
            f"horas_jogadas={self.horas_jogadas}, avaliacao={self.avaliacao})"
        )

    def __eq__(self, outro_objeto: object) -> bool:
        """Confere se dois jogos são os mesmos através do título e plataforma."""
        if not isinstance(outro_objeto, Jogo): # 'isinstance' para verificar se o objeto em '__eq__' é de fato um jogo e não uma outra coisa qualquer.
           return False
        return (
            self.titulo.lower() == outro_objeto.titulo.lower()
            and self.plataforma.lower() == outro_objeto.plataforma.lower()
        )

    def __hash__(self) -> int:
        """Necessário porque ao definir o '__eq__' o Python deixa de gerar o hash do objeto automaticamente."""
        return hash((self.titulo.lower(), self.plataforma.lower()))

    def __lt__(self, outro_objeto: "Jogo") -> bool:
        """Permite comparar dois jogos com '<' (ordenação por horas jogadas)."""
        if not isinstance(outro_objeto, Jogo):
            return NotImplemented
        return self.horas_jogadas < outro_objeto.horas_jogadas

# -=-=-= MIXINS (HERANÇA MÚLTIPLA) -=-=-=

class CampanhaMixin:
    """
    Mixin com os recursos de modo história.

    Atributos adicionais:
        capitulos_concluidos (int): Quantidade de capítulos finalizados.
        percentual_conclusao (float): Progresso em percentual da história (0 a 100%).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # repassa os argumentos pela cadeia de super() até chegar na classe Jogo
        self.capitulos_concluidos = 0
        self.percentual_conclusao = 0.0


class CooperativoMixin:
    """
    Mixin com os recursos de trabalho em equipe.

    Atributos adicionais:
        sessoes_cooperativas (int): Quantidade de sessões jogadas em grupo.
        max_jogadores (int): Limite máximo de jogadores por partida.
        participantes_frequentes (list[str]): Nomes dos jogadores que mais jogam junto.
    """

    def __init__(self, *args, max_jogadores: int = 4, **kwargs): # max_jogadores é nomeado para não se perder na cadeia de super()
        super().__init__(*args, **kwargs)
        self.sessoes_cooperativas = 0
        self.max_jogadores = max_jogadores
        self.participantes_frequentes: list[str] = []

    def adicionar_participante(self, nome: str) -> None:
        """Adiciona um jogador à lista de participantes frequentes (sem repetir nomes)."""
        if nome and nome not in self.participantes_frequentes:
            self.participantes_frequentes.append(nome)

# -=-=-= SUBCLASSES POR ESTILO DE JOGO -=-=-=

class JogoCampanha(CampanhaMixin, Jogo):
    """
    Destinado para jogos de modo história.
    (os atributos capitulos_concluidos e percentual_conclusao vêm do CampanhaMixin)
    """


class JogoCompetitivo(Jogo):
    """
    Subclasse destinado para jogos de pvp e rankeadas.

    Atributos adicionais:
        partidas_jogadas (int): Total de partidas disputadas.
        vitorias (int): Total de vitórias obtidas.
        derrotas (int): Total de derrotas obtidas.
        ranking (str): Elo ou divisão atual no jogo (ex: "Ouro", "Radiante").
        """

    def __init__(self, titulo: str, genero: str, plataforma: str, ranking: str = "Unranked"): # parâmetro opicional. SE não é informado ranking == Unranked (sem rank)
        super().__init__(titulo, genero, plataforma)
        self.partidas_jogadas = 0
        self.vitorias = 0
        self.derrotas = 0
        self.ranking = ranking


    def taxa_vitoria(self) -> float:
        """Calcula e retorna a porcentagem de vitória de um jogador."""
        if self.partidas_jogadas == 0:
            return 0.0
        return (self.vitorias / self.partidas_jogadas) * 100

class JogoCooperativo(CooperativoMixin, Jogo):
    """
    Destindo a jogos de trabalho em equipe.
    (os atributos sessoes_cooperativas, max_jogadores e participantes_frequentes vêm do CooperativoMixin)
        """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadores: int):
        super().__init__(titulo, genero, plataforma, max_jogadores=max_jogadores)


class JogoCampanhaCoop(CampanhaMixin, CooperativoMixin, Jogo):
    """
    Destinado a jogos de trabalho em equipe junto a modo campanha

    Atributos adicionais:
    modo_progresso_compartilhado (bool): Se o progresso salva para todos.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadores: int, progresso_compartilhado: bool = True): # se não for informado que o jogo fica salvo para os dois jogadores, retorna True
        # um único super() percorre toda a cadeia (MRO): CampanhaMixin -> CooperativoMixin -> Jogo
        super().__init__(titulo, genero, plataforma, max_jogadores=max_jogadores)
        self.modo_progresso_compartilhado = progresso_compartilhado

    def resumo_coop(self) -> str:
        """retorna um resumo combinando os dados da campanha e do cooperativo"""
        return f"Capítulos: {self.capitulos_concluidos} | Progresso: {self.percentual_conclusao}% | Grupo Max: {self.max_jogadores} jogadores."

class JogoPc(Jogo):
    """
    Destinado para jogos de PC.
    
    Atributos adicionais:
        requisitos_minimos (str): Especificações técnicas mínimas exigidas.
        loja_digital (str): Loja onde o jogo foi adquirido (ex: "Steam", "Epic Games").
        """
    def __init__(self, titulo: str, genero: str, requisitos_minimos: str, loja_digital : str= "steam"):
        super().__init__(titulo, genero, plataforma= "PC")
        self.requisitos_minimos = requisitos_minimos
        self.loja_digital = loja_digital

class JogoConsole(Jogo):
    """
    Destinado para jogos de Console
    
    Atributos adicionais:
        nome_console (str): Nome da consola (ex: "PlayStation 5", "Xbox Series X").
        midia_fisica (bool): Indica se o jogo é em disco/cartucho físico.
        """
    def __init__(self, titulo: str, genero: str, nome_console: str, midia_fisica: bool = False):
        super().__init__(titulo,genero, plataforma= nome_console)
        self.nome_console = nome_console
        self.midia_fisica = midia_fisica

class JogoMobile(Jogo):
    """
    Destinado para jogos mobiles.
    
    Atributos adicionais:
        tamanho_mb (float): Tamanho de armazenamento do jogo em Megabytes.
        compras_no_app (bool): Indica se o jogo possui microtransações.
        """
    def __init__(self, titulo: str, genero: str, tamanho_mb: float, compras_no_app: bool = True ):
        super().__init__(titulo, genero, plataforma="Mobile")
        self.tamanho_mb = tamanho_mb
        self.compras_no_app = compras_no_app