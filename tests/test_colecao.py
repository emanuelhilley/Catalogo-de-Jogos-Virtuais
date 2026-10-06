"""Testes automatizados para a classe Colecao (CRUD)."""

import pytest
from src.models.jogo import Jogo
from src.models.colecao import Colecao


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