""" Tratamento dos comandos do módulo 'usuario'. """
from rich.panel import Panel

from src.models.usuario import Usuario
from src.cli.exibicao import console
from src.utils.regras import aviso_meta
from src.utils.settings import salvar_settings
from src.utils.persistencia import salvar_usuario, carregar_usuario, resetar_catalogo


def _criar(args, colecoes, config) -> None:
    try:
        meta = args.meta if args.meta is not None else config["meta_anual_jogos"]
        usuario = Usuario(nome=args.nome, email=args.email, meta_jogos_ano=meta)
        salvar_usuario(usuario)
        config["meta_anual_jogos"] = usuario.meta_jogos_ano # a meta também fica registrada no settings.json
        salvar_settings(config)
        resetar_catalogo()

        console.print(Panel(
            f"[bold green]✅ Novo perfil de usuário criado com sucesso![/bold green]\n\n"
            f" [bold]Nome:[/bold] {usuario.nome}\n"
            f" [bold]E-mail:[/bold] {usuario.email}\n"
            f" [bold]Meta Anual:[/bold] {usuario.meta_jogos_ano} jogos\n\n"
            f" [bold yellow]O catálogo foi resetado. Coleções 'Geral' e 'Favoritos' prontas para o novo usuário.[/bold yellow]",
            title="Novo Usuário Configurado", border_style="green"
        ))
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Erro de validação:[/bold red] {e}", border_style="red"))


def _atualizar(args, colecoes, config) -> None:
    usuario_atual = carregar_usuario()
    if not usuario_atual:
        console.print(Panel("[bold red]❌ Nenhum usuário cadastrado para atualizar. Crie um com 'usuario criar'.[/bold red]", border_style="red"))
        return

    nome = args.nome if args.nome is not None else usuario_atual.nome
    email = args.email if args.email is not None else usuario_atual.email
    meta = args.meta if args.meta is not None else config["meta_anual_jogos"]

    try:
        usuario_atualizado = Usuario(nome=nome, email=email, meta_jogos_ano=meta)
        salvar_usuario(usuario_atualizado)
        config["meta_anual_jogos"] = usuario_atualizado.meta_jogos_ano
        salvar_settings(config)
        console.print(Panel(
            f"[bold green]✅ Perfil atualizado com sucesso![/bold green]\n\n"
            f" [bold]Nome:[/bold] {usuario_atualizado.nome}\n"
            f" [bold]E-mail:[/bold] {usuario_atualizado.email}\n"
            f" [bold]Meta Anual:[/bold] {usuario_atualizado.meta_jogos_ano} jogos\n\n"
            f" [dim]Seus jogos e coleções anteriores foram mantidos.[/dim]",
            title="Perfil Atualizado", border_style="green"
        ))
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Erro de validação:[/bold red] {e}", border_style="red"))


def _ver(args, colecoes, config) -> None:
    usuario = carregar_usuario()
    if not usuario:
        console.print(Panel("[yellow]ℹ️ Nenhum perfil encontrado. Crie um com: python3 main.py usuario criar --nome ... --email ...[/yellow]", border_style="yellow"))
        return

    console.print(Panel(
        f" [bold]Nome:[/bold] {usuario.nome}\n"
        f" [bold]E-mail:[/bold] {usuario.email}\n"
        f" [bold]Meta Anual:[/bold] {config['meta_anual_jogos']} jogo(s)\n"
        f" [bold]Total de Coleções:[/bold] {len(colecoes)}",
        title="Perfil do Usuário", border_style="cyan"
    ))


def _meta(args, colecoes, config) -> None:
    usuario = carregar_usuario()
    if not usuario:
        console.print(Panel("[bold red]❌ Crie um perfil primeiro com 'usuario criar'.[/bold red]", border_style="red"))
        return

    usuario._colecoes = colecoes
    usuario.meta_jogos_ano = config["meta_anual_jogos"] # a meta vem do settings.json
    prog = usuario.progresso_meta()
    status_meta = "[bold green]Sim 🎉[/bold green]" if prog['atingida'] else "[bold yellow]Não ⏳[/bold yellow]"

    console.print(Panel(
        f" [bold]Meta Definida:[/bold] {prog['meta']} jogo(s)\n"
        f" [bold]Jogos Finalizados:[/bold] {prog['finalizados']}\n"
        f" [bold]Progresso:[/bold] {prog['percentual']}%\n"
        f" [bold]Meta Atingida:[/bold] {status_meta}",
        title="Progresso da Meta Anual", border_style="magenta"
    ))

    aviso = aviso_meta(colecoes, config["meta_anual_jogos"])
    if aviso:
        console.print(Panel(aviso, title="Aviso de Meta", border_style="yellow"))


ACOES = {"criar": _criar, "atualizar": _atualizar, "ver": _ver, "meta": _meta}


def tratar_usuario(args, colecoes, config) -> None:
    """Chama a função correspondente à ação escolhida (criar, atualizar, ver ou meta)."""
    ACOES[args.acao](args, colecoes, config)