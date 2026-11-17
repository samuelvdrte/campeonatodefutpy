import sqlite3


class BancoDeDados:
    """Responsável pela conexão e pela criação das tabelas."""

    def __init__(self, arquivo="campeonato.db"):
        self.conexao = sqlite3.connect(arquivo)
        self.conexao.row_factory = sqlite3.Row
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.criar_tabelas()

    def criar_tabelas(self):
        self.conexao.executescript("""
            CREATE TABLE IF NOT EXISTS times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS jogadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                posicao TEXT NOT NULL,
                time_id INTEGER NOT NULL,
                FOREIGN KEY (time_id) REFERENCES times(id)
                    ON DELETE CASCADE,
                UNIQUE(nome, time_id)
            );

            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rodada INTEGER NOT NULL,
                time_casa_id INTEGER NOT NULL,
                time_fora_id INTEGER NOT NULL,
                gols_casa INTEGER NOT NULL,
                gols_fora INTEGER NOT NULL,
                FOREIGN KEY (time_casa_id) REFERENCES times(id),
                FOREIGN KEY (time_fora_id) REFERENCES times(id)
            );

            CREATE TABLE IF NOT EXISTS gols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                partida_id INTEGER NOT NULL,
                jogador_id INTEGER NOT NULL,
                assistente_id INTEGER,
                FOREIGN KEY (partida_id) REFERENCES partidas(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (jogador_id) REFERENCES jogadores(id),
                FOREIGN KEY (assistente_id) REFERENCES jogadores(id)
            );
        """)
        self.conexao.commit()

    def fechar(self):
        self.conexao.close()
