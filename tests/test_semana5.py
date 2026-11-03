"""Testes automatizados da entrega final: regras de negócio e settings.json."""

import json
import pytest
from src.models.jogo import Jogo
from src.models.colecao import Colecao
from src.models.excecoes import LimiteJogandoError
from src.utils.regras import verificar_limite_jogando, contar_jogando, aviso_meta
from src.utils.settings import carregar_settings, salvar_settings, PADRAO


def criar_colecao_jogando(quantidade: int) -> Colecao:
    """Auxiliar: cria uma coleção com 'quantidade' jogos já com status JOGANDO."""
    colecao = Colecao("Geral")
    for i in range(quantidade):
        jogo = Jogo(f"Jogo {i}", "RPG", "PC")
        jogo.atualizar_progresso(1.0)
        colecao.adicionar_jogo(jogo)
    return colecao


def criar_colecao_finalizados(quantidade: int) -> Colecao:
    """Auxiliar: cria uma coleção com 'quantidade' jogos FINALIZADOS."""
    colecao = Colecao("Geral")
    for i in range(quantidade):
        jogo = Jogo(f"Jogo {i}", "RPG", "PC")
        jogo.atualizar_progresso(2.0)
        jogo.finalizar()
        colecao.adicionar_jogo(jogo)
    return colecao


# -=-=-= REGRAS DE NEGÓCIO (regras.py) =-=-=-

def test_limite_jogando_atingido():
    """Garante que não é possível passar do limite de jogos simultâneos JOGANDO."""
    colecao = criar_colecao_jogando(3)

    with pytest.raises(LimiteJogandoError):
        verificar_limite_jogando([colecao], 3)


def test_limite_jogando_nao_atingido():
    """Garante que abaixo do limite nenhum erro é levantado."""
    colecao = criar_colecao_jogando(2)

    verificar_limite_jogando([colecao], 3) # não deve levantar erro


def test_jogo_em_varias_colecoes_conta_uma_vez():
    """Garante que o mesmo jogo em duas coleções não conta duas vezes."""
    jogo = Jogo("Minecraft", "Sandbox", "PC")
    jogo.atualizar_progresso(1.0)
    geral = Colecao("Geral")
    favoritos = Colecao("Favoritos")
    geral.adicionar_jogo(jogo)
    favoritos.adicionar_jogo(jogo)

    assert contar_jogando([geral, favoritos]) == 1


def test_aviso_meta_nao_atingida():
    """Testa se o aviso é emitido quando os finalizados são menores que a meta."""
    colecao = criar_colecao_finalizados(1)

    aviso = aviso_meta([colecao], 3)

    assert aviso is not None
    assert "1/3" in aviso


def test_aviso_meta_atingida_ou_sem_meta():
    """Testa se nenhum aviso é emitido quando a meta foi atingida ou não existe."""
    colecao = criar_colecao_finalizados(2)

    assert aviso_meta([colecao], 2) is None
    assert aviso_meta([colecao], 0) is None


# -=-=-= CONFIGURAÇÕES (settings.py) =-=-=-

def test_settings_padrao_sem_arquivo(tmp_path):
    """Testa se, sem o arquivo, são usados os valores padrão."""
    config = carregar_settings(str(tmp_path / "nao_existe.json"))

    assert config == PADRAO


def test_settings_salvar_e_carregar(tmp_path):
    """Testa se uma configuração alterada é salva e carregada corretamente."""
    caminho = str(tmp_path / "settings.json")
    config = carregar_settings(caminho)
    config["meta_anual_jogos"] = 10
    config["generos_favoritos"] = ["RPG"]

    salvar_settings(config, caminho)
    recarregada = carregar_settings(caminho)

    assert recarregada["meta_anual_jogos"] == 10
    assert recarregada["generos_favoritos"] == ["RPG"]


def test_settings_chaves_ausentes_usam_padrao(tmp_path):
    """Testa se as chaves que faltam no arquivo recebem o valor padrão."""
    caminho = tmp_path / "settings.json"
    caminho.write_text(json.dumps({"limite_jogando": 2}), encoding="utf-8")

    config = carregar_settings(str(caminho))

    assert config["limite_jogando"] == 2
    assert config["meta_anual_jogos"] == PADRAO["meta_anual_jogos"]