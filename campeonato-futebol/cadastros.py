class Cadastro:
    """Realiza operações CRUD de times e jogadores."""

    def __init__(self, banco):
        self.conexao = banco.conexao

    def listar_times(self):
        cursor = self.conexao.execute("SELECT id, nome FROM times ORDER BY nome")
        times = cursor.fetchall()

        print("\n--- TIMES CADASTRADOS ---")
        for time in times:
            print(f'{time["id"]} - {time["nome"]}')
        if not times:
            print("Nenhum time cadastrado.")

    def adicionar_time(self, nome):
        self.conexao.execute("INSERT INTO times (nome) VALUES (?)", (nome,))
        self.conexao.commit()

    def editar_time(self, time_id, novo_nome):
        cursor = self.conexao.execute(
            "UPDATE times SET nome = ? WHERE id = ?", (novo_nome, time_id)
        )
        self.conexao.commit()
        return cursor.rowcount > 0

    def excluir_time(self, time_id):
        cursor = self.conexao.execute(
            "DELETE FROM times WHERE id = ?", (time_id,)
        )
        self.conexao.commit()
        return cursor.rowcount > 0

    def listar_jogadores(self):
        cursor = self.conexao.execute("""
            SELECT j.id, j.nome, j.posicao, t.nome AS time
            FROM jogadores j
            JOIN times t ON t.id = j.time_id
            ORDER BY t.nome, j.nome
        """)
        jogadores = cursor.fetchall()

        print("\n--- JOGADORES CADASTRADOS ---")
        for jogador in jogadores:
            print(f'{jogador["id"]} - {jogador["nome"]} | '
                  f'{jogador["posicao"]} | {jogador["time"]}')
        if not jogadores:
            print("Nenhum jogador cadastrado.")

    def adicionar_jogador(self, nome, posicao, time_id):
        self.conexao.execute("""
            INSERT INTO jogadores (nome, posicao, time_id)
            VALUES (?, ?, ?)
        """, (nome, posicao, time_id))
        self.conexao.commit()

    def editar_jogador(self, jogador_id, nome, posicao, time_id):
        cursor = self.conexao.execute("""
            UPDATE jogadores
            SET nome = ?, posicao = ?, time_id = ?
            WHERE id = ?
        """, (nome, posicao, time_id, jogador_id))
        self.conexao.commit()
        return cursor.rowcount > 0

    def excluir_jogador(self, jogador_id):
        cursor = self.conexao.execute(
            "DELETE FROM jogadores WHERE id = ?", (jogador_id,)
        )
        self.conexao.commit()
        return cursor.rowcount > 0

    def obter_times(self):
        return self.conexao.execute(
            "SELECT id, nome FROM times ORDER BY nome"
        ).fetchall()
