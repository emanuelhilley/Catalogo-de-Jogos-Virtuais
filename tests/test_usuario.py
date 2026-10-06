"""Teste automatizados para a parte de Usuário."""
import pytest
from src.models.usuario import Usuario

def test_validacao_usuario_e_email():
    """Testa a criação do usuário e a validação do email."""
    usuario = Usuario("Emanuel", "Emanuel@gmail.com")
    assert usuario.nome == "Emanuel"
    assert usuario.email == "Emanuel@gmail.com"

    with pytest.raises(ValueError, match="e-mail fornecido é inválido"):
        usuario.email = "email_invalido"

def test_gerenciamento_colecoes_usuario():
    """Testa a criação, busca e remoção de coleções do usuário."""
    usuario = Usuario("Emanuel", "emanuel@email.com")

    # Criar coleção
    colecao_rpg = usuario.criar_colecao("RPGs Favoritos")
    assert len(usuario.colecoes) == 1
    assert colecao_rpg.nome == "RPGs Favoritos"

    # Buscar coleção
    encontrada = usuario.buscar_colecao("rpgs favoritos")
    assert encontrada == colecao_rpg

    # Remover coleção
    removida = usuario.remover_colecao("RPGs Favoritos")
    assert removida is True
    assert len(usuario.colecoes) == 0