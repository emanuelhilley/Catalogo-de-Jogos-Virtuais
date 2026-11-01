import json
import os
from src.models.jogo import (
    Jogo,
    JogoPc,
    JogoConsole,
    JogoMobile,
    JogoCampanha,
    JogoCompetitivo,
    JogoCooperativo,
    JogoCampanhaCoop
)
from src.models.colecao import Colecao
from src.models.usuario import Usuario

def jogo_para_dict(jogo: Jogo) -> dict:
    """Converte uma instância de Jogo ou qualquer subclasse num dicionário para JSON."""
    dados = {
        "tipo": jogo.__class__.__name__,
        "titulo": jogo.titulo,
        "genero": jogo.genero,
        "plataforma": jogo.plataforma,
        "status": jogo.status,
        "horas_jogadas": jogo.horas_jogadas,
        "avaliacao": jogo.avaliacao
    }

    # Atributos específicos por Plataforma
    if isinstance(jogo, JogoPc):
        dados["requisitos_minimos"] = getattr(jogo, "requisitos_minimos", "")
        dados["loja_digital"] = getattr(jogo, "loja_digital", "Steam")
    elif isinstance(jogo, JogoConsole):
        dados["nome_console"] = getattr(jogo, "nome_console", "Console")
        dados["midia_fisica"] = getattr(jogo, "midia_fisica", False)
    elif isinstance(jogo, JogoMobile):
        dados["tamanho_mb"] = getattr(jogo, "tamanho_mb", 0.0)
        dados["compras_no_app"] = getattr(jogo, "compras_no_app", True)

    # Atributos específicos por Modo de Jogo
    if isinstance(jogo, JogoCampanha):
        dados["capitulos_concluidos"] = getattr(jogo, "capitulos_concluidos", 0)
        dados["percentual_conclusao"] = getattr(jogo, "percentual_conclusao", 0.0)

    if isinstance(jogo, JogoCompetitivo):
        dados["partidas_jogadas"] = getattr(jogo, "partidas_jogadas", 0)
        dados["vitorias"] = getattr(jogo, "vitorias", 0)
        dados["derrotas"] = getattr(jogo, "derrotas", 0)
        dados["ranking"] = getattr(jogo, "ranking", "Unranked")

    if isinstance(jogo, JogoCooperativo):
        dados["sessoes_cooperativas"] = getattr(jogo, "sessoes_cooperativas", 0)
        dados["max_jogadores"] = getattr(jogo, "max_jogadores", 4)

    if isinstance(jogo, JogoCampanhaCoop):
        dados["modo_progresso_compartilhado"] = getattr(jogo, "modo_progresso_compartilhado", True)

    return dados

def dict_para_jogo(dados: dict) -> Jogo:
    """Recria um objeto Jogo correto a partir dos dados do JSON."""
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
    elif tipo == "JogoCampanha":
        jogo = JogoCampanha(
            titulo=dados["titulo"],
            genero=dados["genero"],
            plataforma=dados.get("plataforma", "Outra")
        )
        jogo.capitulos_concluidos = dados.get("capitulos_concluidos", 0)
        jogo.percentual_conclusao = dados.get("percentual_conclusao", 0.0)
    elif tipo == "JogoCompetitivo":
        jogo = JogoCompetitivo(
            titulo=dados["titulo"],
            genero=dados["genero"],
            plataforma=dados.get("plataforma", "Outra"),
            ranking=dados.get("ranking", "Unranked")
        )
        jogo.partidas_jogadas = dados.get("partidas_jogadas", 0)
        jogo.vitorias = dados.get("vitorias", 0)
        jogo.derrotas = dados.get("derrotas", 0)
    elif tipo == "JogoCooperativo":
        jogo = JogoCooperativo(
            titulo=dados["titulo"],
            genero=dados["genero"],
            plataforma=dados.get("plataforma", "Outra"),
            max_jogadores=dados.get("max_jogadores", 4)
        )
        jogo.sessoes_cooperativas = dados.get("sessoes_cooperativas", 0)
    elif tipo == "JogoCampanhaCoop":
        jogo = JogoCampanhaCoop(
            titulo=dados["titulo"],
            genero=dados["genero"],
            plataforma=dados.get("plataforma", "Outra"),
            max_jogadores=dados.get("max_jogadores", 4),
            progresso_compartilhado=dados.get("modo_progresso_compartilhado", True)
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
    """Garante a existência das coleções 'Geral' e 'Favoritos', agregando todos os jogos em 'Geral'."""
    col_geral = next((c for c in colecoes if c.nome.lower() == "geral"), None)
    if not col_geral:
        col_geral = Colecao("Geral")
        colecoes.insert(0, col_geral)
    else:
        colecoes.remove(col_geral)
        colecoes.insert(0, col_geral)

    col_fav = next((c for c in colecoes if c.nome.lower() == "favoritos"), None)
    if not col_fav:
        col_fav = Colecao("Favoritos")
        colecoes.append(col_fav)

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
    """Salva a lista de coleções garantindo a sincronização de Geral e Favoritos."""
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
    """Carrega as coleções do JSON recriando os objetos exatos de cada classe."""
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

def resetar_catalogo() -> list[Colecao]:
    """Zera o catálogo de jogos criando novas coleções padrão 'Geral' e 'Favoritos'."""
    colecoes_limpas = [Colecao("Geral"), Colecao("Favoritos")]
    salvar_colecoes(colecoes_limpas)
    return colecoes_limpas

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