""" Classe base |Jogo| e suas Subclasses. """

class Jogo: 
    """ classe que representa um jogo genérico no catágolo

    atributos da Classe Jogo:
    titulo (str): Nome do jogo.
    genero (str): Gênero Principal (ex: RPG, FPS, Ação)
    plataforma (str): Plataforma em que o jogo é jogado (PC, Console, Mobile)
    status (str): Estado atual ("NÃO INICIADO", "JOGANDO", "FINALIZADO")
    horas_jogadas (float): Total de horas acumuladas de jogo (>= 0)
    avaliacao (float): Nota dada ao jogo de 0 a 10 (apenas se FINALIZADO)
    """
    def __init__(self, titulo: str, genero: str,plataforma: str):
        """inicializa os atributos básicos de um jogo."""
        self.titulo = titulo         
        self.genero = genero         
        self.plataforma = plataforma 
        self.status = "NÃO INICIADO" 
        self._horas_jogadas = 0.0    
        self._avaliacao = None  

    # ENCAPSULAMENTO

    @property 
    def horas_jogadas(self) -> float:
        """Getter: Retorna o total de horas jogadas."""
        return self._horas_jogadas

    @horas_jogadas.setter
    def horas_jogadas(self, valor: float) -> None:
        """Setter: Valida se as horas são maiores ou iguais a 0."""
        if valor < 0:
            raise ValueError("O total de horas jogadas não pode ser negativo")
        self._horas_jogadas = valor    

    @property
    def avaliacao(self) -> float | None:
       """Getter: Retorna a avaliação do jogo. """
       return self._avaliacao

    @avaliacao.setter
    def avaliacao(self,nota:float) -> None:
        """Setter: Valida se o jogo está finalizado e se a nota está entre 0 e 10."""
        if self.status != "FINALIZADO":
            raise ValueError("Apenas jogos com o status 'FINALIZADO' podem ser avaliados.") # 'raise valueError' para disparar um erro se não seguir as normas
        if not (0.0 <= nota <= 10):
            raise ValueError("A nota deve estar entre 0.0 e 10.0.")
        self._avaliacao = nota

    # -=-=-= MÉTODOS DE NEGÓCIOS -=-=-=
        
    def atualizar_progresso(self, horas: float) -> None:
        """Soma horas jogadas e altera o status para 'JOGANDO' se estiver em 'NÃO INICIADO'"""
        if horas <= 0:
            raise ValueError("Não pode atriubir um número negativo! As horas devem ser maiores que zero.")

        self.horas_jogadas += horas # usa o setter para validar
        if self.status == "NÃO INICIADO":
            self.status = "JOGANDO"
        
    def reiniciar(self) -> None:
        """Permite zerar as horas e mudar status para "JOGANDO"""
        self._horas_jogadas = 0.0
        self._avaliacao = None
        self.status = "JOGANDO" 

    def avaliar(self, nota: float) -> None:
        """Atribui nota ao jogo (chama o setter de avaliação)."""
        self.avaliacao = nota 

    # -=-=-= MÉTODOS ESPECIAIS -=-=-=-=

    def __str__(self) -> str:
        """Define a representação em texto do jogo para 'print'"""
        nota_txt = f"{self.avaliacao}/10" if self.avaliacao is not None else "Sem nota."
        return f"{self.titulo} [{self.plataforma}] - {self.genero} | Status: {self.status} | Horas: {self.horas_jogadas}h | Nota:  {nota_txt}"

    def __eq__(self, outro_objeto: object) -> bool:
        """Confere se dois jogos são os mesmos através do título e plataforma."""
        if not isinstance(outro_objeto, Jogo): # 'isinstance' para verificar se o objeto em '__eq__' é de fato um jogo e não uma outra coisa qualquer.
           return False
        return (
            self.titulo.lower() == outro_objeto.titulo.lower()
            and self.plataforma.lower() == outro_objeto.plataforma.lower()
        )

# -=-=-= SUBCLASSES POR ESTILO DE JOGO -=-=-=

class JogoCampanha(Jogo): 
    """
    Destinado para jogos de modo história.

    Atributos adicionais:
        capitulos_concluidos (int): Quantidade de capítulos finalizados.
        percentual_conclusao (float): Progresso em percentual da história (0 a 100%).
    """

    def __init__(self, titulo: str, genero: str, plataforma: str):
        super().__init__(titulo, genero, plataforma)
        self.capitulos_concluidos = 0 
        self.percentual_conclusao = 0.0 
         

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

class JogoCooperativo(Jogo): 
    """
    Destindo a jogos de trabalho em equipe.
    
    Atributos adicionais:
        sessoes_cooperativas (int): Quantidade de sessões jogadas em grupo.
        max_jogadores (int): Limite máximo de jogadores por partida.
        """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadores: int):
        super().__init__(titulo,genero,plataforma)
        self.sessoes_cooperativas = 0 
        self.max_jogadores = max_jogadores
        

class JogoCampanhaCoop(JogoCampanha,JogoCooperativo): 
    """
    Destinado a jogos de trabalho em equipe junto a modo campanha
    
    Atributos adicionais:
    modo_progresso_compartilhado (bool): Se o progresso salva para todos.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadores: int, progresso_compartilhado: bool = True): # se não for informado que o jogo fica salvo para os dois jogadores, retorna True
        # inicializa as duas classes pai:
        JogoCampanha.__init__(self,titulo, genero, plataforma)
        JogoCooperativo.__init__(self, titulo, genero, plataforma, max_jogadores)
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