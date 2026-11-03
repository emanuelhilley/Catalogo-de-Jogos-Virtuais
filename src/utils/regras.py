""" Regras de negócio que dependem do catálogo inteiro e do settings.json. """
from typing import Optional
from src.models.colecao import Colecao
from src.models.jogo import Jogo
from src.models.excecoes import LimiteJogandoError

def _jogos_unicos(colecoes: list[Colecao]) -> list[Jogo]:
    """Reúne os jogos de todas as coleções. Um jogo que está em várias coleções conta só uma vez."""
    unicos = {}
    for col in colecoes:
        for jogo in col.listar_jogos():
            unicos[(jogo.titulo.lower(), jogo.plataforma.lower())] = jogo # a chave (título + plataforma) evita repetir o mesmo jogo
    return list(unicos.values())

def contar_jogando(colecoes: list[Colecao]) -> int:
    """Conta quantos jogos do catálogo estão com o status 'JOGANDO'."""
    return sum(1 for jogo in _jogos_unicos(colecoes) if jogo.status == "JOGANDO")

def contar_finalizados(colecoes: list[Colecao]) -> int:
    """Conta quantos jogos do catálogo estão com o status 'FINALIZADO'."""
    return sum(1 for jogo in _jogos_unicos(colecoes) if jogo.status == "FINALIZADO")

def verificar_limite_jogando(colecoes: list[Colecao], limite: int) -> None:
    """
    Garante que não passe do limite de jogos simultâneos com status 'JOGANDO'.

    Levanta LimiteJogandoError se já houver 'limite' jogos sendo jogados.
    O limite vem do settings.json (padrão: 3).
    """
    if contar_jogando(colecoes) >= limite:
        raise LimiteJogandoError(
            f"Limite de {limite} jogos simultâneos com status 'JOGANDO' atingido. "
            "Finalize algum jogo antes de iniciar outro."
        )

def aviso_meta(colecoes: list[Colecao], meta: int) -> Optional[str]:
    """
    Retorna um texto de aviso se o total de finalizados for menor que a meta anual.
    Retorna None se a meta foi atingida (ou se não há meta definida).
    """
    if meta <= 0:
        return None

    finalizados = contar_finalizados(colecoes)
    if finalizados < meta:
        return f" Meta anual: {finalizados}/{meta} jogos finalizados (faltam {meta - finalizados})."
    return None