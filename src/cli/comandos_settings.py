""" Tratamento dos comandos do módulo 'settings'. """
from rich.panel import Panel

from src.cli.exibicao import console
from src.utils.settings import salvar_settings


def tratar_settings(args, colecoes, config) -> None:
    """Altera (se for 'definir') e exibe as configurações do settings.json."""
    if args.acao == "definir":
        if args.meta is not None:
            config["meta_anual_jogos"] = max(0, args.meta)
        if args.limite_jogando is not None:
            config["limite_jogando"] = max(1, args.limite_jogando) # o limite precisa ser de pelo menos 1 jogo
        if args.plataforma_principal:
            config["plataforma_principal"] = args.plataforma_principal
        if args.generos_favoritos is not None:
            config["generos_favoritos"] = [g.strip() for g in args.generos_favoritos.split(",") if g.strip()]
        salvar_settings(config)

    generos = ", ".join(config["generos_favoritos"]) or "(nenhum)"
    console.print(Panel(
        f" [bold]Gêneros Favoritos:[/bold] {generos}\n"
        f" [bold]Meta Anual de Jogos:[/bold] {config['meta_anual_jogos']}\n"
        f" [bold]Plataforma Principal:[/bold] {config['plataforma_principal']}\n"
        f" [bold]Limite de Jogos 'JOGANDO':[/bold] {config['limite_jogando']}",
        title="Configurações (settings.json)", border_style="cyan"
    ))