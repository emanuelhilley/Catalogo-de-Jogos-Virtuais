# Catálogo de Jogos Virtuais

## Sistema projetado para **auxiliar jogadores na organização** e no **acompanhamento da sua coleção pessoal** de **jogos.**

### O objetivo do sistema é permitir que o utilizador consiga:

- **Cadastrar Jogos:** Guardar informações essenciais sobre cada jogo (título, género, plataforma, horas jogadas e estado atual, como Não Iniciado, Jogando ou Finalizado).

- **Tratar Diferentes Tipos de Experiências:** O sistema diferencia e regista métricas específicas para jogos de campanha (progresso da história), competitivos (vitórias/derrotas e ranking) e cooperativos (sessões e número de jogadores).

- **Controlar o Progresso:** Atualizar as horas jogadas, redefinir estados e aplicar regras de negócio (por exemplo, impedir a marcação de um jogo como finalizado se este tiver menos de 1 hora jogada).

- **Organizar Coleções:** Criar e gerir listas personalizadas (como "Favoritos" ou "Jogos a Zerar").

- **Analisar o Desempenho:** Gerar relatórios com dados estatísticos, como o total de horas jogadas, a média de avaliações dos jogos concluídos e os Top 5 jogos mais jogados.


## UML

#### 1. Classe Base: `Jogo`
| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `titulo` | `str` | Público (`+`) | Nome do jogo |
| **Atributo** | `genero` | `str` | Público (`+`) | Gênero do jogo |
| **Atributo** | `plataforma` | `str` | Público (`+`) | Plataforma (PC, Console, Mobile) |
| **Atributo** | `status` | `str` | Público (`+`) | Estado atual ("NÃO INICIADO", "JOGANDO", "FINALIZADO")    |
| **Atributo** | `horas_jogadas` | `float` | Protegido (`#`) | Total de horas acumuladas (≥ 0) |
| **Atributo** | `avaliacao` | `float` | Protegido (`#`) | Nota de 0 a 10 (permitida apenas se o jogo estiver "FINALIZADO") |
| **Método** | `atualizar_progresso()` | `None` | Público (`+`) | Atualiza horas e altera o status |
| **Método** | `reiniciar()` | `None` | Público (`+`) | Zera horas e volta para "JOGANDO" |
| **Método** | `avaliar()` | `None` | Público (`+`) | Atribui a nota após validar se o jogo foi finalizado |


#### 2. Subclasse: `JogoCampanha` (Herda de `Jogo`)
| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `capitulos_concluidos`| `int` | Público (`+`) | Total de capítulos finalizados |
| **Atributo** | `percentual_conclusao` | `float` | Público (`+`) | Progresso da história (0 a 100%) |

#### 3. Subclasse: `JogoCompetitivo` (Herda de `Jogo`)
Especialização para jogos focados em partidas ranqueadas e confrontos contra outros jogadores.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `partidas_jogadas` | `int` | Público (`+`) | Total de partidas disputadas |
| **Atributo** | `vitorias` | `int` | Público (`+`) | Quantidade total de vitórias |
| **Atributo** | `derrotas` | `int` | Público (`+`) | Quantidade total de derrotas |
| **Atributo** | `ranking` | `str` | Público (`+`) | Elo ou divisão atual (ex: "Ouro", "Radiante") |
| **Método** | `taxa_vitoria()` | `float` | Público (`+`) | Calcula e devolve a % de vitórias do jogador |

---

#### 4. Subclasse: `JogoCooperativo` (Herda de `Jogo`)
Especialização para jogos focados em cooperação e trabalho em equipe.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `max_jogadores` | `int` | Público (`+`) | Limite máximo de pessoas no grupo |
| **Atributo** | `sessoes_cooperativas`| `int` | Público (`+`) | Número de sessões jogadas em equipe |

---

#### 5. Subclasse: `JogoCampanhaCoop` (Herda de `JogoCampanha` e `JogoCooperativo`)
Representa jogos focados na história principal que podem ser concluídos cooperativamente em grupo.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `modo_progresso_compartilhado` | `bool` | Público (`+`) | Indica se o progresso da história conta para todos os jogadores |
| **Método** | `resumo_coop()`| `str` | Público (`+`) | Exibe o total de capítulos concluídos junto com o limite de jogadores |


---

#### 6. Classe de Organização: `Colecao`
Responsável por agrupar e gerenciar listas personalizadas de jogos no catálogo.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `nome` | `str` | Público (`+`) | Nome da lista (ex: "Favoritos", "Zerar em 2026") |
| **Atributo** | `jogos` | `list[Jogo]` | Público (`+`) | Lista armazenando os objetos do tipo `Jogo` |
| **Método** | `adicionar_jogo()` | `None` | Público (`+`) | Insere um novo objeto de jogo na coleção |
| **Método** | `remover_jogo()` | `None` | Público (`+`) | Remove um jogo específico da coleção |
| **Método** | `listar_jogos()` | `list[Jogo]` | Público (`+`) | Retorna a lista contendo todos os jogos da coleção |

---

#### 7. Classe de Organização: `Usuario` (Opcional)
Representa o perfil do usuário e gerencia suas coleções pessoais.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Atributo** | `nome` | `str` | Público (`+`) | Nome ou apelido do jogador |
| **Atributo** | `colecoes` | `list[Colecao]` | Público (`+`) | Lista contendo as coleções criadas pelo usuário |
| **Método** | `criar_colecao()` | `None` | Público (`+`) | Instancia e adiciona uma nova `Colecao` ao perfil |
| **Método** | `remover_colecao()`| `None` | Público (`+`) | Elimina uma `coleção` existente da lista |
