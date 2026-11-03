""" Tratamento dos comandos do módulo 'colecao'. """
from rich.panel import Panel

from src.models.colecao import Colecao
from src.cli.exibicao import console, mostrar_colecoes_disponiveis, renderizar_tabela_jogos
from src.cli.auxiliares import buscar_colecao, colecao_ou_erro
from src.utils.persistencia import salvar_colecoes


def _criar(args, colecoes, config) -> None:
    if buscar_colecao(colecoes, args.nome.strip()):
        console.print(Panel(f"[bold red]❌ A coleção '{args.nome}' já existe.[/bold red]", border_style="red"))
        return

    nova_col = Colecao(args.nome)
    colecoes.append(nova_col)
    salvar_colecoes(colecoes)
    console.print(Panel(f"[bold green]✅ Coleção '{nova_col.nome}' criada e salva com sucesso![/bold green]", border_style="green"))


def _listar(args, colecoes, config) -> None:
    if not colecoes:
        console.print(Panel("[yellow]ℹ️ Nenhuma coleção cadastrada no momento.[/yellow]", border_style="yellow"))
        return

    for c in colecoes:
        console.print(f"\n [bold cyan]Coleção:[/bold cyan] {c.nome} [dim]({c.total_jogos()} jogo(s), {c.total_horas_jogadas():.1f}h)[/dim]")
        if args.detalhada:
            renderizar_tabela_jogos(c.nome, c.listar_jogos())


def _ver(args, colecoes, config) -> None:
    if not args.nome:
        mostrar_colecoes_disponiveis(colecoes)
        return

    col = colecao_ou_erro(colecoes, args.nome)
    if col:
        renderizar_tabela_jogos(col.nome, col.listar_jogos())


def _remover(args, colecoes, config) -> None:
    if args.nome.lower() in ["geral", "favoritos"]:
        console.print(Panel(f"[bold red]❌ A coleção '{args.nome}' é uma coleção padrão do sistema e não pode ser removida.[/bold red]", border_style="red"))
        return

    col = colecao_ou_erro(colecoes, args.nome)
    if col:
        colecoes.remove(col)
        salvar_colecoes(colecoes)
        console.print(Panel(f"[bold green] Coleção '{args.nome}' removida com sucesso![/bold green]", border_style="green"))


def _adicionar_jogo(args, colecoes, config) -> None:
    destino = colecao_ou_erro(colecoes, args.nome)
    if not destino:
        return

    geral = buscar_colecao(colecoes, "Geral")
    jogo = geral.buscar_por_titulo(args.titulo) if geral else None # 'Geral' guarda todos os jogos cadastrados
    if not jogo:
        console.print(Panel(f"[bold red]❌ Jogo '{args.titulo}' não está cadastrado.[/bold red]", border_style="red"))
        if geral:
            renderizar_tabela_jogos(geral.nome, geral.listar_jogos())
        return

    try:
        destino.adicionar_jogo(jogo) # usa o mesmo objeto: atualizar em uma coleção atualiza em todas
        salvar_colecoes(colecoes)
        console.print(Panel(f"[bold green]✅ '{jogo.titulo}' adicionado à coleção '{destino.nome}'.[/bold green]", border_style="green"))
    except (ValueError, TypeError) as e:
        console.print(Panel(f"[bold red]❌ Erro ao adicionar à coleção:[/bold red] {e}", border_style="red"))


def _filtrar(args, colecoes, config) -> None:
    col = colecao_ou_erro(colecoes, args.nome)
    if not col:
        return

    if args.status:
        filtrados = col.filtrar_por_status(args.status)
    elif args.genero:
        filtrados = col.filtrar_por_genero(args.genero)
    elif args.plataforma:
        filtrados = col.filtrar_por_plataforma(args.plataforma)
    elif args.nota_minima is not None:
        filtrados = col.filtrar_por_nota_minima(args.nota_minima)
    elif args.busca:
        filtrados = col.buscar_por_parte_do_titulo(args.busca)
    else:
        filtrados = col.listar_jogos()

    renderizar_tabela_jogos(f"{col.nome} (Filtrada)", filtrados)


def _ordenar(args, colecoes, config) -> None:
    col = colecao_ou_erro(colecoes, args.nome)
    if not col:
        return

    # cada critério aponta para o método de ordenação da Colecao
    criterios = {
        "titulo": col.ordenar_por_titulo,
        "horas": col.ordenar_por_horas,
        "avaliacao": col.ordenar_por_avaliacao,
        "ano": col.ordenar_por_ano,
    }
    ordenados = criterios[args.criterio]()
    renderizar_tabela_jogos(f"{col.nome} (Ordenada por {args.criterio.upper()})", ordenados)


ACOES = {
    "criar": _criar,
    "listar": _listar,
    "ver": _ver,
    "remover": _remover,
    "adicionar-jogo": _adicionar_jogo,
    "filtrar": _filtrar,
    "ordenar": _ordenar,
}


def tratar_colecao(args, colecoes, config) -> None:
    """Chama a função correspondente à ação escolhida."""
    ACOES[args.acao](args, colecoes, config)