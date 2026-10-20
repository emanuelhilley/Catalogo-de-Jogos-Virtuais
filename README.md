# Catálogo de Jogos Virtuais

## Sistema projetado para **auxiliar jogadores na organização** e no **acompanhamento da sua coleção pessoal** de **jogos.**
## Muitas vezes, quem joga em diversas **plataformas** (como PC, consoles e dispositivos móveis) encontra dificuldades para acompanhar o **progresso** dos seus **jogos**, registrar **metas concluídas** ou analisar o **tempo investido em cada experiência.** Este sistema resolve esse problema ao centralizar todas essas informações em um único **catálogo.**

### O objetivo do sistema é permitir que o utilizador consiga:

- **Cadastrar Jogos:** Guardar informações essenciais sobre cada jogo (título, género, plataforma, horas jogadas e estado atual, como Não Iniciado, Jogando ou Finalizado).

- **Tratar Diferentes Tipos de Experiências:** O sistema diferencia e regista métricas específicas para jogos de campanha (progresso da história), competitivos (vitórias/derrotas e ranking) e cooperativos (sessões e número de jogadores).

- **Controlar o Progresso:** Atualizar as horas jogadas, redefinir estados e aplicar regras de negócio (por exemplo, impedir a marcação de um jogo como finalizado se este tiver menos de 1 hora jogada).

- **Organizar Coleções:** Criar e gerir listas personalizadas (como "Favoritos" ou "Jogos a Zerar").

- **Analisar o Desempenho:** Gerar relatórios com dados estatísticos, como o total de horas jogadas, a média de avaliações dos jogos concluídos e os Top 5 jogos mais jogados.


## UML

#### 1. Classe Base: `Jogo`
Representa a classe base para todos os jogos do catálogo, aplicando encapsulamento com getters e setters.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `_titulo` | `str` | Privado (`-`) | Nome do jogo |
| **Atributo** | `_genero` | `str` | Privado (`-`) | Gênero do jogo |
| **Atributo** | `_plataforma` | `str` | Privado (`-`) | Plataforma (PC, Console, Mobile) |
| **Atributo** | `_status` | `str` | Privado (`-`) | Estado atual ("NÃO INICIADO", "JOGANDO", "FINALIZADO") |
| **Atributo** | `_horas_jogadas` | `float` | Protegido (`#`) | Total de horas acumuladas |
| **Atributo** | `_avaliacao` | `float` | Protegido (`#`) | Nota de 0 a 10 (permitida apenas se o jogo estiver "FINALIZADO") |
| **Método** | `atualizar_progresso()` | `None` | Público (`+`) | Atualiza horas e altera o status |
| **Método** | `reiniciar()` | `None` | Público (`+`) | Zera horas e volta para "JOGANDO" |
| **Método** | `avaliar()` | `None` | Público (`+`) | Atribui a nota após validar se o jogo foi finalizado |

---

#### 1.1. Subclasses por Plataforma (Herdam de `Jogo`)
Especializações para jogos de acordo com o dispositivo/plataforma.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Subclasse** | `JogoPc` | `Jogo` | Público (`+`) | Destinado para jogos de PC |
| **Atributo** | `requisitos_minimos` | `str` | Público (`+`) | Especificações técnicas mínimas exigidas |
| **Atributo** | `loja_digital` | `str` | Público (`+`) | Loja onde o jogo foi adquirido (ex: "Steam", "Epic Games") |
| **Subclasse** | `JogoConsole` | `Jogo` | Público (`+`) | Destinado para jogos de Console |
| **Atributo** | `nome_console` | `str` | Público (`+`) | Nome do console (ex: "PlayStation 5", "Xbox Series X") |
| **Atributo** | `midia_fisica` | `bool` | Público (`+`) | Indica se o jogo é em disco/cartucho físico |
| **Subclasse** | `JogoMobile` | `Jogo` | Público (`+`) | Destinado para jogos mobiles |
| **Atributo** | `tamanho_mb` | `float` | Público (`+`) | Tamanho de armazenamento do jogo em Megabytes |
| **Atributo** | `compras_no_app` | `bool` | Público (`+`) | Indica se o jogo possui microtransações |

---

#### 2. Subclasse: `JogoCampanha` (Herda de `Jogo`)
Especialização para jogos focados em modo história e campanha single-player.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `capitulos_concluidos` | `int` | Público (`+`) | Total de capítulos finalizados |
| **Atributo** | `percentual_conclusao` | `float` | Público (`+`) | Progresso da história (0 a 100%) |

---

#### 3. Subclasse: `JogoCompetitivo` (Herda de `Jogo`)
Especialização para jogos focados em partidas ranqueadas e confrontos contra outros jogadores.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `partidas_jogadas` | `int` | Público (`+`) | Total de partidas disputadas |
| **Atributo** | `vitorias` | `int` | Público (`+`) | Quantidade total de vitórias |
| **Atributo** | `derrotas` | `int` | Público (`+`) | Quantidade total de derrotas |
| **Atributo** | `ranking` | `str` | Público (`+`) | Elo ou divisão atual (ex: "Ouro", "Radiante") |
| **Método** | `taxa_vitoria()` | `float` | Público (`+`) | Calcula e devolve a % de vitórias do jogador |

---

#### 4. Subclasse: `JogoCooperativo` (Herda de `Jogo`)
Especialização para jogos focados em cooperação e trabalho em equipe.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `max_jogadores` | `int` | Público (`+`) | Limite máximo de pessoas no grupo |
| **Atributo** | `sessoes_cooperativas` | `int` | Público (`+`) | Número de sessões jogadas em equipe |

---

#### 5. Subclasse: `JogoCampanhaCoop` (Herda de `JogoCampanha` e `JogoCooperativo`)
Representa jogos focados na história principal que podem ser concluídos cooperativamente em grupo.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `modo_progresso_compartilhado` | `bool` | Público (`+`) | Indica se o progresso da história conta para todos os jogadores |
| **Método** | `resumo_coop()` | `str` | Público (`+`) | Exibe o total de capítulos concluídos junto com o limite de jogadores |

---

#### 6. Classe de Organização: `Colecao`
Responsável por agrupar e gerenciar listas personalizadas de jogos no catálogo.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `nome` | `str` | Público (`+`) | Nome da lista (ex: "Favoritos", "Zerar em 2026") |
| **Atributo** | `_jogos` | `list[Jogo]` | Privado (`-`) | Lista privada armazenando os objetos do tipo `Jogo` |
| **Método** | `adicionar_jogo()` | `None` | Público (`+`) | Insere um novo objeto de jogo na coleção |
| **Método** | `remover_jogo()` | `bool` | Público (`+`) | Remove um jogo específico da coleção pelo título |
| **Método** | `listar_jogos()` | `list[Jogo]` | Público (`+`) | Retorna a lista contendo todos os jogos da coleção |
| **Método** | `buscar_por_titulo()` | `Optional[Jogo]` | Público (`+`) | Busca e retorna um jogo específico pelo título |
| **Método** | `atualizar_jogo()` | `bool` | Público (`+`) | Atualiza atributos de um jogo existente utilizando `**kwargs` |
| **Método** | `total_jogos()` | `int` | Público (`+`) | Retorna a quantidade total de jogos na coleção |
| **Método** | `total_horas_jogadas()` | `float` | Público (`+`) | Retorna a soma total de horas jogadas na coleção |

---

#### 7. Classe de Organização: `Usuario`
Representa o perfil do usuário e gerencia suas coleções pessoais.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `nome` | `str` | Público (`+`) | Nome ou apelido do jogador |
| **Atributo** | `_email` | `str` | Privado (`-`) | E-mail do usuário validado via property/setter |
| **Atributo** | `_colecoes` | `list[Colecao]` | Privado (`-`) | Lista privada contendo as coleções criadas pelo usuário |
| **Método** | `criar_colecao()` | `Colecao` | Público (`+`) | Instancia e adiciona uma nova `Colecao` ao perfil |
| **Método** | `listar_colecoes()` | `list[Colecao]` | Público (`+`) | Retorna todas as coleções do usuário |
| **Método** | `remover_colecao()` | `bool` | Público (`+`) | Elimina uma coleção existente no perfil |
| **Método** | `buscar_colecao()` | `Optional[Colecao]` | Público (`+`) | Busca e retorna uma coleção específica pelo nome |

##  Testes Automatizados

Para rodar os testes automatizados do projeto, execute o comando abaixo no terminal:

```bash
pytest

```
###  O projeto conta com 17 testes automatizados validados via pytest, cobrindo as regras de negócio das classes (Jogo, Colecao, Usuario), a persistência em JSON e a geração do relatório estatístico.

## Estrutura do Projeto

```text

├── data/
│   └── colecoes.json
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── colecao.py
│   │   ├── jogo.py
│   │   └── usuario.py
│   └── utils/
│       ├── __init__.py
│       ├── persistencia.py
│       └── relatorio.py
├── tests/
│   ├── __init__.py
│   ├── test_colecao.py
│   ├── test_jogo.py
│   ├── test_persistencia.py
│   └── test_usuario.py
└── README.md
