from src.models.colecao import Colecao

def gerar_relatorio_geral(colecoes: list[Colecao]) -> dict:
    """Gera dados estatísticos sobre o catálogo de jogos do utilizador."""
    total_jogos = sum(col.total_jogos() for col in colecoes)
    total_horas = sum(col.total_horas_jogadas() for col in colecoes)
    
    return {
        "total_colecoes": len(colecoes),
        "total_jogos": total_jogos,
        "total_horas_jogadas": total_horas
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