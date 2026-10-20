import os
import pytest
from src.models.jogo import JogoPc, JogoConsole
from src.models.colecao import Colecao
from src.utils.persistencia import salvar_colecoes, carregar_colecoes
from src.utils.relatorio import gerar_relatorio_geral

FILE_TEST = "data/test_colecoes.json"

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(FILE_TEST):
        os.remove(FILE_TEST)

def test_salvar_e_carregar_json():
    colecao = Colecao("Favoritos")
    pc_game = JogoPc("Portal 2", "Puzzle", "GTX 750", "Steam")
    console_game = JogoConsole("God of War", "Ação", "PS5", True)
    
    colecao.adicionar_jogo(pc_game)
    colecao.adicionar_jogo(console_game)
    
    salvar_colecoes([colecao], FILE_TEST)
    assert os.path.exists(FILE_TEST)
    
    colecoes_carregadas = carregar_colecoes(FILE_TEST)
    assert len(colecoes_carregadas) == 1
    assert colecoes_carregadas[0].nome == "Favoritos"
    assert colecoes_carregadas[0].total_jogos() == 2

def test_relatorio_inicial():
    col1 = Colecao("RPG")
    game1 = JogoPc("The Witcher 3", "RPG", "GTX 1060", "GOG")
    game1.atualizar_progresso(50.0)
    col1.adicionar_jogo(game1)
    
    stats = gerar_relatorio_geral([col1])
    assert stats["total_colecoes"] == 1
    assert stats["total_jogos"] == 1
    assert stats["total_horas_jogadas"] == 50.0