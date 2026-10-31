from src.models.colecao import Colecao

def gerar_relatorio_geral(colecoes: list[Colecao]) -> dict:
    """Gera dados estatísticos sobre o catálogo de jogos do utilizador."""
    jogos_unicos = {}

    for col in colecoes:
        for jogo in col.listar_jogos():
            chave = jogo.titulo.strip().lower()
            if chave not in jogos_unicos:
                jogos_unicos[chave] = jogo

    total_jogos = len(jogos_unicos)
    total_horas = sum(j.horas_jogadas for j in jogos_unicos.values())
    
    return {
        "total_colecoes": len(colecoes),
        "total_jogos": total_jogos,
        "total_horas_jogadas": round(total_horas, 1)
    }

def exibir_relatorio_terminal(colecoes: list[Colecao]) -> None:
    """Imprime um relatório formatado no terminal."""
    stats = gerar_relatorio_geral(colecoes)
    print("\n" + "="*40)
    print(" RELATÓRIO GERAL DO CATÁLOGO DE JOGOS")
    print("="*40)
    print(f" Total de Coleções: {stats['total_colecoes']}")
    print(f" Total de Jogos:    {stats['total_jogos']}")
    print(f" Total de Horas:    {stats['total_horas_jogadas']:.1f}h")
    print("="*40 + "\n")