from collections import deque
import sys, time

class BuscaProfundidade:
    
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state
        self.depth = 0
        self.qntNodesGen = 0
        self.qntNodesExp = 0
        self.qntNodesFront = 0
        
        self.resultOut = None 
        try:
            self.resultOut = open("missionarios e canibais/out/bf-result.txt", "w")
        except:
            pass
        print("------------------Algoritmo: Busca em profundidade------------------\n", file=self.resultOut)

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print(f"Expandido: {state}", file=self.resultOut)
            print("ERRO: Ha mais canibais que missionarios em uma das bordas!\n", file=self.resultOut)
            return False
        return True

    def generate_next_states(self, state):
        self.qntNodesFront = 0
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
                        
                        self.qntNodesGen += 1
                        self.qntNodesFront +=1
                        
                        if self.is_valid_state(new_state):
                            states.append(new_state)
                            self.qntNodesExp += 1
                            print(f"Expandido: {new_state} (Estado aceito)\n", file=self.resultOut)
                            
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

                        self.qntNodesGen += 1
                        self.qntNodesFront +=1
                        
                        if self.is_valid_state(new_state):
                            states.append(new_state)
                            self.qntNodesExp += 1
                            print(f"Expandido: {new_state} (Estado aceito)\n", file=self.resultOut)
                            
        return states

    def dfs(self, state, path, depth):
        self.estados_visitados.add(state)
        if state == self.goal_state:
            print(f"Profundidade da solução: {depth}", file=self.resultOut)
            print(f"Consumo de memória: {sys.getsizeof(self.estados_visitados)} bytes\n") 
            self.depth = depth
            return path
        
        print(f"\n---------Estado atual: {state} (Profundidade: {depth})------------\n", file=self.resultOut)

        next_states = self.generate_next_states(state)

        for next_state in next_states:
            print(f"Verificando proximo estado: {next_state}", file=self.resultOut)
            if next_state not in self.estados_visitados:
                print("Estado nao visitado!!", file=self.resultOut)
                new_path = path + [next_state]
                result = self.dfs(next_state, new_path, depth + 1)  # Incrementa a profundidade
                if result:
                    return result
            else:
                print("Estado ja visitado!!", file=self.resultOut)
        return None

    def resolver(self):
        resultado = self.dfs(self.start_state, [self.start_state], 0)  # Inicia a profundidade com 0
        return resultado

class BuscaLargura:
    def __init__(self, left_missionaries, left_cannibals, right_missionaries, right_cannibals, boat_on_left,
                 parent_state=None):
        self.left_missionaries = left_missionaries
        self.left_cannibals = left_cannibals
        self.right_missionaries = right_missionaries
        self.right_cannibals = right_cannibals
        self.boat_on_left = boat_on_left
        self.parent_state = parent_state

    # Restante das funções da classe State
    def is_valid(self):
        if (
            self.left_missionaries < 0
            or self.left_cannibals < 0
            or self.right_missionaries < 0
            or self.right_cannibals < 0
        ):
            return False
        if (
            self.left_missionaries > 0
            and self.left_missionaries < self.left_cannibals
            or self.right_missionaries > 0
            and self.right_missionaries < self.right_cannibals
        ):
            return False
        return True

    def is_goal_state(self):
        return (
            self.left_missionaries == 0
            and self.left_cannibals == 0
            and self.right_missionaries == self.right_cannibals
        )

    def __str__(self):
        return f"[{self.left_missionaries}, {self.left_cannibals}, {self.right_missionaries}, {self.right_cannibals}, {'Esquerda' if self.boat_on_left else 'Direita'}]"
    
class BuscaGulosa:
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state
        self.depth = 0
        self.qntNodesGen = 0
        self.qntNodesExp = 0
        self.qntNodesFront = 0
        self.resultOut = None 
        try:
            self.resultOut = open("missionarios e canibais/out/bg-result.txt", "w")
        except:
            pass
        print("------------------Algoritmo: Busca Gulosa------------------\n", file=self.resultOut)

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print(f"Expandido: {state}", file=self.resultOut)
            print("ERRO: Ha mais canibais que missionarios em uma das bordas!\n", file=self.resultOut)
            return False
        
        return True

    def generate_next_states(self, state):
        self.qntNodesFront = 0
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
                        
                        self.qntNodesGen += 1
                        self.qntNodesFront +=1
                        
                        if self.is_valid_state(new_state):
                            states.append(new_state)
                            self.qntNodesExp += 1
                            print(f"Expandido: {new_state} ( Estado aceito )\n", file=self.resultOut)
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
                        self.qntNodesGen += 1
                        self.qntNodesFront +=1
                        
                        if self.is_valid_state(new_state):
                            states.append(new_state)
                            self.qntNodesExp += 1
                            print(f"Expandido: {new_state} ( Estado aceito )\n", file=self.resultOut)

        return states

    def heuristic(self, state):
        missionarios_esquerda, canibais_esquerda, _, _, _ = state
        return missionarios_esquerda + canibais_esquerda

    def greedy_search(self, state, path, depth):
        self.estados_visitados.add(state)
        print(f"\n---------Estado atual: {state} (Profundidade: {depth})------------\n", file=self.resultOut)
        if state == self.goal_state:
            print(f"Consumo de memória: {sys.getsizeof(self.estados_visitados)} bytes\n") 
            self.depth = depth
            return path

        next_states = self.generate_next_states(state)
        next_states.sort(key=self.heuristic)  # Ordena os proximos estados com base na heurística
        for next_state in next_states:
            print(f"Verificando proximo estado: {next_state}", file=self.resultOut)
            if next_state not in self.estados_visitados:
                print("Estado nao visitado!!", file=self.resultOut)
                new_path = path + [next_state]
                result = self.greedy_search(next_state, new_path, depth+1)
                if result:
                    return result
            else:
                print("Estado ja visitado!", file=self.resultOut)
        return None

    def resolver(self):
        return self.greedy_search(self.start_state, [self.start_state], 0)
    
class BuscaAStar:
    def __init__(self, start_state, goal_state):
        self.estados_visitados = set()
        self.start_state = start_state
        self.goal_state = goal_state
        self.depth = 0
        self.qntNodesGen = 0
        self.qntNodesExp = 0
        self.qntNodesFront = 0
        
        self.resultOut = None 
        try:
            self.resultOut = open("missionarios e canibais/out/bas-result.txt", "w")
        except:
            pass
        print("------------------Algoritmo: Busca A*------------------\n", file=self.resultOut)

    def is_valid_state(self, state):
        missionarios_esquerda, canibais_esquerda, barco, missionarios_direita, canibais_direita = state

        # Verifica se o estado é válido
        if missionarios_esquerda < 0 or canibais_esquerda < 0 or missionarios_direita < 0 or canibais_direita < 0:
            return False
        if missionarios_esquerda > 3 or canibais_esquerda > 3 or missionarios_direita > 3 or canibais_direita > 3:
            return False
        if (missionarios_esquerda < canibais_esquerda and missionarios_esquerda > 0) or (missionarios_direita < canibais_direita and missionarios_direita > 0):
            print(f"Expandido: {state}", file=self.resultOut)
            print("ERRO: Ha mais canibais que missionarios em uma das bordas!\n", file=self.resultOut)
            return False
        return True

    def generate_next_states(self, state):
        self.qntNodesFront = 0
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
  
                        self.qntNodesGen += 1
                        self.qntNodesFront +=1
                        
                        if self.is_valid_state(new_state):
                            states.append(new_state)
                            self.qntNodesExp += 1
                            print(f"Expandido: {new_state} ( Estado aceito )\n", file=self.resultOut)
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

                        self.qntNodesGen += 1
                        self.qntNodesFront +=1
                        
                        if self.is_valid_state(new_state):
                            states.append(new_state)
                            self.qntNodesExp += 1
                            print(f"Expandido: {new_state} ( Estado aceito )\n", file=self.resultOut)
        return states

    def heuristic(self, state):
        missionarios_esquerda, canibais_esquerda, _, _, _ = state
        return abs(missionarios_esquerda - 0) + abs(canibais_esquerda - 0)

    def a_star_search(self, state, path, depth):
        self.estados_visitados.add(state)
        print(f"\n---------Estado atual: {state} (Profundidade: {depth})------------\n", file=self.resultOut)
        if state == self.goal_state:
            print(f"Consumo de memória: {sys.getsizeof(self.estados_visitados)} bytes\n") 
            self.depth = depth
            return path

        next_states = self.generate_next_states(state)
        next_states.sort(key=lambda x: self.heuristic(x) + len(path))  # Ordena os proximos estados com base na função de custo combinada
        for next_state in next_states:
            print(f"Verificando proximo estado: {next_state}", file=self.resultOut)
            if next_state not in self.estados_visitados:
                print("Estado nao visitado!!", file=self.resultOut)
                new_path = path + [next_state]
                result = self.a_star_search(next_state, new_path, depth + 1)  # Incrementa a profundidade em cada chamada recursiva
                if result:
                    return result
            else:
                print("Estado ja visitado!", file=self.resultOut)
        return None


    def resolver(self):
        return self.a_star_search(self.start_state, [self.start_state], 0)
