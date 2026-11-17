TIMES_E_JOGADORES = {
    "Cruzeiro": [
        ("Otávio", "Goleiro"), ("Fagner", "Defensor"),
        ("Jonathan Jesus", "Defensor"), ("Fabrício Bruno", "Defensor"),
        ("Kaiki", "Defensor"), ("Lucas Romero", "Meio-campo"),
        ("Matheus Henrique", "Meio-campo"), ("Gerson", "Meio-campo"),
        ("Matheus Pereira", "Meio-campo"), ("Kaio Jorge", "Atacante"),
        ("Keny Arroyo", "Atacante")
    ],
    "Flamengo": [
        ("Rossi", "Goleiro"), ("Varela", "Defensor"),
        ("Léo Ortiz", "Defensor"), ("Léo Pereira", "Defensor"),
        ("Ayrton Lucas", "Defensor"), ("Pulgar", "Meio-campo"),
        ("Jorginho", "Meio-campo"), ("Arrascaeta", "Meio-campo"),
        ("Carrascal", "Meio-campo"), ("Samuel Lino", "Atacante"),
        ("Pedro", "Atacante")
    ],
    "Palmeiras": [
        ("Carlos Miguel", "Goleiro"), ("Giay", "Defensor"),
        ("Gustavo Gómez", "Defensor"), ("Murilo", "Defensor"),
        ("Piquerez", "Defensor"), ("Marlon Freitas", "Meio-campo"),
        ("Andreas Pereira", "Meio-campo"), ("Lucas Evangelista", "Meio-campo"),
        ("Maurício", "Meio-campo"), ("Jhon Arias", "Atacante"),
        ("Vitor Roque", "Atacante")
    ],
    "Corinthians": [
        ("Hugo Souza", "Goleiro"), ("Matheuzinho", "Defensor"),
        ("André Ramalho", "Defensor"), ("Gustavo Henrique", "Defensor"),
        ("Angileri", "Defensor"), ("André", "Meio-campo"),
        ("Breno Bidon", "Meio-campo"), ("Rodrigo Garro", "Meio-campo"),
        ("Kaio César", "Atacante"), ("Yuri Alberto", "Atacante"),
        ("Memphis Depay", "Atacante")
    ],
    "São Paulo": [
        ("Rafael", "Goleiro"), ("Lucas Ramon", "Defensor"),
        ("Arboleda", "Defensor"), ("Tolói", "Defensor"),
        ("Wendell", "Defensor"), ("Bobadilla", "Meio-campo"),
        ("Pablo Maia", "Meio-campo"), ("Luciano", "Meio-campo"),
        ("Lucas Moura", "Atacante"), ("Artur", "Atacante"),
        ("Calleri", "Atacante")
    ],
    "Santos": [
        ("Diógenes", "Goleiro"), ("Igor Vinícius", "Defensor"),
        ("Luan Peres", "Defensor"), ("Adonis Frías", "Defensor"),
        ("Escobar", "Defensor"), ("João Schmidt", "Meio-campo"),
        ("Gabriel Bontempo", "Meio-campo"), ("Rollheiser", "Meio-campo"),
        ("Rony", "Atacante"), ("Gabigol", "Atacante"),
        ("Neymar", "Atacante")
    ],
    "Grêmio": [
        ("Weverton", "Goleiro"), ("João Pedro", "Defensor"),
        ("Gustavo Martins", "Defensor"), ("Kannemann", "Defensor"),
        ("Caio Paulista", "Defensor"), ("Noriega", "Meio-campo"),
        ("Villasanti", "Meio-campo"), ("Tetê", "Meio-campo"),
        ("Amuzu", "Atacante"), ("Enamorado", "Atacante"),
        ("Carlos Vinícius", "Atacante")
    ],
    "Internacional": [
        ("Rochet", "Goleiro"), ("Aguirre", "Defensor"),
        ("Juninho", "Defensor"), ("Mercado", "Defensor"),
        ("Bernabei", "Defensor"), ("Thiago Maia", "Meio-campo"),
        ("Villagra", "Meio-campo"), ("Bruno Gomes", "Meio-campo"),
        ("Alan Patrick", "Meio-campo"), ("Carbonero", "Atacante"),
        ("Alerrandro", "Atacante")
    ],
    "Atlético-MG": [
        ("Everson", "Goleiro"), ("Natanael", "Defensor"),
        ("Léo Duarte", "Defensor"), ("Vitor Hugo", "Defensor"),
        ("Renan Lodi", "Defensor"), ("Castaño", "Meio-campo"),
        ("Alan Franco", "Meio-campo"), ("Alexsander", "Meio-campo"),
        ("Bernard", "Meio-campo"), ("Cuello", "Atacante"),
        ("Cassierra", "Atacante")
    ],
    "Botafogo": [
        ("John", "Goleiro"), ("Vitinho", "Defensor"),
        ("Ferraresi", "Defensor"), ("Barboza", "Defensor"),
        ("Marçal", "Defensor"), ("Marlon Freitas", "Meio-campo"),
        ("Danilo", "Meio-campo"), ("Savarino", "Meio-campo"),
        ("Artur", "Atacante"), ("Igor Jesus", "Atacante"),
        ("Tiquinho", "Atacante")
    ],
    "Fluminense": [
        ("Fábio", "Goleiro"), ("Guga", "Defensor"),
        ("Thiago Silva", "Defensor"), ("Igor Rabello", "Defensor"),
        ("Renê", "Defensor"), ("Hércules", "Meio-campo"),
        ("Martinelli", "Meio-campo"), ("Lucho Acosta", "Meio-campo"),
        ("Savarino", "Atacante"), ("Canobbio", "Atacante"),
        ("Cano", "Atacante")
    ],
    "Vasco": [
        ("Léo Jardim", "Goleiro"), ("Paulo Henrique", "Defensor"),
        ("Cuesta", "Defensor"), ("Robert Renan", "Defensor"),
        ("Cuiabano", "Defensor"), ("Thiago Mendes", "Meio-campo"),
        ("Santiago Sosa", "Meio-campo"), ("Coutinho", "Meio-campo"),
        ("Adson", "Atacante"), ("Rayan", "Atacante"),
        ("Vegetti", "Atacante")
    ]
}


def cadastrar_dados_iniciais(banco):
    cursor = banco.conexao.cursor()
    quantidade = cursor.execute("SELECT COUNT(*) FROM times").fetchone()[0]

    if quantidade == 0:
        for nome_time, jogadores in TIMES_E_JOGADORES.items():
            cursor.execute("INSERT INTO times (nome) VALUES (?)", (nome_time,))
            time_id = cursor.lastrowid

            for nome, posicao in jogadores:
                cursor.execute("""
                    INSERT INTO jogadores (nome, posicao, time_id)
                    VALUES (?, ?, ?)
                """, (nome, posicao, time_id))

        banco.conexao.commit()
