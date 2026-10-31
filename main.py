import sys
from src.models.usuario import Usuario
from src.models.jogo import JogoPc, JogoConsole, JogoMobile
from src.utils.persistencia import salvar_colecoes, carregar_colecoes
from src.utils.relatorio import exibir_relatorio_terminal

def menu_principal():
    colecoes = carregar_colecoes()
    if not colecoes:
        from src.models.colecao import Colecao
        col_padrao = Colecao("Geral")
        colecoes = [col_padrao]

    usuario = Usuario("Jogador", "jogador@email.com", meta_jogos_ano=5)
    usuario._colecoes = colecoes # Atribui as coleções carregadas ao perfil do utilizador.

    while True:
        print("\n===  CATÁLOGO DE JOGOS VIRTUAIS  ===")
        print("1. Adicionar Jogo")
        print("2. Listar / Filtrar Jogos")
        print("3. Atualizar Progresso de Jogo")
        print("4. Ver Relatório Geral")
        print("5. Ver Meta Anual")
        print("6. Salvar e Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título: ").strip()
            genero = input("Gênero: ").strip()
            tipo = input("Plataforma (1-PC, 2-Console, 3-Mobile): ").strip()

            if tipo == "1":
                loja = input("Loja Digital: ").strip() or "Steam"
                req = input("Requisitos Mínimos: ").strip()
                jogo = JogoPc(titulo, genero, req, loja)
            elif tipo == "2":
                console = input("Nome do Console: ").strip() or "Console"
                jogo = JogoConsole(titulo, genero, console)
            else:
                tamanho_str = input("Tamanho em MB: ").strip() or "0"
                tamanho_mb = float(tamanho_str)
                jogo = JogoMobile(titulo, genero, tamanho_mb)

            usuario.listar_colecoes()[0].adicionar_jogo(jogo) # Pega na primeira coleção do utilizador (a coleção "Geral") e adiciona o jogo criado a essa lista.
            print(f" Jogo '{titulo}' adicionado com sucesso!")

        elif opcao == "2":
            col = usuario.listar_colecoes()[0]
            print("\n--- Opções de Filtro ---")
            print("1. Todos | 2. Por Gênero | 3. Por Status | 4. Por Plataforma")
            sub = input("Escolha: ").strip()
            
            jogos = col.listar_jogos()
            if sub == "2":
                g = input("Gênero: ").strip()
                jogos = col.filtrar_por_genero(g)
            elif sub == "3":
                s = input("Status (NÃO INICIADO / JOGANDO / FINALIZADO): ").strip()
                jogos = col.filtrar_por_status(s)
            elif sub == "4":
                p = input("Plataforma: ").strip()
                jogos = col.filtrar_por_plataforma(p)

            print(f"\n--- Jogos Encontrados ({len(jogos)}) ---")
            for j in jogos:
                print(f"• {j.titulo} [{j.plataforma}] - Status: {j.status} | Horas: {j.horas_jogadas}h")

        elif opcao == "3":
            col = usuario.listar_colecoes()[0]
            titulo = input("Título do jogo a atualizar: ").strip()
            jogo = col.buscar_por_titulo(titulo)
            if jogo:
                horas = float(input("Horas a adicionar: ") or 0)
                status = input("Novo Status (JOGANDO / FINALIZADO): ").strip().upper()
                jogo.atualizar_progresso(horas)
                if status:
                    jogo.status = status
                if status == "FINALIZADO":
                    nota = float(input("Nota (0 a 10): ") or 10)
                    jogo.avaliar(nota)
                print(" Progresso atualizado!")
            else:
                print(" Jogo não encontrado.")

        elif opcao == "4":
            exibir_relatorio_terminal(usuario.listar_colecoes())

        elif opcao == "5":
            prog = usuario.progresso_meta()
            print(f"\n Meta Anual: {prog['meta']} jogos finalizados")
            print(f" Concluídos: {prog['finalizados']} ({prog['percentual']}%)")
            print(f"Status: {'Atingida ' if prog['atingida'] else 'Em andamento '}")

        elif opcao == "6":
            salvar_colecoes(usuario.listar_colecoes())
            print("\n Dados salvos com sucesso.")
            sys.exit()
if __name__ == "__main__":
    menu_principal()