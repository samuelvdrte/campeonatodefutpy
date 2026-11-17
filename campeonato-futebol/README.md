# Simulador de Campeonato de Futebol

Aplicação em Python com Programação Orientada a Objetos (POO), interface pelo terminal e banco de dados SQLite3.

## Tema do projeto

Simulador de campeonato de futebol com 12 equipes, incluindo o Cruzeiro. O campeonato é disputado em turno único: são 11 rodadas, 6 partidas por rodada e 66 partidas no total.

Os placares são sorteados sem diferença de força entre os clubes e sem vantagem de mando de campo.

> **Importante:** os elencos são exemplos ilustrativos para preencher o banco e demonstrar o sistema. Não representam escalações oficiais fixas; os nomes devem ser conferidos e atualizados conforme a temporada definida com a professora.

## Funcionalidades

- Menu principal com opções para entrar nas funções e sair do programa.
- Cadastro, consulta, edição e exclusão de times.
- Cadastro, consulta, edição e exclusão de jogadores.
- Simulação de 11 rodadas e 66 partidas, com opção de avançar rodada a rodada ou simular todas automaticamente.
- Classificação com pontos, jogos, vitórias, empates, derrotas, gols pró, gols contra e saldo.
- Ranking dos três artilheiros e dos três jogadores com mais assistências.
- Histórico de partidas salvo no SQLite3.

## Tecnologias e bibliotecas

- Python 3.
- SQLite3 (`sqlite3`): biblioteca padrão do Python, não precisa instalar separadamente.
- `random`: biblioteca padrão do Python para sortear os placares e eventos de gol.

**Não é necessário instalar bibliotecas externas.**

## Como executar

1. Instale o Python 3.
2. Baixe ou clone este repositório.
3. Abra o terminal na pasta do projeto.
4. Execute:

```bash
python main.py
```

O arquivo `campeonato.db` será criado automaticamente na primeira execução, com as tabelas e os cadastros iniciais.

## Estrutura de arquivos

```text
campeonato-futebol/
│
├── main.py              # Menu principal e controle da aplicação
├── database.py          # Conexão e criação das tabelas SQLite
├── dados_iniciais.py    # Cadastro inicial dos times e jogadores
├── cadastros.py         # Operações CRUD de times e jogadores
├── campeonato.py        # Rodadas, partidas e estatísticas
├── README.md            # Instruções do projeto
└── campeonato.db        # Banco criado automaticamente ao executar
```

## Banco de dados

O projeto possui quatro tabelas relacionais:

1. **times**: guarda os clubes.
2. **jogadores**: guarda os jogadores e relaciona cada um a um time.
3. **partidas**: guarda rodada, equipes e placar.
4. **gols**: guarda o autor do gol e, quando houver, o jogador que deu a assistência.

As relações são feitas com chaves estrangeiras (`FOREIGN KEY`).

## CRUD implementado

O menu permite realizar as quatro operações:

- **Create:** cadastrar times e jogadores.
- **Read:** listar times e jogadores.
- **Update:** editar dados de times e jogadores.
- **Delete:** excluir times e jogadores.

Os resultados das partidas também são gravados no banco. Ao iniciar um novo campeonato, o sistema pede confirmação e apaga apenas o histórico de gols e partidas da simulação anterior; os cadastros de times e jogadores são mantidos.

## Como funciona a simulação

- O programa organiza os 12 times em 11 rodadas, com 6 jogos em cada rodada.
- Cada placar é sorteado com `random.randint(0, 4)`, sem vantagem para nenhum clube.
- Os gols e as assistências são registrados na tabela `gols`.
- A classificação percorre os resultados salvos e soma pontos e estatísticas: vitória vale 3 pontos, empate vale 1 e derrota vale 0.
- A opção 3 pausa entre as rodadas; a opção 4 executa tudo sem pedir ENTER entre elas.

## Orientação a Objetos

O projeto foi dividido em classes para separar responsabilidades:

- `BancoDeDados`: abre a conexão, cria as tabelas e fecha o banco.
- `Cadastro`: realiza o CRUD de times e jogadores.
- `Campeonato`: organiza rodadas, simula jogos e calcula a classificação e os rankings. A classificação é calculada com listas e condições em Python para facilitar a compreensão na apresentação.
- `Aplicacao`: controla o menu e a interação com o usuário.

## Sugestão para publicar no GitHub

Crie um repositório chamado `simulador-campeonato-futebol`, envie os arquivos `.py` e o `README.md`. O banco `campeonato.db` é criado automaticamente, então não é necessário enviar esse arquivo ao GitHub.
