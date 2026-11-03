""" Funções auxiliares para achar coleções e jogos (mostram o erro na tela se não encontrarem). """
from typing import Optional
from rich.panel import Panel

from src.models.colecao import Colecao
from src.models.jogo import Jogo
from src.cli.exibicao import console, mostrar_colecoes_disponiveis, renderizar_tabela_jogos


def buscar_colecao(colecoes: list[Colecao], nome: str) -> Optional[Colecao]:
    """Busca uma coleção pelo nome (sem diferenciar maiúsculas de minúsculas)."""
    return next((c for c in colecoes if c.nome.lower() == nome.lower()), None)


def colecao_ou_erro(colecoes: list[Colecao], nome: str) -> Optional[Colecao]:
    """Retorna a coleção. Se não existir, mostra o erro e as coleções disponíveis e retorna None."""
    colecao = buscar_colecao(colecoes, nome)
    if not colecao:
        console.print(Panel(f"[bold red]❌ Coleção '{nome}' não encontrada.[/bold red]", border_style="red"))
        mostrar_colecoes_disponiveis(colecoes)
    return colecao


def jogo_ou_erro(colecao: Colecao, titulo: str) -> Optional[Jogo]:
    """Retorna o jogo. Se não existir na coleção, mostra o erro e a tabela de jogos e retorna None."""
    jogo = colecao.buscar_por_titulo(titulo)
    if not jogo:
        console.print(Panel(f"[bold red]❌ Jogo '{titulo}' não foi encontrado na coleção '{colecao.nome}'.[/bold red]", border_style="red"))
        renderizar_tabela_jogos(colecao.nome, colecao.listar_jogos())
    return jogo