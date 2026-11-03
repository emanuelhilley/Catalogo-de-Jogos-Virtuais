"""Testes automatizados para os relatórios do catálogo (relatorio.py)."""

from src.models.jogo import Jogo
from src.models.colecao import Colecao
from src.utils.relatorio import gerar_relatorio_geral


def criar_jogo(titulo: str, horas: float = 0.0, genero: str = "RPG", plataforma: str = "PC") -> Jogo:
    """Auxiliar: cria um jogo já com as horas informadas."""
    jogo = Jogo(titulo, genero, plataforma)
    if horas > 0:
        jogo.atualizar_progresso(horas)
    return jogo


def test_relatorio_nao_conta_duplicados():
    """Garante que o mesmo jogo em duas coleções conta uma vez, mas plataformas diferentes contam separado."""
    geral = Colecao("Geral")
    favoritos = Colecao("Favoritos")
    doom_pc = criar_jogo("Doom", 2.0, plataforma="PC")
    geral.adicionar_jogo(doom_pc)
    favoritos.adicionar_jogo(doom_pc)
    geral.adicionar_jogo(criar_jogo("Doom", 3.0, plataforma="Console"))

    stats = gerar_relatorio_geral([geral, favoritos])

    assert stats["total_colecoes"] == 2
    assert stats["total_jogos"] == 2
    assert stats["total_horas_jogadas"] == 5.0


def test_media_avaliacao_so_dos_finalizados():
    """Testa se a média considera apenas os jogos finalizados com nota."""
    geral = Colecao("Geral")
    for titulo, nota in [("A", 8.0), ("B", 9.0)]:
        jogo = criar_jogo(titulo, 2.0)
        jogo.finalizar()
        jogo.avaliar(nota)
        geral.adicionar_jogo(jogo)
    geral.adicionar_jogo(criar_jogo("C", 3.0)) # jogando, sem nota: não entra na média

    stats = gerar_relatorio_geral([geral])

    assert stats["media_avaliacao_finalizados"] == 8.5


def test_percentual_por_status():
    """Testa o percentual de jogos em cada status."""
    geral = Colecao("Geral")
    finalizado = criar_jogo("A", 2.0)
    finalizado.finalizar()
    geral.adicionar_jogo(finalizado)
    geral.adicionar_jogo(criar_jogo("B", 1.0))
    geral.adicionar_jogo(criar_jogo("C"))
    geral.adicionar_jogo(criar_jogo("D"))

    percentuais = gerar_relatorio_geral([geral])["percentual_por_status"]

    assert percentuais == {"NÃO INICIADO": 50.0, "JOGANDO": 25.0, "FINALIZADO": 25.0}


def test_top5_ordenado_e_limitado():
    """Testa se o top 5 vem em ordem decrescente de horas e tem no máximo 5 jogos."""
    geral = Colecao("Geral")
    for i in range(1, 7):
        geral.adicionar_jogo(criar_jogo(f"Jogo {i}", float(i)))
    geral.adicionar_jogo(criar_jogo("Sem horas"))

    top5 = gerar_relatorio_geral([geral])["top5_mais_jogados"]

    assert [j.titulo for j in top5] == ["Jogo 6", "Jogo 5", "Jogo 4", "Jogo 3", "Jogo 2"]


def test_horas_em_generos_favoritos():
    """Testa a soma de horas apenas dos gêneros favoritos (sem diferenciar maiúsculas)."""
    geral = Colecao("Geral")
    geral.adicionar_jogo(criar_jogo("A", 4.0, genero="RPG"))
    geral.adicionar_jogo(criar_jogo("B", 6.0, genero="FPS"))

    assert gerar_relatorio_geral([geral], ["rpg"])["horas_generos_favoritos"] == 4.0
    assert gerar_relatorio_geral([geral])["horas_generos_favoritos"] is None


def test_relatorio_sem_jogos():
    """Garante que o relatório funciona com o catálogo vazio, sem divisão por zero."""
    stats = gerar_relatorio_geral([Colecao("Geral")])

    assert stats["total_jogos"] == 0
    assert stats["media_avaliacao_finalizados"] is None
    assert stats["top5_mais_jogados"] == []
    assert all(valor == 0.0 for valor in stats["percentual_por_status"].values())