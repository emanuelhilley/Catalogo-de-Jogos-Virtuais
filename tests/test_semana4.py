import pytest
from src.models.usuario import Usuario
from src.models.colecao import Colecao
from src.models.jogo import JogoPc, JogoConsole

def test_filtros_e_ordenacao():
    col = Colecao("Testes")
    j1 = JogoPc("Zelda", "Aventura", "GTX 1060", "Steam")
    j2 = JogoConsole("Mario", "Plataforma", "Switch")
    
    j1.atualizar_progresso(30.0)
    j2.atualizar_progresso(10.0)

    col.adicionar_jogo(j1)
    col.adicionar_jogo(j2)

    assert len(col.filtrar_por_genero("Aventura")) == 1
    assert len(col.filtrar_por_plataforma("PC")) == 1

    ordenados = col.ordenar_por_horas(decrescente=True)
    assert ordenados[0].titulo == "Zelda"

def test_meta_anual_usuario():
    usr = Usuario("Joao", "joao@email.com", meta_jogos_ano=2)
    col = usr.criar_colecao("Favoritos")
    
    j1 = JogoPc("Doom", "Ação", "GTX 1060", "Steam")
    j1.status = "FINALIZADO"
    col.adicionar_jogo(j1)

    prog = usr.progresso_meta()
    assert prog["finalizados"] == 1
    assert prog["atingida"] is False

    j2 = JogoConsole("Halo", "Ação", "Xbox")
    j2.status = "FINALIZADO"
    col.adicionar_jogo(j2)

    prog2 = usr.progresso_meta()
    assert prog2["finalizados"] == 2
    assert prog2["atingida"] is True