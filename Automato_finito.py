from Gramatica_Regular import GR


class AF():
    def __init__(self,Estados,Alfabeto,Transicao,Qo,F):
        self.Estados = Estados
        self.Alfabeto = Alfabeto
        self.Transicoes = Transicao #{estado:{simbolo:estado}}
        self.Qo = Qo
        self.F = F
        # Verifica se tem transição por epsilon, para colocar mais uma coluna na tabela
        self.epsilon = False
        for dic in Transicao.values():
            if '&' in list(dic.keys()):
                self.epsilon = True
                break
            
    def __repr__(self):
        string = f"Estados: {self.Estados}\n"
        string += f"Estado inicial : {self.Qo}\n"
        string+= f"Estados aceitacao : {self.F}\n"
        string+= f"Alfabeto: {self.Alfabeto}\n"
        string+= f"Transicoes: {self.Tabela()}\n"
        return string
    
    def Tabela(self): # Retorna a tabela de transicoes
        string = "\033[92;1m\n      δ     \033[0m|"
        for i in self.Alfabeto: # Coloca a parte do alfabeto
            string += f"    {i}     |"

        SIMBOLOS = self.Alfabeto
        if self.epsilon:
            string += f"\033[91m     ε    \033[0m|"
            SIMBOLOS += ['&']

        TRACO = (len(string)-(20 if self.epsilon else 13))*"-"
        string = string[:-1] + "\n"+TRACO+"\n"
        
        for estado in self.Estados: # Transições dos estados
            if len(estado.split(',')) > 1: # Caso seja ambiguo (a-> B,C)
                est = f"{'{'+estado+'}'}"
            else:
                est = estado
            Qo = est if estado not in self.F else "*"+est # Caso seja estado final
            if estado == self.Qo:
                Qo = "->"+Qo # Caso seja estado inicial
            tam = len(Qo)
            string += ((5-tam//2)*" ")+Qo+((6-tam//2)*" ")+"|" # Estado Inicial
            for alf in SIMBOLOS:
                if estado in list(self.Transicoes.keys()) and alf in list(self.Transicoes[estado].keys()):
                    est = self.Transicoes[estado][alf]
                    if len(est.split(',')) > 1: # Caso seja ambiguo (a-> B,C)
                        est = f"{'{'+est+'}'}"
                else:
                    est = "--"
                tam = len(est)
                string += ((5-tam//2)*" ")+est+((5-tam//2)*" ")+"|"
            string = string[:-1] + "\n"+TRACO+"\n"
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
                    
    def convert_to_AFD(self): #TODO: ajeitar variaveis e comentar
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
                        next_states.update(sorted(self.fechamento_ep(transition)))

                next_states = frozenset(next_states)
                
                if next_states not in dfa_states:
                    dfa_states.add(next_states)
                    queue.append(next_states)

                dfa_transitions.append([sorted(list(current_state)), symbol, sorted(list(next_states))])
            
        for state in dfa_states:
            if any(accept_state in state for accept_state in self.F):
                dfa_accepting_states.append(sorted(list(state)))
        
        dfa_states = sorted([sorted(list(estado)) for estado in dfa_states])
        for estado in dfa_states:
            if estado == []:
                dfa_states.remove(estado)
        dfa_transitions = [[list(estado), simbolo, list(fechamento)] for estado, simbolo, fechamento in dfa_transitions]
        
        existe_vazio = True
        while existe_vazio:
            existe_vazio = False
            for transicao in dfa_transitions:
                if transicao[0] == [] or (transicao[2] == [] and transicao[2] not in self.F):
                    dfa_transitions.remove(transicao)
                    existe_vazio= True
                    
        
        
        dfa_initial_state = sorted(list(dfa_initial_state))
        dfa_transitions = sorted(dfa_transitions)
        dfa_accepting_states = sorted(dfa_accepting_states)
        
        #print(dfa_transitions[4][2])
        
        dfa = AF(dfa_states, self.Alfabeto, dfa_transitions, dfa_initial_state, dfa_accepting_states)
        return dfa
        
    def convert_to_GR(self):  #TODO: ajeitar variaveis e comentar
        nao_terminais = [f'N{i}' for i in range(len(self.Estados))]
        #print(nao_terminais)
        simbolo_inicial = nao_terminais[self.Estados.index(self.Qo)]
        #print(simbolo_inicial)

        estados_finais = []
        for estado_aceitacao in self.F:
            #regras.append([nao_terminais[self.Estados.index(estado_aceitacao)], '$'])
            estados_finais.append(estado_aceitacao)
        
        regras = []
        for transicao in sorted(self.Transicoes):
            inicio = nao_terminais[self.Estados.index(transicao[0])]
            terminal = transicao[1]
            if transicao[2] != []:
                fim = nao_terminais[self.Estados.index(sorted(transicao[2]))]

            if transicao[2] in estados_finais:
                regras.append([inicio, terminal])              
            if fim:
               # print(f"{inicio} -> {terminal}")
                regras.append([inicio, terminal, fim])
        
        
       # print(regras)
        GR_resultante = GR(nao_terminais, self.Alfabeto, regras, simbolo_inicial)
        return GR_resultante
                        
    def minimiza_AFD(self): # Minimiza Automato finito
        self.removeInacessivel_e_Mortos()
        # Ajusta todos os estados em Finais e NãoFinais
        Conjuntos = [list(set(self.Estados) - set(self.F)), self.F]
        NovoConjunto = []
        while True: # Enquanto não alterar
            for conj in Conjuntos:
                subConj = []
                for est in conj:
                    b = False
                    for cj in subConj:
                        if est in cj:
                            break
                    else:
                        subConj.append([est])
                        dest = pegaEnderecoConjunto(est, self.Transicoes, Conjuntos, self.Alfabeto) # Pega os destinos
                        for i in conj:
                            for cj in subConj:
                                if i in cj:
                                    break
                            else:
                                if pegaEnderecoConjunto(i, self.Transicoes, Conjuntos, self.Alfabeto, dest): # Compara os destinos
                                    subConj[-1].append(i)
                NovoConjunto += subConj
            if len(Conjuntos) == len(NovoConjunto): # Caso tenham os mesmos numeros de conjuntos
                for c in Conjuntos:
                    for n in NovoConjunto:
                        #print(sorted(n),sorted(c))
                        if sorted(n) == sorted(c):
                            break
                    else: # Não achou igual
                        break
                else:
                    break
            Conjuntos, NovoConjunto = NovoConjunto.copy(), []
        #print("Novo> ",NovoConjunto)
        # -=-=-=-=-=-=- Reajusta o Automato =-=-=-=-=-=-=-=-=-=-=-=-=
        self.Estados = [f"E{n}" for n in range(len(Conjuntos))]
        # -=-=-=- Novos estados Finais e inicial -=-=-=-
        novoFim = []
        for ind,conj in enumerate(Conjuntos): 
            if self.Qo in conj:
                self.Qo = f"E{ind}"
            for f in self.F:
                if f in conj:
                    novoFim.append(f"E{ind}")
                    break
        self.F = novoFim

        # -=-=-=-=-=-= Novas Transições -=-=-=-=-=-=-
        novaTrans = {} #{estado:{simbolo:estado}}
        for n in range(len(Conjuntos)):
            dest = pegaEnderecoConjunto(Conjuntos[n][0], self.Transicoes, Conjuntos, self.Alfabeto)
            #print(dest)
            for a,i in zip(self.Alfabeto, dest):
                if Conjuntos[n][0] in list(self.Transicoes.keys()) and a in list(self.Transicoes[Conjuntos[n][0]].keys()):
                    if f"E{n}" not in list(novaTrans.keys()):
                        novaTrans[f"E{n}"] = {}
                    novaTrans[f"E{n}"][a] = f"E{i}"
        self.Transicoes = novaTrans

    def removeInacessivel_e_Mortos(self):
        global acesso, transicoes
        transicoes = self.Transicoes
        acesso = set([self.Qo])
        PassaEstados(self.Qo) # Inacessiveis

        for l in range(2):        
            estFora = set(self.Estados) - acesso
            deletar = []
            for i in estFora:
                if i in list(self.Transicoes.keys()):
                    del self.Transicoes[i]
                    self.Estados.remove(i)
                for k,v in self.Transicoes.items():
                    for k2,v2 in v.items():
                        if v2 == i:
                            deletar.append((k, k2))
            for i in deletar:
                if i[0] in list(self.Transicoes.keys()):
                    del self.Transicoes[i[0]][i[1]]
            # -=-=-=-=-=-=-=-=-=-=-=- Remove estados Mortos -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            transicoes = self.Transicoes
            acesso = set(self.F)
            for i in self.F:
                VoltaEstados(i) # Mortos

        

def VoltaEstados(est): # Para achar estados Mortos
    global acesso, transicoes
    for k,g in transicoes.items():
        if k not in acesso and est in list(g.values()):
            acesso.add(k)
            VoltaEstados(k)
    return
    

def PassaEstados(est): # Para achar estados inacessiveis
    global acesso, transicoes
    if est not in list(transicoes.keys()):
        return
    for i in transicoes[est].values():
        if i not in acesso:
            acesso.add(i)
            PassaEstados(i)
    return

def pegaEnderecoConjunto(est, transicoes, Conjuntos, alfabeto, destino=None): # Para Minimizar o AFD
    if destino is None: # Pega os conjuntos de cada transição ("--" quando não tem transição)
        if est not in list(transicoes.keys()):
            return ["--" for i in range(len(alfabeto))]
        dest = []
        for i in alfabeto:
            if i in list(transicoes[est].keys()):
                for ind, l in enumerate(Conjuntos):
                    #print(transicoes[est][i], l)
                    if transicoes[est][i] in l:
                        dest.append(ind)
                        break
                else:
                    print("Não achou")
            else:
                dest.append("--")
        #print("Destino: ",dest)
        return dest
    else: # Verifica se aponta pros mesmos Conjuntos
        if est not in list(transicoes.keys()):
            if all(elemento == '--' for elemento in destino):
                return True
            return False
        for i,d in zip(alfabeto, destino):
            if i in list(transicoes[est].keys()): # Caso tenha uma transição
                if d == "--" or transicoes[est][i] not in Conjuntos[d]:
                    #print("Destino diferente")
                    return False
            elif d != "--": # Caso não tenha transição e o destino tenha
                #print("Destino diferente")
                return False
        #print("Mesmo Destino")
        return True
