import sys

from src.cli.exibicao import console
from src.cli.parser import criar_parser
from src.cli.comandos_usuario import tratar_usuario
from src.cli.comandos_colecao import tratar_colecao
from src.cli.comandos_jogo import tratar_jogo
from src.cli.comandos_settings import tratar_settings
from src.utils.relatorio import exibir_relatorio_terminal
from src.utils.persistencia import carregar_colecoes
from src.utils.settings import carregar_settings


def tratar_relatorio(args, colecoes, config) -> None:
    """Exibe os relatórios do catálogo."""
    if args.acao == "geral":
        exibir_relatorio_terminal(colecoes, config["generos_favoritos"])


# cada comando principal aponta para a função que trata as suas ações
COMANDOS = {
    "usuario": tratar_usuario,
    "colecao": tratar_colecao,
    "jogo": tratar_jogo,
    "settings": tratar_settings,
    "relatorio": tratar_relatorio,
}


def main():
    parser, parsers_modulos = criar_parser()

    if len(sys.argv) == 1:
        console.clear()
        parser.print_help()
        return

    args = parser.parse_args()

    console.clear()

    if args.comando_principal in parsers_modulos and getattr(args, "acao", None) is None:
        parsers_modulos[args.comando_principal].print_help()
        return

    tratar = COMANDOS.get(args.comando_principal)
    if tratar is None:
        parser.print_help()
        return

    colecoes = carregar_colecoes()
    config = carregar_settings() # regras configuráveis (meta anual, limite de JOGANDO, plataforma principal...)
    tratar(args, colecoes, config)


if __name__ == "__main__":
    main()