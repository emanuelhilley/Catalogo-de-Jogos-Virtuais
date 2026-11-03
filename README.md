# Catálogo de Jogos Virtuais

## Sistema projetado para **auxiliar jogadores na organização** e no **acompanhamento da sua coleção pessoal** de **jogos.**
## Muitas vezes, quem joga em diversas **plataformas** (como PC, consoles e dispositivos móveis) encontra dificuldades para acompanhar o **progresso** dos seus **jogos**, registrar **metas concluídas** ou analisar o **tempo investido em cada experiência.** Este sistema resolve esse problema ao centralizar todas essas informações em um único **catálogo.**

### O objetivo do sistema é permitir que o utilizador consiga:

- **Cadastrar Jogos:** Guardar informações essenciais sobre cada jogo (título, género, plataforma, ano de lançamento, horas jogadas, datas de início e término e estado atual, como Não Iniciado, Jogando ou Finalizado).

- **Tratar Diferentes Tipos de Experiências:** O sistema diferencia e regista métricas específicas para jogos de campanha (progresso da história), competitivos (vitórias/derrotas e ranking) e cooperativos (sessões, número de jogadores e participantes frequentes).

- **Controlar o Progresso:** Atualizar as horas jogadas, redefinir estados e aplicar regras de negócio (por exemplo, impedir a marcação de um jogo como finalizado se este tiver menos de 1 hora jogada).

- **Organizar Coleções:** Criar e gerir listas personalizadas (como "Favoritos" ou "Jogos a Zerar"), com filtros por género, plataforma, status e nota mínima, busca por parte do título e ordenações.

- **Configurar as Regras:** Definir no `settings.json` a meta anual de jogos finalizados, o limite de jogos simultâneos com status "JOGANDO", a plataforma principal e os géneros favoritos.

- **Analisar o Desempenho:** Gerar relatórios com dados estatísticos, como o total de horas jogadas, a média de avaliações dos jogos concluídos e os Top 5 jogos mais jogados.


## Instalação e Execução

Requisitos: **Python 3.10+**. Instale as dependências (`rich`, `rich-argparse` e `pytest`) com:

```bash
pip install -r requirements.txt
```

O sistema é uma **CLI** com subcomandos. Execute sempre a partir da raiz do projeto (onde está o `main.py`):

```bash
python3 main.py                  # ajuda geral
python3 main.py jogo --help      # ajuda de um módulo
```

Módulos e ações disponíveis:

| Módulo | Ações |
|---|---|
| `usuario` | `criar`, `atualizar`, `ver`, `meta` |
| `colecao` | `criar`, `listar`, `ver`, `remover`, `adicionar-jogo`, `filtrar`, `ordenar` |
| `jogo` | `adicionar`, `progresso`, `finalizar`, `avaliar`, `reiniciar`, `remover` |
| `settings` | `ver`, `definir` |
| `relatorio` | `geral` |

Exemplos de uso:

```bash
python3 main.py usuario criar --nome "Maria" --email "maria@email.com" --meta 5
python3 main.py jogo adicionar --titulo "Minecraft" --genero "Sandbox" --plataforma pc --modo cooperativo --max-jogadores 4 --ano 2011
python3 main.py jogo progresso --titulo "Minecraft" --horas 2.5
python3 main.py jogo finalizar --titulo "Minecraft"
python3 main.py jogo avaliar --titulo "Minecraft" --nota 9.5
python3 main.py colecao criar --nome "Jogos com os amigos"
python3 main.py colecao adicionar-jogo --nome "Jogos com os amigos" --titulo "Minecraft"
python3 main.py colecao filtrar --nome Geral --nota-minima 8
python3 main.py colecao ordenar --nome Geral --criterio horas
python3 main.py relatorio geral
```

>  O comando `usuario criar` **reseta** os jogos e coleções anteriores. Para alterar apenas os dados do perfil, use `usuario atualizar`!!!

A pasta `data/` acompanha o repositório com dados de exemplo. As coleções **Geral** (reúne todos os jogos) e **Favoritos** são criadas automaticamente.


## Configurações (`settings.json`)

As regras configuráveis ficam no `settings.json`, na raiz do projeto. Se o arquivo não existir ou faltar alguma chave, são usados valores padrão. Também podem ser alteradas pela CLI com `settings definir`.


## Regras de Negócio

- Um jogo só pode receber avaliação após ser marcado como "FINALIZADO" (nota entre 0 e 10).
- Não é permitido marcar como "FINALIZADO" um jogo com menos de 1h registrada.
- Não é permitido duplicar jogos com mesmo título e plataforma.
- Horas jogadas devem ser ≥ 0 e atualizadas progressivamente.
- O título não pode ser vazio e o status só aceita "NÃO INICIADO", "JOGANDO" ou "FINALIZADO".
- Não é permitido mais de 3 jogos simultâneos com status "JOGANDO" (limite configurável em `limite_jogando`).
- Se o número de jogos finalizados for menor que a meta anual (`meta_anual_jogos`), o sistema emite um aviso.
- Reiniciar um jogo zera as horas e a nota e volta o status para "JOGANDO".


## UML

#### 1. Classe Base: `Jogo`
Representa a classe base para todos os jogos do catálogo.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `_titulo` | `str` | Privado (`-`) | Nome do jogo (não pode ser vazio, validado via property/setter) |
| **Atributo** | `genero` | `str` | Público (`+`) | Gênero do jogo |
| **Atributo** | `plataforma` | `str` | Público (`+`) | Plataforma (PC, Console, Mobile) |
| **Atributo** | `_status` | `str` | Privado (`-`) | Estado atual ("NÃO INICIADO", "JOGANDO", "FINALIZADO"), validado via property/setter |
| **Atributo** | `_horas_jogadas` | `float` | Protegido (`#`) | Total de horas acumuladas |
| **Atributo** | `_avaliacao` | `float` | Protegido (`#`) | Nota de 0 a 10 (permitida apenas se o jogo estiver "FINALIZADO") |
| **Atributo** | `ano_lancamento` | `Optional[int]` | Público (`+`) | Ano de lançamento (opcional) |
| **Atributo** | `data_inicio` | `Optional[date]` | Público (`+`) | Data em que começou a ser jogado (registrada automaticamente) |
| **Atributo** | `data_termino` | `Optional[date]` | Público (`+`) | Data em que foi finalizado (registrada automaticamente) |
| **Método** | `atualizar_progresso()` | `None` | Público (`+`) | Atualiza horas e altera o status |
| **Método** | `finalizar()` | `None` | Público (`+`) | Marca como "FINALIZADO" (exige pelo menos 1h registrada) |
| **Método** | `reiniciar()` | `None` | Público (`+`) | Zera horas e volta para "JOGANDO" |
| **Método** | `avaliar()` | `None` | Público (`+`) | Atribui a nota após validar se o jogo foi finalizado |
| **Método especial** | `__str__()` | `str` | Público (`+`) | Resumo do jogo |
| **Método especial** | `__repr__()` | `str` | Público (`+`) | Exibição detalhada do jogo |
| **Método especial** | `__eq__()` | `bool` | Público (`+`) | Igualdade por título e plataforma |
| **Método especial** | `__lt__()` | `bool` | Público (`+`) | Ordenação por horas jogadas |
| **Método especial** | `__hash__()` | `int` | Público (`+`) | Hash por título e plataforma (necessário ao definir o `__eq__`) |

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

#### 1.2. Mixins (usados na herança múltipla)
Classes auxiliares que guardam os recursos de cada modo de jogo e podem ser combinadas.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Mixin** | `CampanhaMixin` | - | Público (`+`) | Recursos de modo história |
| **Atributo** | `capitulos_concluidos` | `int` | Público (`+`) | Total de capítulos finalizados |
| **Atributo** | `percentual_conclusao` | `float` | Público (`+`) | Progresso da história (0 a 100%) |
| **Mixin** | `CooperativoMixin` | - | Público (`+`) | Recursos de trabalho em equipe |
| **Atributo** | `max_jogadores` | `int` | Público (`+`) | Limite máximo de pessoas no grupo |
| **Atributo** | `sessoes_cooperativas` | `int` | Público (`+`) | Número de sessões jogadas em equipe |
| **Atributo** | `participantes_frequentes` | `list[str]` | Público (`+`) | Jogadores que mais jogam junto |
| **Método** | `adicionar_participante()` | `None` | Público (`+`) | Adiciona um participante sem repetir nomes |

---

#### 2. Subclasse: `JogoCampanha` (Herda de `CampanhaMixin` e `Jogo`)
Especialização para jogos focados em modo história e campanha single-player.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `capitulos_concluidos` | `int` | Público (`+`) | Total de capítulos finalizados (vem do `CampanhaMixin`) |
| **Atributo** | `percentual_conclusao` | `float` | Público (`+`) | Progresso da história (0 a 100%) (vem do `CampanhaMixin`) |

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

#### 4. Subclasse: `JogoCooperativo` (Herda de `CooperativoMixin` e `Jogo`)
Especialização para jogos focados em cooperação e trabalho em equipe.

| Elemento | Nome | Tipo / Retorno | Visibilidade | Descrição |
|---|---|---|---|---|
| **Atributo** | `max_jogadores` | `int` | Público (`+`) | Limite máximo de pessoas no grupo (vem do `CooperativoMixin`) |
| **Atributo** | `sessoes_cooperativas` | `int` | Público (`+`) | Número de sessões jogadas em equipe (vem do `CooperativoMixin`) |
| **Atributo** | `participantes_frequentes` | `list[str]` | Público (`+`) | Jogadores frequentes (vem do `CooperativoMixin`) |

---

#### 5. Subclasse: `JogoCampanhaCoop` (Herda de `JogoCampanha` e `JogoCooperativo`)
Representa jogos focados na história principal que podem ser concluídos cooperativamente em grupo (**herança múltipla**). Ordem de resolução (MRO): `JogoCampanhaCoop → JogoCampanha → CampanhaMixin → JogoCooperativo → CooperativoMixin → Jogo`.

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
| **Método** | `adicionar_jogo()` | `None` | Público (`+`) | Insere um novo objeto de jogo na coleção (não permite duplicados) |
| **Método** | `remover_jogo()` | `bool` | Público (`+`) | Remove um jogo específico da coleção pelo título |
| **Método** | `listar_jogos()` | `list[Jogo]` | Público (`+`) | Retorna a lista contendo todos os jogos da coleção |
| **Método** | `buscar_por_titulo()` | `Optional[Jogo]` | Público (`+`) | Busca e retorna um jogo específico pelo título |
| **Método** | `buscar_por_parte_do_titulo()` | `list[Jogo]` | Público (`+`) | Retorna os jogos cujo título contém o trecho informado |
| **Método** | `atualizar_jogo()` | `bool` | Público (`+`) | Atualiza atributos de um jogo existente utilizando `**kwargs` |
| **Método** | `filtrar_por_genero()`, `filtrar_por_status()`, `filtrar_por_plataforma()`, `filtrar_por_nota_minima()` | `list[Jogo]` | Público (`+`) | Filtram os jogos pelo critério informado |
| **Método** | `ordenar_por_titulo()`, `ordenar_por_horas()`, `ordenar_por_avaliacao()`, `ordenar_por_ano()` | `list[Jogo]` | Público (`+`) | Ordenam os jogos pelo critério informado |
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
| **Método** | `progresso_meta()` | `dict` | Público (`+`) | Retorna a meta, os jogos finalizados, o percentual e se a meta foi atingida |

---

#### 8. Exceções Customizadas (`src/models/excecoes.py`)
Todas herdam de `CatalogoError`, que por sua vez herda de `ValueError`.

| Exceção | Quando é levantada |
|---|---|
| `TituloInvalidoError` | Título vazio |
| `HorasInvalidasError` | Horas negativas ou progresso menor ou igual a zero |
| `StatusInvalidoError` | Status inexistente ou tentativa de finalizar com menos de 1h |
| `AvaliacaoInvalidaError` | Nota fora de 0–10 ou jogo ainda não finalizado |
| `JogoDuplicadoError` | Jogo com mesmo título e plataforma já existe na coleção |
| `LimiteJogandoError` | Limite de jogos simultâneos "JOGANDO" atingido |


## Decisões de Design

- **Herança múltipla com mixins:** `CampanhaMixin` e `CooperativoMixin` guardam os recursos de cada modo, e `JogoCampanhaCoop` herda de `JogoCampanha` e `JogoCooperativo` (herança em losango sobre `Jogo`), reaproveitando os dois.
- **Encapsulamento com `@property`:** título, status, horas e nota são validados nos setters.
- **Regras no modelo:** a regra de "1h para finalizar" fica em `Jogo.finalizar()`. Já as regras que olham o catálogo inteiro (limite de "JOGANDO" e aviso de meta) ficam em `src/utils/regras.py` e usam os valores do `settings.json`.
- **Exceções customizadas** herdando de `ValueError`, para deixar claro qual regra foi violada.
- **Coleção "Geral":** todo jogo cadastrado aparece nela, e o mesmo jogo em várias coleções é **um único objeto**, então atualizar em uma atualiza em todas.
- **Persistência desacoplada do domínio:** `persistencia.py` converte os objetos de/para JSON, recriando a classe certa pelo campo `tipo`.



##  Testes Automatizados

Para rodar os testes automatizados do projeto, execute o comando abaixo no terminal, na raiz do projeto:

```bash
pytest -q

```
###  O projeto conta com 54 testes automatizados validados via pytest, cobrindo casos felizes e de erro:


## Estrutura do Projeto

```text

├── main.py
├── settings.json
├── requirements.txt
├── data/
│   ├── colecoes.json
│   └── usuario.json
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── colecao.py
│   │   ├── excecoes.py
│   │   ├── jogo.py
│   │   └── usuario.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── persistencia.py
│   │   ├── regras.py
│   │   ├── relatorio.py
│   │   └── settings.py
│   └── cli/
│       ├── __init__.py
│       ├── auxiliares.py
│       ├── comandos_colecao.py
│       ├── comandos_jogo.py
│       ├── comandos_settings.py
│       ├── comandos_usuario.py
│       ├── exibicao.py
│       ├── fabrica.py
│       └── parser.py
├── tests/
│   ├── __init__.py
│   ├── test_colecao.py
│   ├── test_jogo.py
│   ├── test_persistencia.py
│   ├── test_relatorio.py
│   ├── test_semana4.py
│   ├── test_semana5.py
│   └── test_usuario.py
└── README.md
```
