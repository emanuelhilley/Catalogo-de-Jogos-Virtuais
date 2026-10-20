import json # Carrega a biblioteca nativa do Python responsável por ler e escrever arquivos no formato JSON.
import os # biblioteca que interage com o sistema operacional (para criar pastas e verificar se arquivos existem na máquina).
from src.models.jogo import Jogo, JogoCampanha, JogoCompetitivo, JogoCooperativo, JogoPc, JogoConsole, JogoMobile
from src.models.colecao import Colecao

# Funções para converter objetos (Jogo, Colecao) em dicionários para poder guardar num ficheiro .json, e depois ler o JSON e recriar os objetos.

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
    
    # Atributos específicos de subclasses
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

  # Restaura o progresso
    horas = dados.get("horas_jogadas", 0.0)
    if horas > 0:
        jogo.atualizar_progresso(horas)

    status = dados.get("status", "NÃO INICIADO")
    if status:
        jogo.status = status

    if dados.get("avaliacao") is not None and jogo.status == "FINALIZADO":
        jogo.avaliar(dados["avaliacao"])
        
    return jogo

def salvar_colecoes(colecoes: list[Colecao], caminho_arquivo: str = "data/colecoes.json") -> None:
    """Salva uma lista de coleções e seus jogos num ficheiro JSON."""
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
    """Carrega as coleções e os seus jogos a partir de um ficheiro JSON."""
    if not os.path.exists(caminho_arquivo):
        return []
        
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados_totais = json.load(f)
        
    colecoes = []
    for dados_col in dados_totais:
        col = Colecao(dados_col["nome"])
        for dados_jogo in dados_col.get("jogos", []):
            jogo = dict_para_jogo(dados_jogo)
            col.adicionar_jogo(jogo)
        colecoes.append(col)
        
    return colecoes