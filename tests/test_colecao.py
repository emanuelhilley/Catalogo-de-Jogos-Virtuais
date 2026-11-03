"""Testes automatizados para a classe Colecao (CRUD)."""

import pytest
from src.models.jogo import Jogo
from src.models.colecao import Colecao
from src.models.excecoes import JogoDuplicadoError


def test_criacao_colecao():
    """Testa a inicialização de uma coleção vazia."""
    colecao = Colecao("Favoritos")
    assert colecao.nome == "Favoritos"
    assert colecao.total_jogos() == 0


def test_adicionar_e_buscar_jogo():
    """Testa a adição e a busca de um jogo pelo título (Create e Read)."""
    colecao = Colecao("RPG")
    jogo = Jogo("Chrono Trigger", "RPG", "SNES")

    colecao.adicionar_jogo(jogo)

    assert colecao.total_jogos() == 1
    assert colecao.buscar_por_titulo("chrono trigger") == jogo


def test_adicionar_jogo_duplicado():
    """Garante que não é possível adicionar dois jogos iguais na mesma coleção."""
    colecao = Colecao("Minha Lista")
    jogo1 = Jogo("Portal 2", "Puzzle", "PC")
    jogo2 = Jogo("portal 2", "Puzzle", "PC")

    colecao.adicionar_jogo(jogo1)

    with pytest.raises(ValueError, match="já está presente"):
        colecao.adicionar_jogo(jogo2)


def test_atualizar_jogo_com_kwargs(): # kwargs permite atualizar qualquer atributo do jogo de uma só vez
    """Testa a atualização de atributos de um jogo via **kwargs (Update)."""
    colecao = Colecao("Zerados")
    jogo = Jogo("God of War", "Ação", "PlayStation")
    colecao.adicionar_jogo(jogo)

    sucesso = colecao.atualizar_jogo("God of War", status="FINALIZADO", genero="Ação/Aventura")

    assert sucesso is True
    assert jogo.status == "FINALIZADO"
    assert jogo.genero == "Ação/Aventura"


def test_remover_jogo():
    """Testa a remoção de um jogo existente (Delete)."""
    colecao = Colecao("PC")
    jogo = Jogo("Doom", "FPS", "PC")
    colecao.adicionar_jogo(jogo)

    removido = colecao.remover_jogo("Doom")

    assert removido is True
    assert colecao.total_jogos() == 0
    assert colecao.buscar_por_titulo("Doom") is None


# -=-=-= NOVOS TESTES: exceção customizada, busca, filtros e ordenação =-=-=-

def test_duplicado_levanta_excecao_customizada():
    """Garante que o duplicado levanta JogoDuplicadoError (que também é um ValueError)."""
    colecao = Colecao("Minha Lista")
    colecao.adicionar_jogo(Jogo("Portal 2", "Puzzle", "PC"))

    with pytest.raises(JogoDuplicadoError):
        colecao.adicionar_jogo(Jogo("PORTAL 2", "Puzzle", "pc"))


def test_buscar_por_parte_do_titulo():
    """Testa a busca de jogos por um trecho do título."""
    colecao = Colecao("Geral")
    colecao.adicionar_jogo(Jogo("Minecraft", "Sandbox", "PC"))
    colecao.adicionar_jogo(Jogo("Terraria", "Sandbox", "PC"))
    colecao.adicionar_jogo(Jogo("Doom", "FPS", "PC"))

    encontrados = colecao.buscar_por_parte_do_titulo("CRAFT")

    assert len(encontrados) == 1
    assert encontrados[0].titulo == "Minecraft"
    assert colecao.buscar_por_parte_do_titulo("xyz") == []


def test_filtrar_por_nota_minima():
    """Testa o filtro por nota mínima (jogos sem nota ficam de fora)."""
    colecao = Colecao("Geral")
    jogo1 = Jogo("Hades", "Rogue-like", "PC")
    jogo2 = Jogo("Doom", "FPS", "PC")
    jogo3 = Jogo("Celeste", "Plataforma", "PC")

    for jogo, nota in [(jogo1, 9.0), (jogo2, 5.0)]:
        jogo.atualizar_progresso(2.0)
        jogo.finalizar()
        jogo.avaliar(nota)

    for jogo in (jogo1, jogo2, jogo3):
        colecao.adicionar_jogo(jogo)

    filtrados = colecao.filtrar_por_nota_minima(8.0)

    assert filtrados == [jogo1]


def test_ordenar_por_ano():
    """Testa a ordenação por ano de lançamento (jogos sem ano ficam no fim)."""
    colecao = Colecao("Geral")
    antigo = Jogo("Doom", "FPS", "PC")
    antigo.ano_lancamento = 1993
    novo = Jogo("Hades", "Rogue-like", "PC")
    novo.ano_lancamento = 2020
    sem_ano = Jogo("Celeste", "Plataforma", "PC")

    for jogo in (antigo, sem_ano, novo):
        colecao.adicionar_jogo(jogo)

    titulos = [j.titulo for j in colecao.ordenar_por_ano()]

    assert titulos == ["Hades", "Doom", "Celeste"]


def test_getter_jogos_retorna_copia():
    """Garante o encapsulamento: alterar a lista devolvida não altera a coleção."""
    colecao = Colecao("Geral")
    colecao.adicionar_jogo(Jogo("Doom", "FPS", "PC"))

    colecao.jogos.clear()

    assert colecao.total_jogos() == 1