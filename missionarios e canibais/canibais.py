#Somente modifiquei o em profundidade, por algum motivo ele não soluciona corretamente
from collections import deque

class BuscaProfundidade:
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print("ERRO: Há mais canibais que missionários em uma das bordas!\n")
            return False
        print(">>>Estado aceito.<<<\n")
        return True

    def generate_next_states(self, state):
        states = []
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        if barco == 'esquerda':
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            missionarios_esquerda - m,
                            canibais_esquerda - c,
                            'direita',
                            missionarios_direita + m,
                            canibais_direita + c
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)
        else:
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            missionarios_esquerda + m,
                            canibais_esquerda + c,
                            'esquerda',
                            missionarios_direita - m,
                            canibais_direita - c
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)

        return states

    def dfs(self, state, path, depth):
        self.estados_visitados.add(state)
        print(f"\n---------Estado atual: {state} (Profundidade: {depth})------------")
        if state == self.goal_state:
            print(f"Profundidade da solução: {len(path) - 1}")
            return path

        next_states = self.generate_next_states(state)
        for next_state in next_states:
            print(f"\nVerificando próximo estado: {next_state}")
            if next_state not in self.estados_visitados:
                print("Estado não visitado!!")
                new_path = path + [next_state]
                result = self.dfs(next_state, new_path, depth + 1)  # Incrementa a profundidade
                if result:
                    return result
            else:
                print("Estado já visitado!!")
        return None

    def resolver(self):
        return self.dfs(self.start_state, [self.start_state], 0)  # Inicia a profundidade com 0

class BuscaLargura:
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print("ERRO: Há mais canibais que missionários em uma das bordas!\n")
            return False
        print(">>>Estado aceito.<<<\n")
        return True

    def generate_next_states(self, state):
        states = []
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        if barco == 'esquerda':
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            max(missionarios_esquerda - m, 0),
                            max(canibais_esquerda - c, 0),
                            'direita',
                            min(missionarios_direita + m, 3),
                            min(canibais_direita + c, 3)
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)
        else:
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            min(missionarios_esquerda + m, 3),
                            min(canibais_esquerda + c, 3),
                            'esquerda',
                            max(missionarios_direita - m, 0),
                            max(canibais_direita - c, 0)
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)

        return states

    def bfs(self, state, path, depth):
        fila = deque()
        fila.append([state])

        while fila:
            path = fila.popleft()
            state = path[-1]

            if state == self.goal_state:
                print(f"Profundidade da solução: {len(path) - 1}")
                return path

            self.estados_visitados.add(state)
            next_states = self.generate_next_states(state)

            for next_state in next_states:
                if next_state not in self.estados_visitados:
                    if self.is_valid_state(next_state):
                        new_path = list(path)
                        new_path.append(next_state)
                        fila.append(new_path)

        return None

    def resolver(self):
        return self.bfs(self.start_state, [self.start_state], 0)  # Inicia a profundidade com 0

    
class BuscaGulosa:
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print("ERRO: Há mais canibais que missionários em uma das bordas!\n")
            return False
        print(">>>Estado aceito.<<<\n")
        return True

    def generate_next_states(self, state):
        states = []
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        if barco == 'esquerda':
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            missionarios_esquerda - m,
                            canibais_esquerda - c,
                            'direita',
                            missionarios_direita + m,
                            canibais_direita + c
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)
        else:
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            missionarios_esquerda + m,
                            canibais_esquerda + c,
                            'esquerda',
                            missionarios_direita - m,
                            canibais_direita - c
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)

        return states

    def heuristic(self, state):
        missionarios_esquerda, canibais_esquerda, _, _, _ = state
        return missionarios_esquerda + canibais_esquerda

    def greedy_search(self, state, path, depth):
        self.estados_visitados.add(state)
        print(f"\n---------Estado atual: {state} (Profundidade: {depth})------------")
        if state == self.goal_state:
            return path

        next_states = self.generate_next_states(state)
        next_states.sort(key=self.heuristic)  # Ordena os próximos estados com base na heurística
        for next_state in next_states:
            print(f"\nVerificando próximo estado: {next_state}")
            if next_state not in self.estados_visitados:
                print("Estado não visitado!!")
                new_path = path + [next_state]
                result = self.greedy_search(next_state, new_path, depth+1)
                if result:
                    return result
            else:
                print("Estado já visitado!")
        return None

    def resolver(self):
        return self.greedy_search(self.start_state, [self.start_state], 0)
    
class BuscaAStar:
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print("ERRO: Há mais canibais que missionários em uma das bordas!\n")
            return False
        print(">>>Estado aceito.<<<\n")
        return True

    def generate_next_states(self, state):
        states = []
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        if barco == 'esquerda':
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            missionarios_esquerda - m,
                            canibais_esquerda - c,
                            'direita',
                            missionarios_direita + m,
                            canibais_direita + c
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)
        else:
            for m in range(3):
                for c in range(3):
                    if m + c > 0 and m + c <= 2:
                        new_state = (
                            missionarios_esquerda + m,
                            canibais_esquerda + c,
                            'esquerda',
                            missionarios_direita - m,
                            canibais_direita - c
                        )
                        print(f"Novo estado: {new_state}")
                        if self.is_valid_state(new_state):
                            states.append(new_state)
        return states

    def heuristic(self, state):
        missionarios_esquerda, canibais_esquerda, _, _, _ = state
        return abs(missionarios_esquerda - 0) + abs(canibais_esquerda - 0)

    def a_star_search(self, state, path, depth):
        self.estados_visitados.add(state)
        print(f"\n---------Estado atual: {state} (Profundidade: {depth})------------")
        if state == self.goal_state:
            return path

        next_states = self.generate_next_states(state)
        next_states.sort(key=lambda x: self.heuristic(x) + len(path))  # Ordena os próximos estados com base na função de custo combinada
        for next_state in next_states:
            print(f"\nVerificando próximo estado: {next_state}")
            if next_state not in self.estados_visitados:
                print("Estado não visitado!!")
                new_path = path + [next_state]
                result = self.a_star_search(next_state, new_path, depth + 1)  # Incrementa a profundidade em cada chamada recursiva
                if result:
                    return result
            else:
                print("Estado já visitado!")
        return None


    def resolver(self):
        return self.a_star_search(self.start_state, [self.start_state], 0)