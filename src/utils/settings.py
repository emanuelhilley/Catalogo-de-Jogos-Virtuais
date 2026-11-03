""" Leitura e gravação do settings.json (regras de negócio configuráveis). """
import json
import os

CAMINHO_SETTINGS = "settings.json"

# valores usados quando o arquivo não existe ou quando falta alguma chave
PADRAO = {
    "generos_favoritos": [],
    "meta_anual_jogos": 5,
    "plataforma_principal": "pc",
    "limite_jogando": 3
}

def carregar_settings(caminho_arquivo: str = CAMINHO_SETTINGS) -> dict:
    """Carrega as configurações do JSON. Chaves ausentes usam o valor padrão."""
    config = dict(PADRAO) # copia o padrão para não alterar o original
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            config.update(json.load(f)) # o que estiver no arquivo sobrescreve o padrão
    return config

def salvar_settings(config: dict, caminho_arquivo: str = CAMINHO_SETTINGS) -> None:
    """Salva as configurações em formato JSON."""
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)