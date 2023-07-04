from missionarios_canibaisFinal import BuscaProfundidade, BuscaLargura, BuscaGulosa,BuscaAStar
import time
import networkx as nx
import matplotlib.pyplot as plt

def solve(num_missionaries, num_cannibals):
    start_time = time.time()

    initial_state = BuscaLargura(num_missionaries, num_cannibals, 0, 0, True)
    visited = set()
    stack = [[initial_state]]
    level = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_depth = 0
    max_memory_usage = 0

    while stack:
        max_memory_usage = max(max_memory_usage, len(stack))
        path = stack.pop()  # Remove o último estado adicionado à pilha
        print(f"\nProfundidade {level}:\n")
        nodes_expanded += 1

        current_state = path[-1]
        visited.add(str(current_state))

        if current_state.is_goal_state():
            execution_time = time.time() - start_time
            solution_depth = len(path) - 1
            return path, nodes_expanded, nodes_generated, max_memory_usage, level, solution_depth, max_depth, execution_time

        print(f'Atual: {current_state}\n')
        possible_moves = get_possible_moves(current_state)
        print('Expandidos: \n')
        for move in possible_moves:
            new_state = apply_move(current_state, move)
            valid_indicator = "(Valido)" if new_state.is_valid() else "(Invalido)"
            visited_indicator = "(já foi visitado)" if str(new_state) in visited else ""
            print(f"---> {new_state} {visited_indicator} {valid_indicator} ")
            if str(new_state) not in visited:
                nodes_generated += 1
                if new_state.is_valid():
                    stack.append(path + [new_state])  # Adiciona o novo estado à pilha
                    max_depth = max(max_depth, len(path))

        level += 1

    return None, nodes_expanded, nodes_generated, max_memory_usage, 0, 0, max_depth, time.time() - start_time


def get_possible_moves(state):
    possible_moves = []
    if state.boat_on_left:
        for m in range(state.left_missionaries + 1):
            for c in range(state.left_cannibals + 1):
                if m + c >= 1 and m + c <= 2:
                    possible_moves.append((m, c))
    else:
        for m in range(state.right_missionaries + 1):
            for c in range(state.right_cannibals + 1):
                if m + c >= 1 and m + c <= 2:
                    possible_moves.append((m, c))
    return possible_moves


def apply_move(state, move):
    missionaries, cannibals = move
    if state.boat_on_left:
        new_left_missionaries = state.left_missionaries - missionaries
        new_left_cannibals = state.left_cannibals - cannibals
        new_right_missionaries = state.right_missionaries + missionaries
        new_right_cannibals = state.right_cannibals + cannibals
        new_boat_on_left = False
    else:
        new_left_missionaries = state.left_missionaries + missionaries
        new_left_cannibals = state.left_cannibals + cannibals
        new_right_missionaries = state.right_missionaries - missionaries
        new_right_cannibals = state.right_cannibals - cannibals
        new_boat_on_left = True
    return BuscaLargura(new_left_missionaries, new_left_cannibals, new_right_missionaries, new_right_cannibals,
                 new_boat_on_left)

 
def plot_info(busca, nome):
    dados = [busca.depth, busca.qntNodesGen, busca.qntNodesExp, busca.qntNodesFront]
    nomes = ['Profundidade', 'Nós gerados', 'Nós expandidos', 'Nós na fronteira']
    cores = ['red', 'green', 'yellow', 'blue']
    indices = range(len(dados))
        
    plt.bar(indices, dados, color=cores)
    for i, valor in enumerate(dados):
        plt.annotate(str(valor), xy=(i, valor), ha='center', va='bottom')
    plt.title(nome)
    plt.xticks(indices, nomes)
    plt.show()

def plot_largura(busca, nome):
    
    nomes = ['Profundidade', 'Nós gerados', 'Nós expandidos', 'Nós na fronteira']
    cores = ['red', 'green', 'yellow', 'blue']
    indices = range(len(busca))
        
    plt.bar(indices, busca, color=cores)
    for i, valor in enumerate(busca):
        plt.annotate(str(valor), xy=(i, valor), ha='center', va='bottom')
    plt.title(nome)
    plt.xticks(indices, nomes)
    #plt.show()
 
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
            solution, nodes_expanded, nodes_generated, max_memory_usage, _, solution_depth, max_depth, execution_time = solve(
                3, 3
            )

            if solution:
                print("Solução encontrada:\n")
                for state in solution:
                    print(f'--> {state}')
            else:
                print("Solucao não encontrada")

            # Statitics
            values = [solution_depth, nodes_generated, nodes_expanded, max_memory_usage]

            #plot_largura(values, 'Busca em Largura')
          
        elif option == 2:
            # Executar busca profundidade
            # ...
            busca = BuscaProfundidade(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #plot_info(busca, 'Busca em profundidade')

        elif option == 3:
            # Executar busca gulosa
            # ...
            busca = BuscaGulosa(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #plot_info(busca, 'Busca gulosa')

        elif option == 4:
            # Executar busca A*
            # ...
            busca = BuscaAStar(start_state, goal_state)
            t_start = time.perf_counter()
            solucao = busca.resolver()
            t_end = time.perf_counter()
            printSolucao(solucao, t_end, t_start)
            #plot_info(busca, 'Busca em A*')


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
