""" classe base |Jogo| e suas Subclasses. """

class jogo: 
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

    def atualizar_progresso(self, horas: float) -> None:
        """Soma horas jogadas e permite atualizar o status do Jogo."""
        pass 

    def reiniciar(self) -> None:
        """Permite zerar as horas e mudar status para "JOGANDO"""
        pass 

    def avaliar(self, nota: float) -> None:
        """Permite avaliar quando o jogo está "FINALIZADO"""
        pass 

class JogoCampanha: 
    """
    Destinado para jogos de modo história.

    atributos adicionais:
    capitulos_concluidos (int): quantidade de capítulos concluídos.
    percentual_conclusao (float): progresso em porcentagem da história.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str):
        self.capitulos_concluidos = 0 
        self.percentual_conclusao = 0.0 
        super().__init__(titulo, genero, plataforma) 

class JogoCompetitivo: 
    """
    Subclasse destinado para jogos de pvp e rankeadas.

    atributos adicionais:
    partidas_jogadas (int): Total de partidas disputadas.
    vitorias (int): Total de vitórias obtidas.
    derrotas (int): Total de derrotas obtidas.
    ranking (str): Divisão atual no jogo (ouro, diamante...).
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, ranking: str = "Unranked"): # parâmetro opicional. SE não é informado ranking == Unranked (sem rank)
        self.partidas_jogadas = 0
        self.vitorias = 0
        self.derrotas = 0
        self.ranking = ranking
        super().__init__(titulo, genero, plataforma)

    def taxa_vitoria(self) -> float:
        """Calcula e retorna a porcentagem de vitória de um jogador."""
        pass

class JogoCooperativo: 
    """
    Destindo a jogos de trabalho em equipe.

    Atributos adicionais:
    sessoes_cooperativas (int): Quantidades de sessões jogadas em equipe.
    max_jogadores (int): Quantidade máxima de jogadores por partidas.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadores: int):
        self.sessoes_cooperativas = 0 
        self.max_jogadores = max_jogadores
        super().__init__(titulo,genero,plataforma)

class JogoCampanhaCoop: 
    """
    Destinado a jogos de trabalho em equipe junto a modo campanha
    
    Atributos adicionais:
    modo_progresso_compartilhado (bool): Se o progresso salva para todos.
    """

    def __init__(self, titulo: str, genero: str, plataforma: str, max_jogadoress: int, progresso_compartilhado: bool = True): # se não for informado que o jogo fica salvo para os dois jogadores, retorna True
        # inicializa as duas classes pai:
        self.JogoCampanha.__init__(self,titulo, genero, plataforma)
        self.jogoCooperativo.__init__(self, titulo, genero, plataforma, max_jogadoress)
        self.modo_progresso_compartilhado = progresso_compartilhado

    def resumo_coop(self) -> str:
        """retorna um resumo combinando os dados da campanha e do cooperativo"""
        pass 