import json
import os
from src.models.jogo import Jogo, JogoPc, JogoConsole, JogoMobile
from src.models.colecao import Colecao
from src.models.usuario import Usuario

def jogo_para_dict(jogo: Jogo) -> dict:
    """Converte uma instância de Jogo ou subclasse num dicionário."""
    dados = {
        "tipo": jogo.__class__.__name__,
        "titulo": jogo.titulo,
        "genero": jogo.genero,
        "plataforma": jogo.plataforma,
        "status": jogo.status,
        "horas_jogadas": jogo.horas_jogadas,
        "avaliacao": jogo.avaliacao
    }
    if isinstance(jogo, JogoPc):
        dados["requisitos_minimos"] = jogo.requisitos_minimos
        dados["loja_digital"] = jogo.loja_digital
    elif isinstance(jogo, JogoConsole):
        dados["nome_console"] = jogo.nome_console
        dados["midia_fisica"] = jogo.midia_fisica
    elif isinstance(jogo, JogoMobile):
        dados["tamanho_mb"] = jogo.tamanho_mb
        dados["compras_no_app"] = jogo.compras_no_app
    return dados

def dict_para_jogo(dados: dict) -> Jogo:
    """Recria um objeto Jogo a partir de um dicionário."""
    tipo = dados.get("tipo", "Jogo")
    if tipo == "JogoPc":
        jogo = JogoPc(
            titulo=dados["titulo"],
            genero=dados["genero"],
            requisitos_minimos=dados.get("requisitos_minimos", ""),
            loja_digital=dados.get("loja_digital", "Steam")
        )
    elif tipo == "JogoConsole":
        jogo = JogoConsole(
            titulo=dados["titulo"],
            genero=dados["genero"],
            nome_console=dados.get("nome_console", "Console"),
            midia_fisica=dados.get("midia_fisica", False)
        )
    elif tipo == "JogoMobile":
        jogo = JogoMobile(
            titulo=dados["titulo"],
            genero=dados["genero"],
            tamanho_mb=dados.get("tamanho_mb", 0.0),
            compras_no_app=dados.get("compras_no_app", True)
        )
    else:
        jogo = Jogo(
            titulo=dados["titulo"],
            genero=dados["genero"],
            plataforma=dados.get("plataforma", "Outra")
        )
    
    horas = dados.get("horas_jogadas", 0.0)
    if horas > 0:
        jogo.atualizar_progresso(horas)
    status = dados.get("status", "NÃO INICIADO")
    if status:
        jogo.status = status
    if dados.get("avaliacao") is not None and jogo.status == "FINALIZADO":
        jogo.avaliar(dados["avaliacao"])
    return jogo

def garantir_colecoes_padrao(colecoes: list[Colecao]) -> list[Colecao]:
    """Garante que as coleções 'Geral' e 'Favoritos' existam e que 'Geral' contenha todos os jogos."""
    col_geral = next((c for c in colecoes if c.nome.lower() == "geral"), None)
    if not col_geral:
        col_geral = Colecao("Geral")
        colecoes.insert(0, col_geral)

    col_fav = next((c for c in colecoes if c.nome.lower() == "favoritos"), None)
    if not col_fav:
        col_fav = Colecao("Favoritos")
        colecoes.append(col_fav)

    # Sincroniza todos os jogos cadastrados nas outras coleções para a coleção Geral
    titulos_geral = {j.titulo.lower() for j in col_geral.listar_jogos()}
    for col in colecoes:
        if col.nome.lower() == "geral":
            continue
        for jogo in col.listar_jogos():
            if jogo.titulo.lower() not in titulos_geral:
                col_geral.adicionar_jogo(jogo)
                titulos_geral.add(jogo.titulo.lower())

    return colecoes

def salvar_colecoes(colecoes: list[Colecao], caminho_arquivo: str = "data/colecoes.json") -> None:
    """Salva a lista de coleções no arquivo JSON garantindo a presença das coleções padrão."""
    colecoes = garantir_colecoes_padrao(colecoes)
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    dados_totais = []
    for col in colecoes:
        dados_col = {
            "nome": col.nome,
            "jogos": [jogo_para_dict(j) for j in col.listar_jogos()]
        }
        dados_totais.append(dados_col)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_totais, f, indent=4, ensure_ascii=False)

def carregar_colecoes(caminho_arquivo: str = "data/colecoes.json") -> list[Colecao]:
    """Carrega as coleções e assegura a existência de 'Geral' e 'Favoritos'."""
    colecoes = []
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_totais = json.load(f)
        for dados_col in dados_totais:
            col = Colecao(dados_col["nome"])
            for dados_jogo in dados_col.get("jogos", []):
                jogo = dict_para_jogo(dados_jogo)
                col.adicionar_jogo(jogo)
            colecoes.append(col)

    return garantir_colecoes_padrao(colecoes)

def salvar_usuario(usuario: Usuario, caminho_arquivo: str = "data/usuario.json") -> None:
    """Salva os dados do perfil do usuário em formato JSON."""
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    dados = {
        "nome": usuario.nome,
        "email": usuario.email,
        "meta_jogos_ano": usuario.meta_jogos_ano
    }
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_usuario(caminho_arquivo: str = "data/usuario.json") -> Usuario | None:
    """Carrega os dados do perfil do usuário do arquivo JSON."""
    if not os.path.exists(caminho_arquivo):
        return None
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return Usuario(
            nome=dados["nome"],
            email=dados["email"],
            meta_jogos_ano=dados.get("meta_jogos_ano", 0)
        )