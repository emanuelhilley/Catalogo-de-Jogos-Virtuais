""" Configuração do parser principal e dos subcomandos da CLI. """
import argparse
import sys
from rich.panel import Panel
from rich.table import Table
from rich_argparse import RichHelpFormatter

from src.cli.exibicao import console
from src.utils.persistencia import carregar_colecoes


class CustomArgumentParser(argparse.ArgumentParser):
    """Customização do ArgumentParser para exibir tabelas estilizadas e dados cadastrados quando faltarem argumentos."""

    def error(self, message: str):
        console.clear()
        prog_name = self.prog.replace("main.py ", "")

        console.print(Panel(
            f"[bold red]⚠️ Parâmetros incompletos ou incorretos para o comando:[/bold red] [bold yellow]{prog_name}[/bold yellow]\n\n"
            f"[dim]Mensagem do sistema: {message}[/dim]",
            title="Sintaxe Incorreta",
            border_style="red"
        ))

        table_args = Table(
            title=f"📋 Parâmetros Aceitos para: [bold cyan]{prog_name}[/bold cyan]",
            header_style="bold magenta",
            border_style="dim"
        )
        table_args.add_column("Parâmetro", style="bold white")
        table_args.add_column("Obrigatório?", justify="center")
        table_args.add_column("Tipo / Opções", style="cyan")
        table_args.add_column("Descrição", style="yellow")

        for action in self._actions:
            if action.dest == "help":
                continue

            opts = ", ".join(action.option_strings) if action.option_strings else action.dest
            req = "[bold red]Sim[/bold red]" if action.required else "[dim green]Não[/dim green]"

            if action.choices:
                tipo = " | ".join(map(str, action.choices))
            elif action.type == int:
                tipo = "Número (Inteiro)"
            elif action.type == float:
                tipo = "Número (Decimal)"
            elif isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction)):
                tipo = "Flag (Opção)"
            else:
                tipo = "Texto"

            table_args.add_row(opts, req, tipo, action.help or "")

        console.print(table_args)

        if "jogo" in prog_name or "colecao" in prog_name:
            try:
                colecoes = carregar_colecoes()
                if colecoes:
                    table_dados = Table(
                        title=" Suas Coleções e Jogos Cadastrados",
                        header_style="bold green",
                        border_style="green"
                    )
                    table_dados.add_column("Coleção", style="bold white")
                    table_dados.add_column("Jogos Disponíveis", style="yellow")

                    for c in colecoes:
                        lista_jogos = ", ".join([f"'{j.titulo}'" for j in c.listar_jogos()]) or "[dim](Nenhum jogo nesta coleção)[/dim]"
                        table_dados.add_row(c.nome, lista_jogos)

                    console.print(table_dados)
            except Exception:
                pass

        exemplo = f"python3 main.py {prog_name}"
        if "jogo progresso" in prog_name:
            exemplo += ' --titulo "Minecraft" --horas 2.5'
        elif "jogo adicionar" in prog_name:
            exemplo += ' --titulo "Minecraft" --genero "Sandbox / Cooperativo" --plataforma pc --modo cooperativo --max-jogadores 4 --ano 2011'
        elif "jogo avaliar" in prog_name:
            exemplo += ' --titulo "Minecraft" --nota 9.5'
        elif "usuario criar" in prog_name:
            exemplo += ' --nome "Maria" --email "maria@email.com" --meta 5'
        elif "usuario atualizar" in prog_name:
            exemplo += ' --nome "Maria Silva" --email "maria.silva@email.com"'
        elif "colecao criar" in prog_name:
            exemplo += ' --nome "Jogos com os amigos"'
        elif "colecao adicionar-jogo" in prog_name:
            exemplo += ' --nome "Favoritos" --titulo "Minecraft"'
        elif "settings definir" in prog_name:
            exemplo += ' --meta 5 --limite-jogando 3 --plataforma-principal pc --generos-favoritos "RPG, Ação"'

        console.print(Panel(
            f"[bold white]Copie, cole e ajuste os valores no terminal:[/bold white]\n"
            f"[bold green]{exemplo}[/bold green]",
            title=" Exemplo Prático de Uso",
            border_style="cyan"
        ))
        sys.exit(2)


# ==================== SUBCOMANDOS (um bloco por módulo) ====================

def _adicionar_usuario(subparsers, parsers_modulos: dict) -> None:
    parser_user = subparsers.add_parser("usuario", help="Gerenciar perfil de usuário e metas", formatter_class=RichHelpFormatter)
    parsers_modulos["usuario"] = parser_user
    sub_user = parser_user.add_subparsers(dest="acao", parser_class=CustomArgumentParser)

    cmd_user_criar = sub_user.add_parser("criar", help="Criar NOVO perfil de usuário (reseta os jogos e coleções anteriores)", formatter_class=RichHelpFormatter)
    cmd_user_criar.add_argument("--nome", required=True, type=str, help="Nome do usuário")
    cmd_user_criar.add_argument("--email", required=True, type=str, help="E-mail do usuário")
    cmd_user_criar.add_argument("--meta", type=int, default=None, help="Meta anual de jogos a finalizar (opcional, padrão: a do settings.json)")

    cmd_user_atualizar = sub_user.add_parser("atualizar", help="Atualizar dados do perfil existente (mantém os jogos)", formatter_class=RichHelpFormatter)
    cmd_user_atualizar.add_argument("--nome", type=str, help="Novo nome do usuário")
    cmd_user_atualizar.add_argument("--email", type=str, help="Novo e-mail do usuário")
    cmd_user_atualizar.add_argument("--meta", type=int, help="Nova meta anual de jogos")

    sub_user.add_parser("ver", help="Exibir informações do perfil cadastrado", formatter_class=RichHelpFormatter)
    sub_user.add_parser("meta", help="Verificar o progresso da meta anual", formatter_class=RichHelpFormatter)


def _adicionar_colecao(subparsers, parsers_modulos: dict) -> None:
    parser_col = subparsers.add_parser("colecao", help="Gerenciar coleções de jogos", formatter_class=RichHelpFormatter)
    parsers_modulos["colecao"] = parser_col
    sub_col = parser_col.add_subparsers(dest="acao", parser_class=CustomArgumentParser)

    cmd_col_criar = sub_col.add_parser("criar", help="Criar uma nova coleção", formatter_class=RichHelpFormatter)
    cmd_col_criar.add_argument("--nome", required=True, type=str, help="Nome da coleção")

    cmd_col_listar = sub_col.add_parser("listar", help="Listar coleções cadastradas", formatter_class=RichHelpFormatter)
    cmd_col_listar.add_argument("--detalhada", action="store_true", help="Exibe os jogos dentro de cada coleção")

    cmd_col_ver = sub_col.add_parser("ver", help="Exibir jogos de uma coleção (ou listar as disponíveis)", formatter_class=RichHelpFormatter)
    cmd_col_ver.add_argument("--nome", type=str, default=None, help="Nome da coleção (opcional)")

    cmd_col_remover = sub_col.add_parser("remover", help="Remover uma coleção pelo nome", formatter_class=RichHelpFormatter)
    cmd_col_remover.add_argument("--nome", required=True, type=str, help="Nome da coleção a ser removida")

    cmd_col_addjogo = sub_col.add_parser("adicionar-jogo", help="Adicionar a uma coleção um jogo já cadastrado em 'Geral'", formatter_class=RichHelpFormatter)
    cmd_col_addjogo.add_argument("--nome", required=True, type=str, help="Nome da coleção destino")
    cmd_col_addjogo.add_argument("--titulo", required=True, type=str, help="Título do jogo já cadastrado")

    cmd_col_filtrar = sub_col.add_parser("filtrar", help="Filtrar jogos de uma coleção", formatter_class=RichHelpFormatter)
    cmd_col_filtrar.add_argument("--nome", required=True, type=str, help="Nome da coleção")
    cmd_col_filtrar.add_argument(
        "--status",
        type=lambda s: s.upper(),
        choices=["NÃO INICIADO", "JOGANDO", "FINALIZADO"],
        help="Filtrar por status (aceita maiúsculas ou minúsculas)"
    )
    cmd_col_filtrar.add_argument("--genero", type=str, help="Filtrar por gênero")
    cmd_col_filtrar.add_argument("--plataforma", type=str, help="Filtrar por plataforma")
    cmd_col_filtrar.add_argument("--nota-minima", type=float, help="Filtrar por nota mínima")
    cmd_col_filtrar.add_argument("--busca", type=str, help="Buscar por parte do título")

    cmd_col_ordenar = sub_col.add_parser("ordenar", help="Ordenar jogos de uma coleção", formatter_class=RichHelpFormatter)
    cmd_col_ordenar.add_argument("--nome", required=True, type=str, help="Nome da coleção")
    cmd_col_ordenar.add_argument("--criterio", choices=["titulo", "horas", "avaliacao", "ano"], required=True, help="Critério de ordenação")


def _adicionar_jogo(subparsers, parsers_modulos: dict) -> None:
    parser_jogo = subparsers.add_parser("jogo", help="Gerenciar jogos no catálogo", formatter_class=RichHelpFormatter)
    parsers_modulos["jogo"] = parser_jogo
    sub_jogo = parser_jogo.add_subparsers(dest="acao", parser_class=CustomArgumentParser)

    cmd_jogo_add = sub_jogo.add_parser("adicionar", help="Adicionar um novo jogo a uma coleção", formatter_class=RichHelpFormatter)
    # --colecao é OPCIONAL (padrão "Geral")
    cmd_jogo_add.add_argument("--colecao", type=str, default="Geral", help="Nome da coleção destino (opcional, padrão: Geral)")
    cmd_jogo_add.add_argument("--titulo", required=True, type=str, help="Título do jogo")
    cmd_jogo_add.add_argument("--genero", required=True, type=str, help="Gênero principal")
    # --plataforma é OPCIONAL: se não for informada, usa a plataforma_principal do settings.json
    cmd_jogo_add.add_argument("--plataforma", choices=["pc", "console", "mobile", "outra"], help="Plataforma principal (opcional, padrão: plataforma_principal do settings.json)")
    cmd_jogo_add.add_argument("--ano", type=int, default=None, help="Ano de lançamento (opcional)")
    # --modo é OPCIONAL (padrão "padrao"): define qual classe de jogo será criada
    cmd_jogo_add.add_argument(
        "--modo",
        choices=["padrao", "campanha", "competitivo", "cooperativo", "campanhacoop"],
        default="padrao",
        help="Modo do jogo, define a classe usada (opcional, padrão: padrao)"
    )
    cmd_jogo_add.add_argument("--requisitos", type=str, default="", help="Requisitos mínimos (PC)")
    cmd_jogo_add.add_argument("--loja", type=str, default="Steam", help="Loja digital (PC)")
    cmd_jogo_add.add_argument("--console", type=str, default="Console", help="Nome do console (Console)")
    cmd_jogo_add.add_argument("--midia-fisica", action="store_true", help="Se possui mídia física (Console)")
    cmd_jogo_add.add_argument("--tamanho", type=float, default=0.0, help="Tamanho em MB (Mobile)")
    cmd_jogo_add.add_argument("--ranking", type=str, default="Unranked", help="Elo ou divisão atual (modo competitivo)")
    cmd_jogo_add.add_argument("--max-jogadores", type=int, default=4, help="Máximo de jogadores por partida (modos cooperativo e campanhacoop)")
    cmd_jogo_add.add_argument("--progresso-individual", action="store_true", help="Progresso NÃO compartilhado entre os jogadores (modo campanhacoop, padrão: compartilhado)")

    cmd_jogo_prog = sub_jogo.add_parser("progresso", help="Atualizar horas jogadas", formatter_class=RichHelpFormatter)
    cmd_jogo_prog.add_argument("--colecao", type=str, default="Geral", help="Nome da coleção (opcional, padrão: Geral)")
    cmd_jogo_prog.add_argument("--titulo", required=True, type=str, help="Título do jogo")
    cmd_jogo_prog.add_argument("--horas", required=True, type=float, help="Horas a adicionar")

    cmd_jogo_fin = sub_jogo.add_parser("finalizar", help="Marcar jogo como FINALIZADO (exige pelo menos 1h registrada)", formatter_class=RichHelpFormatter)
    cmd_jogo_fin.add_argument("--colecao", type=str, default="Geral", help="Nome da coleção (opcional, padrão: Geral)")
    cmd_jogo_fin.add_argument("--titulo", required=True, type=str, help="Título do jogo")

    cmd_jogo_aval = sub_jogo.add_parser("avaliar", help="Atribuir nota (0.0 a 10.0) a um jogo FINALIZADO", formatter_class=RichHelpFormatter)
    cmd_jogo_aval.add_argument("--colecao", type=str, default="Geral", help="Nome da coleção (opcional, padrão: Geral)")
    cmd_jogo_aval.add_argument("--titulo", required=True, type=str, help="Título do jogo")
    cmd_jogo_aval.add_argument("--nota", required=True, type=float, help="Nota de 0.0 a 10.0")

    cmd_jogo_rein = sub_jogo.add_parser("reiniciar", help="Zerar horas e voltar status para JOGANDO", formatter_class=RichHelpFormatter)
    cmd_jogo_rein.add_argument("--colecao", type=str, default="Geral", help="Nome da coleção (opcional, padrão: Geral)")
    cmd_jogo_rein.add_argument("--titulo", required=True, type=str, help="Título do jogo")

    cmd_jogo_rem = sub_jogo.add_parser("remover", help="Remover jogo de uma coleção", formatter_class=RichHelpFormatter)
    cmd_jogo_rem.add_argument("--colecao", type=str, default="Geral", help="Nome da coleção (opcional, padrão: Geral)")
    cmd_jogo_rem.add_argument("--titulo", required=True, type=str, help="Título do jogo")


def _adicionar_settings(subparsers, parsers_modulos: dict) -> None:
    parser_set = subparsers.add_parser("settings", help="Ver ou alterar as configurações (settings.json)", formatter_class=RichHelpFormatter)
    parsers_modulos["settings"] = parser_set
    sub_set = parser_set.add_subparsers(dest="acao", parser_class=CustomArgumentParser)

    sub_set.add_parser("ver", help="Exibir as configurações atuais", formatter_class=RichHelpFormatter)

    cmd_set_def = sub_set.add_parser("definir", help="Alterar as configurações", formatter_class=RichHelpFormatter)
    cmd_set_def.add_argument("--meta", type=int, help="Meta anual de jogos finalizados")
    cmd_set_def.add_argument("--limite-jogando", type=int, help="Máximo de jogos simultâneos com status JOGANDO")
    cmd_set_def.add_argument("--plataforma-principal", choices=["pc", "console", "mobile", "outra"], help="Plataforma principal")
    cmd_set_def.add_argument("--generos-favoritos", type=str, help="Gêneros favoritos separados por vírgula")


def _adicionar_relatorio(subparsers, parsers_modulos: dict) -> None:
    parser_rel = subparsers.add_parser("relatorio", help="Exibir relatórios e estatísticas", formatter_class=RichHelpFormatter)
    parsers_modulos["relatorio"] = parser_rel
    sub_rel = parser_rel.add_subparsers(dest="acao", parser_class=CustomArgumentParser)
    sub_rel.add_parser("geral", help="Exibir relatório geral do catálogo", formatter_class=RichHelpFormatter)


def criar_parser() -> tuple[CustomArgumentParser, dict]:
    """Configura o parser principal e subcomandos usando CustomArgumentParser."""
    parser = CustomArgumentParser(
        description=" [bold cyan]Catálogo de Jogos Virtuais[/bold cyan] - Interface via Linha de Comando",
        formatter_class=RichHelpFormatter
    )

    subparsers = parser.add_subparsers(
        dest="comando_principal",
        help="Comandos principais",
        parser_class=CustomArgumentParser
    )

    parsers_modulos = {}
    _adicionar_usuario(subparsers, parsers_modulos)
    _adicionar_colecao(subparsers, parsers_modulos)
    _adicionar_jogo(subparsers, parsers_modulos)
    _adicionar_settings(subparsers, parsers_modulos)
    _adicionar_relatorio(subparsers, parsers_modulos)

    return parser, parsers_modulos