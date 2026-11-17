import random


class Campeonato:
    def __init__(self, banco):
        self.conexao = banco.conexao

    def gerar_rodadas(self):
        times = self.conexao.execute(
            "SELECT id, nome FROM times ORDER BY id"
        ).fetchall()

        if len(times) != 12:
            raise ValueError("O campeonato precisa ter exatamente 12 times.")

        rodadas = []
        for numero in range(11):
            jogos = []
            for i in range(6):
                jogos.append((times[i], times[11 - i]))
            rodadas.append(jogos)
            times = [times[0], times[-1]] + times[1:-1]

        return rodadas

    def simular_partida(self, rodada, casa, fora):
        gols_casa = random.randint(0, 4)
        gols_fora = random.randint(0, 4)

        cursor = self.conexao.cursor()
        cursor.execute(
            """INSERT INTO partidas
            (rodada, time_casa_id, time_fora_id, gols_casa, gols_fora)
            VALUES (?, ?, ?, ?, ?)""",
            (rodada, casa["id"], fora["id"], gols_casa, gols_fora)
        )
        partida_id = cursor.lastrowid

        self.registrar_gols(partida_id, casa, gols_casa)
        self.registrar_gols(partida_id, fora, gols_fora)
        self.conexao.commit()

        return gols_casa, gols_fora

    def registrar_gols(self, partida_id, time, quantidade):
        jogadores = self.conexao.execute(
            "SELECT id FROM jogadores WHERE time_id = ?", (time["id"],)
        ).fetchall()

        for _ in range(quantidade):
            autor = random.choice(jogadores)["id"]
            outros_jogadores = [j["id"] for j in jogadores if j["id"] != autor]

            assistente_id = None
            if outros_jogadores and random.random() < 0.75:
                assistente_id = random.choice(outros_jogadores)

            self.conexao.execute(
                """INSERT INTO gols (partida_id, jogador_id, assistente_id)
                VALUES (?, ?, ?)""",
                (partida_id, autor, assistente_id)
            )

    def iniciar_campeonato(self, pausar=True):
        quantidade = self.conexao.execute(
            "SELECT COUNT(*) FROM jogadores"
        ).fetchone()[0]

        if quantidade != 132:
            print("O campeonato precisa ter 132 jogadores cadastrados.")
            return

        confirmar = input(
            "Iniciar novo campeonato? Os resultados anteriores serão apagados (s/n): "
        ).strip().lower()
        if confirmar != "s":
            print("Operação cancelada.")
            return

        self.conexao.execute("DELETE FROM gols")
        self.conexao.execute("DELETE FROM partidas")
        self.conexao.commit()

        rodadas = self.gerar_rodadas()

        for numero, jogos in enumerate(rodadas, 1):
            if pausar:
                input(f"\nPressione ENTER para simular a rodada {numero}...")

            print(f"\n========== RODADA {numero} ==========")
            for casa, fora in jogos:
                gols_casa, gols_fora = self.simular_partida(
                    numero, casa, fora
                )
                print(f'{casa["nome"]} {gols_casa} x {gols_fora} {fora["nome"]}')

            self.mostrar_classificacao()
            self.mostrar_ranking("gols", "ARTILHEIROS")
            self.mostrar_ranking("assistencias", "ASSISTÊNCIAS")

        print("\nCAMPEONATO FINALIZADO!")

    def mostrar_classificacao(self):
        times = self.conexao.execute(
            "SELECT id, nome FROM times ORDER BY nome"
        ).fetchall()
        partidas = self.conexao.execute("SELECT * FROM partidas").fetchall()

        tabela = {}
        for time in times:
            tabela[time["id"]] = {
                "nome": time["nome"], "jogos": 0, "vitorias": 0,
                "empates": 0, "derrotas": 0, "gp": 0, "gc": 0,
                "pontos": 0
            }

        for partida in partidas:
            casa = tabela[partida["time_casa_id"]]
            fora = tabela[partida["time_fora_id"]]
            gols_casa = partida["gols_casa"]
            gols_fora = partida["gols_fora"]

            casa["jogos"] += 1
            fora["jogos"] += 1
            casa["gp"] += gols_casa
            casa["gc"] += gols_fora
            fora["gp"] += gols_fora
            fora["gc"] += gols_casa

            if gols_casa > gols_fora:
                casa["vitorias"] += 1
                casa["pontos"] += 3
                fora["derrotas"] += 1
            elif gols_fora > gols_casa:
                fora["vitorias"] += 1
                fora["pontos"] += 3
                casa["derrotas"] += 1
            else:
                casa["empates"] += 1
                fora["empates"] += 1
                casa["pontos"] += 1
                fora["pontos"] += 1

        classificacao = list(tabela.values())
        classificacao.sort(
            key=lambda time: (
                time["pontos"], time["vitorias"],
                time["gp"] - time["gc"], time["gp"]
            ),
            reverse=True
        )

        print("\n--- CLASSIFICAÇÃO ---")
        print("TIME                 PTS  J  V  E  D  GP  GC  SG")
        for time in classificacao:
            saldo = time["gp"] - time["gc"]
            print(
                f'{time["nome"]:<20} {time["pontos"]:>3} '
                f'{time["jogos"]:>2} {time["vitorias"]:>2} '
                f'{time["empates"]:>2} {time["derrotas"]:>2} '
                f'{time["gp"]:>3} {time["gc"]:>3} {saldo:>3}'
            )

    def mostrar_ranking(self, tipo, titulo):
        if tipo == "gols":
            campo = "g.jogador_id"
        else:
            campo = "g.assistente_id"

        consulta = f"""
            SELECT j.nome, t.nome AS time, COUNT(g.id) AS total
            FROM gols g
            JOIN jogadores j ON j.id = {campo}
            JOIN times t ON t.id = j.time_id
            GROUP BY j.id
            ORDER BY total DESC, j.nome
            LIMIT 3
        """
        jogadores = self.conexao.execute(consulta).fetchall()

        print(f"\n--- TOP 3 {titulo} ---")
        if not jogadores:
            print("Ainda não há registros.")

        for posicao, jogador in enumerate(jogadores, 1):
            print(
                f'{posicao}º - {jogador["nome"]} '
                f'({jogador["time"]}): {jogador["total"]}'
            )

    def mostrar_historico(self):
        partidas = self.conexao.execute("""
            SELECT p.rodada, casa.nome AS casa, p.gols_casa,
                   fora.nome AS fora, p.gols_fora
            FROM partidas p
            JOIN times casa ON casa.id = p.time_casa_id
            JOIN times fora ON fora.id = p.time_fora_id
            ORDER BY p.rodada, p.id
        """).fetchall()

        print("\n--- HISTÓRICO DE PARTIDAS ---")
        if not partidas:
            print("Nenhuma partida foi simulada.")

        for partida in partidas:
            print(
                f'Rodada {partida["rodada"]}: {partida["casa"]} '
                f'{partida["gols_casa"]} x {partida["gols_fora"]} '
                f'{partida["fora"]}'
            )
