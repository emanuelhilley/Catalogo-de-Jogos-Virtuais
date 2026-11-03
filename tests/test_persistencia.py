"""Testes automatizados para a persistência em JSON (persistencia.py)."""

import json
from datetime import date
from src.models.jogo import Jogo, JogoCampanhaCoop
from src.models.colecao import Colecao
from src.models.usuario import Usuario
from src.utils.persistencia import (
    salvar_colecoes,
    carregar_colecoes,
    salvar_usuario,
    carregar_usuario
)


def pegar_geral(colecoes: list[Colecao]) -> Colecao:
    """Auxiliar: devolve a coleção 'Geral' de uma lista de coleções."""
    return next(c for c in colecoes if c.nome == "Geral")


def test_persistencia_preserva_tipo_e_campos(tmp_path):
    """Testa se salvar e carregar mantém a classe do jogo, as datas e os campos específicos."""
    caminho = str(tmp_path / "colecoes.json")
    jogo = JogoCampanhaCoop("It Takes Two", "Aventura", "PC", 2)
    jogo.ano_lancamento = 2021
    jogo.adicionar_participante("Ana")
    jogo.atualizar_progresso(5.0)
    jogo.finalizar()
    jogo.avaliar(9.5)
    geral = Colecao("Geral")
    geral.adicionar_jogo(jogo)

    salvar_colecoes([geral], caminho)
    carregado = pegar_geral(carregar_colecoes(caminho)).buscar_por_titulo("It Takes Two")

    assert isinstance(carregado, JogoCampanhaCoop)
    assert carregado.max_jogadores == 2
    assert carregado.participantes_frequentes == ["Ana"]
    assert carregado.ano_lancamento == 2021
    assert carregado.status == "FINALIZADO"
    assert carregado.avaliacao == 9.5
    assert carregado.data_termino == date.today()


def test_persistencia_nao_altera_datas_ao_carregar(tmp_path):
    """Garante que carregar um jogo não troca a data de início salva pela data de hoje."""
    caminho = str(tmp_path / "colecoes.json")
    jogo = Jogo("Hades", "Rogue-like", "PC")
    jogo.atualizar_progresso(3.0)
    jogo.data_inicio = date(2025, 1, 10)
    geral = Colecao("Geral")
    geral.adicionar_jogo(jogo)

    salvar_colecoes([geral], caminho)
    carregado = pegar_geral(carregar_colecoes(caminho)).buscar_por_titulo("Hades")

    assert carregado.data_inicio == date(2025, 1, 10)
    assert carregado.horas_jogadas == 3.0
    assert carregado.status == "JOGANDO"


def test_geral_espelha_mesmo_titulo_em_plataformas_diferentes(tmp_path):
    """Garante que dois jogos de mesmo título e plataformas diferentes entram na Geral."""
    caminho = str(tmp_path / "colecoes.json")
    favoritos = Colecao("Favoritos")
    favoritos.adicionar_jogo(Jogo("Doom", "FPS", "PC"))
    favoritos.adicionar_jogo(Jogo("Doom", "FPS", "Console"))

    salvar_colecoes([Colecao("Geral"), favoritos], caminho)
    geral = pegar_geral(carregar_colecoes(caminho))

    assert geral.total_jogos() == 2


def test_carregar_arquivo_antigo_sem_campos_novos(tmp_path):
    """Testa se um JSON antigo (sem ano e datas) continua carregando normalmente."""
    caminho = tmp_path / "colecoes.json"
    dados = [{
        "nome": "Geral",
        "jogos": [{
            "tipo": "Jogo", "titulo": "Doom", "genero": "FPS", "plataforma": "PC",
            "status": "JOGANDO", "horas_jogadas": 3.0, "avaliacao": None
        }]
    }]
    caminho.write_text(json.dumps(dados), encoding="utf-8")

    jogo = pegar_geral(carregar_colecoes(str(caminho))).buscar_por_titulo("Doom")

    assert jogo.horas_jogadas == 3.0
    assert jogo.ano_lancamento is None
    assert jogo.data_inicio is None


def test_carregar_sem_arquivo_cria_colecoes_padrao(tmp_path):
    """Testa se, sem arquivo salvo, as coleções 'Geral' e 'Favoritos' são criadas vazias."""
    colecoes = carregar_colecoes(str(tmp_path / "nao_existe.json"))

    assert [c.nome for c in colecoes] == ["Geral", "Favoritos"]
    assert all(c.total_jogos() == 0 for c in colecoes)


def test_salvar_e_carregar_usuario(tmp_path):
    """Testa se os dados do perfil do usuário são salvos e carregados corretamente."""
    caminho = str(tmp_path / "usuario.json")

    salvar_usuario(Usuario("Ana", "ana@email.com", meta_jogos_ano=3), caminho)
    usuario = carregar_usuario(caminho)

    assert usuario.nome == "Ana"
    assert usuario.email == "ana@email.com"
    assert usuario.meta_jogos_ano == 3
    assert carregar_usuario(str(tmp_path / "nao_existe.json")) is None