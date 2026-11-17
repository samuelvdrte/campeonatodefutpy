from database import BancoDeDados
from dados_iniciais import cadastrar_dados_iniciais
from cadastros import Cadastro
from campeonato import Campeonato


class Aplicacao:
    """Controla o menu e a navegação do programa."""

    def __init__(self):
        self.banco = BancoDeDados()
        cadastrar_dados_iniciais(self.banco)
        self.cadastro = Cadastro(self.banco)
        self.campeonato = Campeonato(self.banco)

    def menu_times(self):
        while True:
            print("""
--- GERENCIAR TIMES ---
1 - Listar times
2 - Adicionar time
3 - Editar time
4 - Excluir time
0 - Voltar
""")
            opcao = input("Escolha: ").strip()

            try:
                if opcao == "1":
                    self.cadastro.listar_times()
                elif opcao == "2":
                    nome = input("Nome do time: ").strip()
                    if nome:
                        self.cadastro.adicionar_time(nome)
                        print("Time cadastrado.")
                elif opcao == "3":
                    self.cadastro.listar_times()
                    time_id = int(input("ID do time: "))
                    nome = input("Novo nome: ").strip()
                    if self.cadastro.editar_time(time_id, nome):
                        print("Time atualizado.")
                    else:
                        print("Time não encontrado.")
                elif opcao == "4":
                    self.cadastro.listar_times()
                    time_id = int(input("ID do time: "))
                    if input("Confirma exclusão? (s/n): ").lower() == "s":
                        if self.cadastro.excluir_time(time_id):
                            print("Time excluído.")
                        else:
                            print("Time não encontrado.")
                elif opcao == "0":
                    break
                else:
                    print("Opção inválida.")
            except Exception as erro:
                print("Não foi possível concluir a operação:", erro)

    def menu_jogadores(self):
        while True:
            print("""
--- GERENCIAR JOGADORES ---
1 - Listar jogadores
2 - Adicionar jogador
3 - Editar jogador
4 - Excluir jogador
0 - Voltar
""")
            opcao = input("Escolha: ").strip()

            try:
                if opcao == "1":
                    self.cadastro.listar_jogadores()
                elif opcao == "2":
                    self.cadastro.listar_times()
                    nome = input("Nome do jogador: ").strip()
                    posicao = input("Posição: ").strip()
                    time_id = int(input("ID do time: "))
                    self.cadastro.adicionar_jogador(nome, posicao, time_id)
                    print("Jogador cadastrado.")
                elif opcao == "3":
                    self.cadastro.listar_jogadores()
                    jogador_id = int(input("ID do jogador: "))
                    nome = input("Novo nome: ").strip()
                    posicao = input("Nova posição: ").strip()
                    self.cadastro.listar_times()
                    time_id = int(input("ID do novo time: "))
                    if self.cadastro.editar_jogador(
                        jogador_id, nome, posicao, time_id
                    ):
                        print("Jogador atualizado.")
                    else:
                        print("Jogador não encontrado.")
                elif opcao == "4":
                    self.cadastro.listar_jogadores()
                    jogador_id = int(input("ID do jogador: "))
                    if input("Confirma exclusão? (s/n): ").lower() == "s":
                        if self.cadastro.excluir_jogador(jogador_id):
                            print("Jogador excluído.")
                        else:
                            print("Jogador não encontrado.")
                elif opcao == "0":
                    break
                else:
                    print("Opção inválida.")
            except Exception as erro:
                print("Não foi possível concluir a operação:", erro)

    def executar(self):
        try:
            while True:
                print("""
====================================
     SIMULADOR DE CAMPEONATO
====================================
1 - Gerenciar times (CRUD)
2 - Gerenciar jogadores (CRUD)
3 - Simular rodadas (avançar com ENTER)
4 - Simular todas as rodadas automaticamente
5 - Ver classificação
6 - Ver artilheiros
7 - Ver assistências
8 - Ver histórico de partidas
0 - Sair
""")
                opcao = input("Escolha uma opção: ").strip()

                try:
                    if opcao == "1":
                        self.menu_times()
                    elif opcao == "2":
                        self.menu_jogadores()
                    elif opcao == "3":
                        self.campeonato.iniciar_campeonato(pausar=True)
                    elif opcao == "4":
                        self.campeonato.iniciar_campeonato(pausar=False)
                    elif opcao == "5":
                        self.campeonato.mostrar_classificacao()
                    elif opcao == "6":
                        self.campeonato.mostrar_ranking("gols", "ARTILHEIROS")
                    elif opcao == "7":
                        self.campeonato.mostrar_ranking(
                            "assistencias", "ASSISTÊNCIAS"
                        )
                    elif opcao == "8":
                        self.campeonato.mostrar_historico()
                    elif opcao == "0":
                        print("Programa encerrado. Até mais!")
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                except ValueError as erro:
                    print("Atenção:", erro)
                except Exception as erro:
                    print("Ocorreu um erro na operação:", erro)
        finally:
            self.banco.fechar()


if __name__ == "__main__":
    Aplicacao().executar()
