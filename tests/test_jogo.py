"""Testes automátizados para a classe Jogo e suas subclasses."""

import pytest
from datetime import date
from src.models.jogo import (
    Jogo, JogoPc, JogoCompetitivo,
    JogoCampanha, JogoCooperativo, JogoCampanhaCoop
)
from src.models.excecoes import (
    CatalogoError,
    TituloInvalidoError,
    HorasInvalidasError,
    StatusInvalidoError,
    AvaliacaoInvalidaError,
    JogoDuplicadoError
)

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

# -=-=-= NOVOS TESTES: validações, regras de negócio e exceções customizadas -=-=-=

def test_titulo_vazio():
    """Garante que não é possível criar um jogo com título vazio."""
    with pytest.raises(TituloInvalidoError):
        Jogo("   ", "RPG", "PC")

def test_status_invalido():
    """Garante que o status só aceita um dos três valores permitidos."""
    jogo = Jogo("Hades", "Rogue-like", "PC")

    with pytest.raises(StatusInvalidoError):
        jogo.status = "PAUSADO"

def test_progresso_com_horas_zero():
    """Garante que o progresso só aceita horas maiores que zero."""
    jogo = Jogo("Celeste", "Plataforma", "PC")

    with pytest.raises(HorasInvalidasError):
        jogo.atualizar_progresso(0)

def test_finalizar_com_menos_de_1h():
    """Garante que não é possível finalizar um jogo com menos de 1h registrada."""
    jogo = Jogo("Celeste", "Plataforma", "PC")
    jogo.atualizar_progresso(0.5)

    with pytest.raises(StatusInvalidoError, match="pelo menos"):
        jogo.finalizar()

    assert jogo.status == "JOGANDO" # o status não pode mudar quando a regra falha

def test_finalizar_com_sucesso_registra_datas():
    """Testa se finalizar muda o status e registra as datas de início e término."""
    jogo = Jogo("Hollow Knight", "Metroidvania", "PC")
    jogo.atualizar_progresso(2.0)
    jogo.finalizar()

    assert jogo.status == "FINALIZADO"
    assert jogo.data_inicio == date.today()
    assert jogo.data_termino == date.today()

def test_nota_fora_do_intervalo():
    """Garante que a nota precisa estar entre 0 e 10."""
    jogo = Jogo("Elden Ring", "Action RPG", "PC")
    jogo.atualizar_progresso(2.0)
    jogo.finalizar()

    with pytest.raises(AvaliacaoInvalidaError):
        jogo.avaliar(11)

def test_reiniciar_jogo():
    """Testa se reiniciar zera horas e nota e volta o status para JOGANDO."""
    jogo = Jogo("Hades", "Rogue-like", "PC")
    jogo.atualizar_progresso(3.0)
    jogo.finalizar()
    jogo.avaliar(9.0)

    jogo.reiniciar()

    assert jogo.horas_jogadas == 0.0
    assert jogo.avaliacao is None
    assert jogo.status == "JOGANDO"
    assert jogo.data_termino is None

def test_excecoes_herdam_de_valueerror():
    """Garante que as exceções customizadas continuam sendo capturadas por 'except ValueError'."""
    assert issubclass(CatalogoError, ValueError)
    assert issubclass(JogoDuplicadoError, CatalogoError)
    assert issubclass(StatusInvalidoError, ValueError)

# -=-=-= NOVOS TESTES: métodos especiais =-=-=-

def test_lt_ordena_por_horas_e_repr():
    """Testa o __lt__ (ordenação por horas jogadas) e o __repr__ (exibição detalhada)."""
    jogo1 = Jogo("A", "RPG", "PC")
    jogo1.atualizar_progresso(2.0)
    jogo2 = Jogo("B", "RPG", "PC")
    jogo2.atualizar_progresso(5.0)

    assert jogo1 < jogo2
    assert sorted([jogo2, jogo1]) == [jogo1, jogo2]
    assert "Jogo(titulo='A'" in repr(jogo1)

def test_hash_consistente_com_eq():
    """Testa se jogos iguais (título + plataforma) contam como um só em um conjunto."""
    jogo1 = Jogo("Minecraft", "Sandbox", "PC")
    jogo2 = Jogo("minecraft", "Sobrevivência", "pc")

    assert len({jogo1, jogo2}) == 1

# -=-=-= NOVOS TESTES: herança múltipla com mixins =-=-=-

def test_heranca_multipla_campanha_coop():
    """Testa se JogoCampanhaCoop reúne os recursos de campanha e de cooperativo."""
    jogo = JogoCampanhaCoop("It Takes Two", "Aventura", "PC", 2)

    assert isinstance(jogo, JogoCampanha)
    assert isinstance(jogo, JogoCooperativo)
    assert isinstance(jogo, Jogo)
    assert jogo.titulo == "It Takes Two"
    assert jogo.plataforma == "PC"
    assert jogo.capitulos_concluidos == 0   # vem do CampanhaMixin
    assert jogo.max_jogadores == 2          # vem do CooperativoMixin
    assert jogo.modo_progresso_compartilhado is True
    assert "Capítulos: 0" in jogo.resumo_coop()

def test_participantes_frequentes_sem_repetir():
    """Testa se o jogo cooperativo guarda os participantes sem repetir nomes."""
    jogo = JogoCooperativo("Minecraft", "Sandbox", "PC", 4)
    jogo.adicionar_participante("Ana")
    jogo.adicionar_participante("Ana")
    jogo.adicionar_participante("Bruno")

    assert jogo.participantes_frequentes == ["Ana", "Bruno"]