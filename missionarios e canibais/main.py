from canibais import BuscaProfundidade, BuscaLargura, BuscaGulosa, BuscaAStar
import time
import networkx as nx
import matplotlib.pyplot as plt


def criar_arvore(busca):
    grafo = nx.DiGraph()
    for estado in busca.estados_visitados:
        grafo.add_node(estado)

    for estado in busca.estados_visitados:
        next_states = busca.generate_next_states(estado)
        for next_state in next_states:
            if next_state in busca.estados_visitados:
                grafo.add_edge(estado, next_state)

    plotar_arvore_estados(grafo)


def plotar_arvore_estados(grafo):
    pos = nx.spring_layout(grafo)
    nx.draw_networkx(grafo, pos, with_labels=True, font_size=9, font_family="Comic Sans MS", node_size=1000,
                     node_color="lightblue", edge_color="gray", arrows=True, arrowstyle='->, head_width=0.3, head_length=1.0')

    plt.title("Árvore de Estados")
    plt.axis("off")

    plt.show()


def main():
    quantidade = 3
    canibais, missionarios = quantidade, quantidade

    while True:
        start_state = (missionarios, canibais, 'esquerda', 0, 0)
        goal_state = (0, 0, 'direita', missionarios, canibais)

        print_menu()
        option = get_menu_choice()

        t_start, t_end = 0, 0

        if option == 0:
            print("Saindo do programa...")
            break

        elif option == 1:
            # Executar busca em largura
            busca = BuscaLargura(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #criar_arvore(busca)

        elif option == 2:
            # Executar busca profundidade
            # ...
            busca = BuscaProfundidade(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #criar_arvore(busca)

        elif option == 3:
            # Executar busca gulosa
            # ...
            busca = BuscaGulosa(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #criar_arvore(busca)

        elif option == 4:
            # Executar busca A*
            # ...
            busca = BuscaAStar(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #criar_arvore(busca)


def print_menu():
    print('============= MENU =============')
    print('1 - Busca em Largura')
    print('2 - Busca em Profundidade')
    print('3 - Busca Gulosa*')
    print('4 - Busca A*')
    print('0 - Sair')
    print('================================')


def get_menu_choice():
    while True:
        try:
            choice = int(input("Digite o número da opção desejada: "))
            if choice in [0, 1, 2, 3, 4]:
                return choice
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")


def printSolucao(solucao, t_end, t_start):
    if solucao:
        print("Solução encontrada:")
        for state in solucao:
            print(state)
    else:
        print('>>>>>>>>>> Não foi encontrada uma solução. <<<<<<<<<<<<<<')

    print('\nTempo decorrido: {:.4f} ms\n\n'.format(t_end - t_start))


if __name__ == "__main__":
    main()
