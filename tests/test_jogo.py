"""Testes automátizados para a classe Jogo e suas subclasses."""

import pytest
from src.models.jogo import Jogo, JogoPc, JogoCompetitivo

def test_criacao_jogo_base():
    """Testa se um jogo é criado seguindo os padrões corretos."""
    jogo = Jogo("The witcher","RPG","PC")
    assert jogo.titulo == "The witcher"
    assert jogo.genero == "RPG" 
    assert jogo.plataforma == "PC"
    assert jogo.status == "NÃO INICIADO"
    assert jogo.horas_jogadas == 0.0
    assert jogo.avaliacao is None

def test_atualizar_progresso_sucesso():
    "Testa a atualização de horas e a mudança de status."
    jogo = Jogo("Celeste", "Plataforma", "PC")
    jogo.atualizar_progresso(5.5)

    assert jogo.horas_jogadas == 5.5
    assert jogo.status == "JOGANDO"

def test_validacao_horas_negativas():
    "Garente que o sistema dispare ValueError quando inserido horas negativas."
    jogo = Jogo("Hades", "Rogue-like", "PC")

    with pytest.raises(ValueError, match= "O total de horas jogadas não pode ser negativo"): 
        # Diz ao pytest que é esperado que esse pedaço de código lance um erro. Se o erro for lançado como esperado, o teste passa com sucesso
        jogo.horas_jogadas = -10

def test_validacao_avaliacao_status_invalido():
    """Garante que não é possível avaliar um jogo que ainda não está finalizado."""
    jogo = Jogo("Elden Ring", "Action RPG", "PC")

    with pytest.raises(ValueError, match="FINALIZADO"):
        jogo.avaliar(9.5)

def test_avaliar_jogo_finalizado_com_sucesso():
    "Testa se a avaliação funciona perfeitamente após um jogo ser finalizado."
    jogo = Jogo("Hollow Knight", "Metroidvania", "PC")
    jogo.status = "FINALIZADO"
    jogo.avaliar(10.0)

    assert jogo.avaliacao == 10.0

def test_comparacao_jogos_iguais():
    "Testa se 2 jogos são iguais com o __eq__ ."
    jogo1 = Jogo("Minecraft", "Sandbox", "PC")
    jogo2 = Jogo("minecraft", "Sobrevivência", "pc")

    assert jogo1 == jogo2

def test_subclasse_pc():
    """Testa se a subclasse JogoPc inicializa os atributos específicos corretamente. """
    jogo_pc = JogoPc("Cyberpunk 2077", "RPG", "16GB RAM, RTX 2060", "Steam")
    assert jogo_pc.plataforma == "PC"
    assert jogo_pc.loja_digital == "Steam"
    assert jogo_pc.requisitos_minimos == "16GB RAM, RTX 2060"

def test_subclasse_jogo_competitivo():
    """Testa o cálculo da taxa de vitória na subclasse jogo competitivo."""
    jogo_pvp = JogoCompetitivo("Valorant", "FPS", "PC", ranking="Imortal")
    jogo_pvp.partidas_jogadas = 10
    jogo_pvp.vitorias = 7
    jogo_pvp.derrotas = 3

    assert jogo_pvp.taxa_vitoria() == 70.0
    assert jogo_pvp.ranking == "Imortal"

