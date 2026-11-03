""" Tratamento dos comandos do módulo 'jogo'. """
from rich.panel import Panel

from src.cli.exibicao import console, nome_modo, detalhes_modo, renderizar_tabela_jogos
from src.cli.auxiliares import colecao_ou_erro, jogo_ou_erro
from src.cli.fabrica import instanciar_jogo
from src.utils.persistencia import salvar_colecoes
from src.utils.regras import verificar_limite_jogando, aviso_meta


def _adicionar(args, colecoes, colecao, config) -> None:
    try:
        if args.plataforma is None:
            args.plataforma = str(config["plataforma_principal"]).lower() # usa a plataforma principal do settings.json

        novo_jogo = instanciar_jogo(args)
        novo_jogo.ano_lancamento = args.ano

        colecao.adicionar_jogo(novo_jogo)
        salvar_colecoes(colecoes)

        linhas = [
            f" [bold]Modo:[/bold] {nome_modo(novo_jogo)}",
            *detalhes_modo(novo_jogo),
            f" [bold]Coleção Destino:[/bold] {colecao.nome}",
        ]
        if colecao.nome.lower() != "geral":
            linhas.append(" [bold]Espelhado automaticamente em:[/bold] Geral")

        console.print(Panel(
            f"[bold green]✅ Jogo '{novo_jogo.titulo}' adicionado com sucesso![/bold green]\n\n"
            + "\n".join(linhas),
            title="Jogo Registrado", border_style="green"
        ))
    except (ValueError, TypeError) as e:
        console.print(Panel(f"[bold red]❌ Erro ao adicionar jogo:[/bold red] {e}", border_style="red"))


def _progresso(args, colecoes, colecao, config) -> None:
    jogo = jogo_ou_erro(colecao, args.titulo)
    if not jogo:
        return

    try:
        if jogo.status == "NÃO INICIADO": # só um jogo novo passa a ocupar uma vaga de 'JOGANDO'
            verificar_limite_jogando(colecoes, config["limite_jogando"])

        jogo.atualizar_progresso(args.horas)
        salvar_colecoes(colecoes)
        console.print(Panel(
            f"[bold green] Progresso atualizado com sucesso![/bold green]\n\n"
            f" [bold]Jogo:[/bold] {jogo.titulo}\n"
            f" [bold]Horas Totais:[/bold] {jogo.horas_jogadas:.1f}h\n"
            f" [bold]Status Atual:[/bold] {jogo.status}",
            title="Progresso Registrado", border_style="green"
        ))
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Erro:[/bold red] {e}", border_style="red"))


def _finalizar(args, colecoes, colecao, config) -> None:
    jogo = jogo_ou_erro(colecao, args.titulo)
    if not jogo:
        return

    try:
        jogo.finalizar() # valida a regra de pelo menos 1h registrada
        salvar_colecoes(colecoes)
        console.print(Panel(
            f"[bold green] Jogo '{jogo.titulo}' marcado como FINALIZADO![/bold green]\n\n"
            f"Agora você já pode atribuir uma nota com: python3 main.py jogo avaliar --titulo \"{jogo.titulo}\" --nota X",
            title="Status Atualizado", border_style="green"
        ))

        aviso = aviso_meta(colecoes, config["meta_anual_jogos"]) # avisa se ainda falta para bater a meta anual
        if aviso:
            console.print(Panel(aviso, title="Aviso de Meta", border_style="yellow"))
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Não foi possível finalizar:[/bold red] {e}", border_style="red"))


def _avaliar(args, colecoes, colecao, config) -> None:
    jogo = jogo_ou_erro(colecao, args.titulo)
    if not jogo:
        return

    try:
        jogo.avaliar(args.nota) # o setter exige status FINALIZADO e nota entre 0 e 10
        salvar_colecoes(colecoes)
        console.print(Panel(
            f"[bold green] Jogo '{jogo.titulo}' avaliado com sucesso![/bold green]\n\n"
            f" [bold]Nota Atribuída:[/bold] {jogo.avaliacao}/10.0",
            title="Avaliação Salva", border_style="green"
        ))
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Não foi possível avaliar:[/bold red] {e}", border_style="red"))


def _reiniciar(args, colecoes, colecao, config) -> None:
    jogo = jogo_ou_erro(colecao, args.titulo)
    if not jogo:
        return

    try:
        if jogo.status != "JOGANDO": # reiniciar volta o jogo para 'JOGANDO', então também ocupa uma vaga
            verificar_limite_jogando(colecoes, config["limite_jogando"])

        jogo.reiniciar()
        salvar_colecoes(colecoes)
        console.print(Panel(f"[bold yellow] Jogo '{jogo.titulo}' foi reiniciado com sucesso.[/bold yellow]", title="Jogo Reiniciado", border_style="yellow"))
    except ValueError as e:
        console.print(Panel(f"[bold red]❌ Não foi possível reiniciar:[/bold red] {e}", border_style="red"))


def _remover(args, colecoes, colecao, config) -> None:
    sucesso = colecao.remover_jogo(args.titulo)
    if not sucesso:
        console.print(Panel(f"[bold red]❌ Jogo '{args.titulo}' não foi encontrado na coleção '{colecao.nome}'.[/bold red]", border_style="red"))
        renderizar_tabela_jogos(colecao.nome, colecao.listar_jogos())
        return

    # 'Geral' reúne todos os jogos: removê-lo de lá também o remove das outras coleções
    da_geral = colecao.nome.lower() == "geral"
    if da_geral:
        for outra in colecoes:
            outra.remover_jogo(args.titulo)

    salvar_colecoes(colecoes)
    aviso = " e de todas as outras coleções" if da_geral else ""
    console.print(Panel(f"[bold green] Jogo '{args.titulo}' removido da coleção '{colecao.nome}'{aviso}.[/bold green]", border_style="green"))


ACOES = {
    "adicionar": _adicionar,
    "progresso": _progresso,
    "finalizar": _finalizar,
    "avaliar": _avaliar,
    "reiniciar": _reiniciar,
    "remover": _remover,
}


def tratar_jogo(args, colecoes, config) -> None:
    """Encontra a coleção alvo (padrão: Geral) e chama a função da ação escolhida."""
    nome_colecao = args.colecao if getattr(args, "colecao", None) else "Geral"
    colecao = colecao_ou_erro(colecoes, nome_colecao)
    if not colecao:
        return

    ACOES[args.acao](args, colecoes, colecao, config)