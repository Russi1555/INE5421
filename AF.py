class AF():
    def __init__(self,Estados,Alfabeto,Transicao,Qo,F):
        self.Estados = Estados
        self.Alfabeto = Alfabeto
        self.Transicoes = Transicao #[estado,simbolo,estado]
        self.Qo = Qo
        self.F = F
    def __repr__(self):
        string = f"Estados: {self.Estados}\n"
        string += f"Estado inicial : {self.Qo}\n"
        string+= f"Estados aceitacao : {self.F}\n"
        string+= f"Alfabeto: {self.Alfabeto}\n"
        string+= f"Transicoes: {self.Transicoes}\n"
        return string
    def fechamento_ep(self, estado):
        fechamento = set([estado])

        pilha = [estado]
        while pilha:
            current_state = pilha.pop()

            # Check if current state has epsilon transitions
            epsilon_transitions = [transicao[2] for transicao in self.Transicoes
                                   if transicao[0] == current_state and transicao[1] == '&']

            for transition_state in epsilon_transitions:
                if transition_state not in fechamento:
                    fechamento.add(transition_state)
                    pilha.append(transition_state)

        return fechamento
    
    def novas_transicoes(self):
        if '&' in self.Alfabeto:
            Alfabeto = self.Alfabeto
            Alfabeto.remove('&')
        novas_transicoes = []
        #fechamento epsilon pro estado inicial
        fechamento_inicial = frozenset(self.fechamento_ep(self.Qo))
        
        #fila para processar estados
        fila_estados = [fechamento_inicial]
        
        #conjunto pra registrar estados já processados
        estados_processados = set([fechamento_inicial])
        
        while fila_estados:
            estado_atual = fila_estados.pop(0)
            
            for simbolo in self.Alfabeto:
                transicoes_simbolo = set()
                
                for estado in estado_atual:
                    #encontra transições para o atual estado e simbolo
                    transicoes = [transicao[2] for transicao in self.Transicoes
                                   if transicao[0] == estado and transicao[1] == simbolo]
                    transicoes_simbolo.update(transicoes)
                
                if transicoes_simbolo:
                    #calcula fechamento epsilon pra transicao
                    fechamento_simbolo = set()
                    for estado in transicoes_simbolo:
                        fechamento_simbolo.update(self.fechamento_ep(estado))

                    fechamento_simbolo = frozenset(fechamento_simbolo)
                    
                    if fechamento_simbolo not in estados_processados:
                        #adiciona o novo estado e suas transições a fila
                        fila_estados.append(fechamento_simbolo)
                        estados_processados.add(fechamento_simbolo)
                        
                    novas_transicoes.append([estado_atual, simbolo, fechamento_simbolo])
        novas_transicoes = [[list(estado), simbolo, list(fechamento)] for estado, simbolo, fechamento in novas_transicoes]
        return novas_transicoes
                    
    
    def convert_to_dfa(self):
        dfa_states = set()
        dfa_transitions = []
        dfa_initial_state = frozenset(self.fechamento_ep(self.Qo))
        dfa_accepting_states = []

        queue = [dfa_initial_state]
        dfa_states.add(dfa_initial_state)

        while queue:
            current_state = queue.pop(0)

            for symbol in self.Alfabeto:
                next_states = set()
                
                for state in current_state:
                    transitions = [transicao[2] for transicao in self.Transicoes
                                   if transicao[0] == state and transicao[1] == symbol]
                    for transition in transitions:
                        next_states.update(self.fechamento_ep(transition))

                next_states = frozenset(next_states)
                
                if next_states not in dfa_states:
                    dfa_states.add(next_states)
                    queue.append(next_states)

                dfa_transitions.append([list(current_state), symbol, list(next_states)])

        for state in dfa_states:
            if any(accept_state in state for accept_state in self.F):
                dfa_accepting_states.append(list(state))
        
        dfa_states = [[list(estado)] for estado in dfa_states]
        for estado in dfa_states:
            if estado == [[]]:
                dfa_states.remove(estado)
        dfa_transitions = [[list(estado), simbolo, list(fechamento)] for estado, simbolo, fechamento in dfa_transitions]
        
        existe_vazio = True
        while existe_vazio:
            existe_vazio = False
            for transicao in dfa_transitions:
                if transicao[0] == [] or transicao[2] == []:
                    dfa_transitions.remove(transicao)
                    existe_vazio= True
        
        
        dfa_initial_state = list(dfa_initial_state)
        
        #print(dfa_transitions[4][2])
        
        dfa = AF(dfa_states, self.Alfabeto, dfa_transitions, dfa_initial_state, dfa_accepting_states)
        return dfa
        
                        
automata = AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              [['q0', 'a', 'q1'],
               ['q1', '&', 'q2'],
               ['q1', 'a', 'q3'],
               ['q2', 'b', 'q0']],
              'q0',
              ['q3'])

automato2 = AF(['1','2','3'],
               ['a','b'],
               [['1','b','2'],
                ['1','&','3'],
                ['2','a','1'],
                ['2','b','2'],
                ['3','a','2'],
                ['3','a','3'],
                ['3','b','3']],
               '1',
               ['2'])

state = '3'
closure = automata.fechamento_ep('q1')
print(automato2.convert_to_dfa())
print(automata.Estados)
print(closure)  # Output: {'q1', 'q2'}
