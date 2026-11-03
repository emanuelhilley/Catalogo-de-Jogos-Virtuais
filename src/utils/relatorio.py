""" Relatórios e estatísticas do catálogo de jogos. """
from typing import Optional
from src.models.colecao import Colecao
from src.models.jogo import Jogo

STATUS_ORDEM = ("NÃO INICIADO", "JOGANDO", "FINALIZADO")

def _jogos_unicos(colecoes: list[Colecao]) -> list[Jogo]:
    """Reúne os jogos de todas as coleções. Um jogo em várias coleções conta só uma vez (título + plataforma)."""
    jogos_unicos = {}

    for col in colecoes:
        for jogo in col.listar_jogos():
            chave = (jogo.titulo.strip().lower(), jogo.plataforma.strip().lower())
            if chave not in jogos_unicos:
                jogos_unicos[chave] = jogo

    return list(jogos_unicos.values())

def gerar_relatorio_geral(colecoes: list[Colecao], generos_favoritos: Optional[list[str]] = None) -> dict:
    """Gera dados estatísticos sobre o catálogo de jogos do utilizador."""
    jogos = _jogos_unicos(colecoes)

    total_jogos = len(jogos)
    total_horas = sum(j.horas_jogadas for j in jogos)

    # média de avaliação: considera apenas os jogos finalizados que têm nota
    notas = [j.avaliacao for j in jogos if j.status == "FINALIZADO" and j.avaliacao is not None]
    media_avaliacao = round(sum(notas) / len(notas), 1) if notas else None

    # percentual de jogos por status
    percentual_por_status = {}
    for status in STATUS_ORDEM:
        quantidade = sum(1 for j in jogos if j.status == status)
        percentual_por_status[status] = round(quantidade / total_jogos * 100, 1) if total_jogos else 0.0

    # top 5 mais jogados: sorted() usa o __lt__ do Jogo (ordenação por horas jogadas)
    jogados = [j for j in jogos if j.horas_jogadas > 0]
    top5 = sorted(jogados, reverse=True)[:5]

    # horas nos gêneros favoritos (vêm do settings.json)
    horas_generos_favoritos = None
    if generos_favoritos:
        favoritos = {g.strip().lower() for g in generos_favoritos}
        horas_generos_favoritos = round(sum(j.horas_jogadas for j in jogos if j.genero.strip().lower() in favoritos), 1)

    return {
        "total_colecoes": len(colecoes),
        "total_jogos": total_jogos,
        "total_horas_jogadas": round(total_horas, 1),
        "media_avaliacao_finalizados": media_avaliacao,
        "percentual_por_status": percentual_por_status,
        "top5_mais_jogados": top5,
        "horas_generos_favoritos": horas_generos_favoritos
    }

def exibir_relatorio_terminal(colecoes: list[Colecao], generos_favoritos: Optional[list[str]] = None) -> None:
    """Imprime um relatório formatado no terminal."""
    stats = gerar_relatorio_geral(colecoes, generos_favoritos)
    media = stats["media_avaliacao_finalizados"]
    media_txt = f"{media:.1f}/10" if media is not None else "Sem jogos avaliados"

    print("\n" + "="*40)
    print(" RELATÓRIO GERAL DO CATÁLOGO DE JOGOS")
    print("="*40)
    print(f" Total de Coleções: {stats['total_colecoes']}")
    print(f" Total de Jogos:    {stats['total_jogos']}")
    print(f" Total de Horas:    {stats['total_horas_jogadas']:.1f}h")
    print(f" Média das Notas (finalizados): {media_txt}")
    if stats["horas_generos_favoritos"] is not None:
        print(f" Horas em Gêneros Favoritos:    {stats['horas_generos_favoritos']:.1f}h")

    print("-"*40)
    print(" Jogos por Status:")
    for status, percentual in stats["percentual_por_status"].items():
        print(f"   {status}: {percentual:.1f}%")

    print("-"*40)
    print(" Top 5 Jogos Mais Jogados:")
    if not stats["top5_mais_jogados"]:
        print("   (nenhum jogo com horas registradas)")
    for posicao, jogo in enumerate(stats["top5_mais_jogados"], start=1):
        print(f"   {posicao}. {jogo.titulo} [{jogo.plataforma}] - {jogo.horas_jogadas:.1f}h")
    print("="*40 + "\n")