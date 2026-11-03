""" Funções de exibição no terminal (tabelas e textos com Rich). """
from rich.console import Console
from rich.table import Table

from src.models.jogo import (
    Jogo, JogoCampanha, JogoCompetitivo, JogoCooperativo, JogoCampanhaCoop
)

console = Console()

# ==================== MODOS DE JOGO (classes do jogo.py) ====================

NOMES_MODO = {
    JogoCampanha: "Campanha",
    JogoCompetitivo: "Competitivo",
    JogoCooperativo: "Cooperativo",
    JogoCampanhaCoop: "Campanha + Coop",
}


def nome_modo(jogo: Jogo) -> str:
    """Nome amigável do modo, deduzido da classe do objeto. Jogo base e classes de plataforma = 'Padrão'."""
    return NOMES_MODO.get(type(jogo), "Padrão")


def detalhes_modo(jogo: Jogo) -> list[str]:
    """Linhas extras com os atributos específicos de cada modo (usadas no painel de confirmação)."""
    linhas = []
    if isinstance(jogo, JogoCompetitivo):
        linhas.append(f" [bold]Ranking:[/bold] {jogo.ranking}")
    if isinstance(jogo, JogoCooperativo):
        linhas.append(f" [bold]Máx. de Jogadores:[/bold] {jogo.max_jogadores}")
    if isinstance(jogo, JogoCampanhaCoop):
        compartilhado = "Sim" if jogo.modo_progresso_compartilhado else "Não"
        linhas.append(f" [bold]Progresso Compartilhado:[/bold] {compartilhado}")
    return linhas


def renderizar_tabela_jogos(nome_colecao: str, jogos: list):
    """Exibe uma tabela estilizada com os jogos de uma coleção usando Rich."""
    if not jogos:
        console.print(f"[yellow] A coleção '{nome_colecao}' está vazia ou não possui jogos no critério selecionado.[/yellow]")
        return

    table = Table(
        title=f"🎮 Jogos da Coleção: [bold cyan]{nome_colecao}[/bold cyan]",
        header_style="bold magenta",
        border_style="dim"
    )

    table.add_column("Título", style="bold white")
    table.add_column("Modo", style="bold cyan")
    table.add_column("Gênero", style="yellow")
    table.add_column("Plataforma", style="green")
    table.add_column("Ano", justify="right", style="dim")
    table.add_column("Status", style="bold blue")
    table.add_column("Horas", justify="right", style="cyan")
    table.add_column("Nota", justify="right", style="magenta")

    for j in jogos:
        if j.status == "FINALIZADO":
            status_formatted = f"[bold green]{j.status}[/bold green]"
        elif j.status == "JOGANDO":
            status_formatted = f"[bold yellow]{j.status}[/bold yellow]"
        else:
            status_formatted = f"[dim]{j.status}[/dim]"

        nota_str = f"{j.avaliacao:.1f}/10" if j.avaliacao is not None else "-"
        ano_str = str(j.ano_lancamento) if j.ano_lancamento is not None else "-"

        table.add_row(
            j.titulo,
            nome_modo(j),
            j.genero,
            j.plataforma,
            ano_str,
            status_formatted,
            f"{j.horas_jogadas:.1f}h",
            nota_str
        )

    console.print(table)


def mostrar_colecoes_disponiveis(colecoes: list):
    """Auxiliar para listar coleções e seus jogos no terminal."""
    if not colecoes:
        console.print("[yellow] Nenhuma coleção cadastrada no momento.[/yellow]")
        return

    table = Table(title="📁 Coleções e Jogos Disponíveis", header_style="bold cyan", border_style="dim")
    table.add_column("Nome da Coleção", style="bold white")
    table.add_column("Jogos", style="yellow")

    for c in colecoes:
        jogos_str = ", ".join([j.titulo for j in c.listar_jogos()]) or "(Sem jogos)"
        table.add_row(c.nome, jogos_str)

    console.print(table)