""" Fábrica que escolhe a classe certa de jogo conforme os argumentos da CLI. """
from src.models.jogo import (
    Jogo, JogoPc, JogoConsole, JogoMobile,
    JogoCampanha, JogoCompetitivo, JogoCooperativo, JogoCampanhaCoop
)


def nome_plataforma(args) -> str:
    """Texto da plataforma dos jogos criados por modo (mesmo padrão de JogoPc, JogoConsole e JogoMobile)."""
    if args.plataforma == "pc":
        return "PC"
    if args.plataforma == "console":
        return args.console
    if args.plataforma == "mobile":
        return "Mobile"
    return args.plataforma


def instanciar_jogo(args) -> Jogo:
    """Fábrica: escolhe a classe do jogo conforme o --modo. No modo 'padrao', a classe depende da --plataforma."""
    plataforma = nome_plataforma(args)

    if args.modo == "campanha":
        return JogoCampanha(args.titulo, args.genero, plataforma)
    if args.modo == "competitivo":
        return JogoCompetitivo(args.titulo, args.genero, plataforma, args.ranking)
    if args.modo == "cooperativo":
        return JogoCooperativo(args.titulo, args.genero, plataforma, args.max_jogadores)
    if args.modo == "campanhacoop":
        return JogoCampanhaCoop(args.titulo, args.genero, plataforma, args.max_jogadores, not args.progresso_individual)

    # modo padrão: a classe depende da plataforma
    if args.plataforma == "pc":
        return JogoPc(args.titulo, args.genero, args.requisitos, args.loja)
    if args.plataforma == "console":
        return JogoConsole(args.titulo, args.genero, args.console, args.midia_fisica)
    if args.plataforma == "mobile":
        return JogoMobile(args.titulo, args.genero, args.tamanho)

    return Jogo(args.titulo, args.genero, args.plataforma)