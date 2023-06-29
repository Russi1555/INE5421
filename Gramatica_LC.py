class GLC():
    def __init__(self, N, T, P, S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = P  # {Tx : ['T'], Ty: ['TN', 'T'], Tz: ['NTN', 'N', 'T']}
        self.inicial = S
        self.First, self.Follow, self.M = None, None, None
        self.TIPO = "GLC"

    def __repr__(self):
        string = ""
        for estado in self.regras:
            if estado == self.inicial:
                substring = (f"*{estado} -> ")
            else:
                substring = (f"{estado} -> ")
            for producao in self.regras[estado]:
                substring += producao
                substring += " | "
            string += substring[:-2]
            string += "\n"
        return string

    def ApresentarOpcoes(self):
        print("1- Fatoração") # Retorna GLC
        print("2- Remove recursão a esquerda") # Retorna GLC
        print("3- Detecta não determinismo") # Retorna None
        print("4- Gera Firsts") # Retorna None
        print("5- Gera Follows") # Retorna None
        print("6- Mostra First e Follow") # Retorna None
        print("7- Cria Tabela LL(1)") # Retorna None
        print("8- Mostra Tabela LL(1)") # Retorna None
        print("9- Cancelar")

        return (9, [self.factorization,
                    self.remove_recursividades,
                    self.non_determinism_detection,
                    self.assemble_first,
                    self.assemble_follow,
                    self.MostraFirst_Follow,
                    self.Cria_Tabela_LL1,
                    self.MostraTabelaLL1])
            

    def remover_improdutivos(self):
        t_marcados = set(self.terminais)  # Passo 1: marcar os terminais
        for producao in self.regras.values(): #Esse for muito provavelmente é desnecessário. Deixar aqui por enqunato
            for corpo in  producao:
                for simbolo in corpo:
                    if simbolo.islower():
                        t_marcados.add(simbolo)
        
        cabecas_marcadas = set() #Passo 2.1: Marcar cabeças com corpo marcado
        for cabeca,producao in self.regras.items():
            for corpo in producao:
                todos_simbolos_marcados = all(simbolo in t_marcados or simbolo.islower() for simbolo in corpo)
                if todos_simbolos_marcados:
                    cabecas_marcadas.add(cabeca)

        nt_marcados = cabecas_marcadas.copy()

        for cabeca, producao in self.regras.items(): #passo 2.2: atualizar a lista de NT's marcadas
            for corpo in producao:
                if all(simbolo in nt_marcados for simbolo in corpo):
                    nt_marcados.add(cabeca)

        marcados = nt_marcados.union(t_marcados) #unifica tudo como "simbolos marcados"

        gramatica_nova = GR(self.nao_terminais.copy(), self.terminais.copy(), {}, self.inicial)

        # Itera sobre tudo e deixa apenas as producoes que os simbolos estão marcados
        for cabeca, producao in self.regras.items():
            if cabeca in marcados:
                novas_producoes = []
                for body in producao:
                    if all(simbolo in marcados or simbolo in self.terminais for simbolo in body):
                        novas_producoes.append(body)
                if novas_producoes:
                    gramatica_nova.regras[cabeca] = novas_producoes

        return gramatica_nova
    
    def remover_inalcancaveis(self):
        alcancaveis = set([self.inicial])  # Passo 1: Marcar o NT inicial como alcançavel

        # Passo 2: Marcar simbolos que possam ser alcançados a partir do NT inicial
        marcados = set()
        while marcados != alcancaveis:
            marcados = alcancaveis.copy()
            for cabeca, producao in self.regras.items():
                if cabeca in alcancaveis:
                    for corpo in producao:
                        for symbol in corpo:
                            if symbol in self.nao_terminais:
                                alcancaveis.add(symbol)

        # Passo 3: remover simbolos inalcançaveis da gramática
        gramatica_nova = GR(set(), self.terminais.copy(), {}, self.inicial)
        for cabeca, producao in self.regras.items():
            if cabeca in alcancaveis:
                producoes_atualizadas = []
                for corpo in producao:
                    if all(symbol in alcancaveis or symbol in self.terminais for symbol in corpo):
                        producoes_atualizadas.append(corpo)
                if producoes_atualizadas:
                    gramatica_nova.regras[cabeca] = producoes_atualizadas

        return gramatica_nova
        print(self)

    def check_recursao_esquerda(self):
        recursao_esquerda = set()
        
        for nt in self.regras: #Passo 1: Identificar as producoes com recursividade direta
            producoes = self.regras[nt]
            for producao in producoes:
                if producao[0] == nt:
                    recursao_esquerda.add(nt)
                    break
        return recursao_esquerda
    
    def remover_recursao_esquerda(self):
        recursao_esquerda = self.check_recursao_esquerda()
        while recursao_esquerda != set():
            #Passo 2: Para cada nt com recursividade direta
            for nt in recursao_esquerda:
                producoes_novas = []
                producoes_restantes = []

                for producao in self.regras[nt]:
                    if producao[0] == nt:
                        nova_producao = producao[1:] +nt+ "'" #troca t e nt' de posicao
                        producoes_novas.append(nova_producao) #producoes_novas = producoes atualizadas
                    else:
                        producoes_restantes.append(producao + nt + "'") #producoes sem recursividade permanecem em nt, producoes novas vão pra nt'

                producao_vazia = '&'
                producoes_novas.append(producao_vazia) #acrescenta epsilon as nt'

                self.regras[nt] = producoes_restantes
                novo_nt = nt + "'"
                self.regras[novo_nt] = producoes_novas 

            recursao_esquerda = set()
            #Checar se foi tudo resolvido, vai retornar o conjunto para ser tratado recursivamente por fora
            for nt in self.regras:
                producoes = self.regras[nt]

                for producao in producoes:

                    if producao[0] == nt:
                        recursao_esquerda.add(nt)
                        break

            return recursao_esquerda 
        
        #Talvez precise voltar pra fazer o Passo 3 / 5

    def remove_recursividades(self):
        novoGLC = GLC(self.nao_terminais.copy(), self.terminais.copy(), self.regras.copy(), self.inicial)
        ciclo_no_inicial = False
        #Verifica há um ciclo na produção do NT inicial
        for producao in self.regras[self.inicial]:
            if self.inicial in producao:
                ciclo_no_inicial = True
                break
        
        #Se há, é necessário fazer uma remoção da recursividade direta ou
        #sofrer com um loop infinito
        if ciclo_no_inicial:
            if self.check_recursao_esquerda() != set():
                self.remover_recursao_esquerda()
        
        nt = self.nao_terminais

        #IMPLEMENTAÇÃO DO ALGORITMO DOS SLIDES

        for i in range(0,len(nt)):
            Ai = nt[i]
            for j in range(i):
                Aj = nt[j]
                for producao in self.regras[Ai]:
                    if Aj in producao: #Se Ai => Ajα
                        for producao_substituta in self.regras[Aj]:
                            #Remova Ai => Aj de P
                            #Se aj =>  β ∈ P então P′ = P′ ∪ {Ai ::= βα}
                            nova_producao = producao.replace(Aj, producao_substituta)
                            if producao in self.regras[Ai]:
                                indice = self.regras[Ai].index(producao)
                                self.regras[Ai][indice] = nova_producao
                            else:
                                self.regras[Ai].append(nova_producao)

        #Elimine as recursões diretas de P' com lado esquerdo Ai
        if self.check_recursao_esquerda() != set():
            self.remover_recursao_esquerda()
        return novoGLC
        
    def non_determinism_detection(self):
        regras = self.regras
        for estado in list(regras):
            first_prods = {}
            for prod in regras.get(estado):
                if prod[0] in self.terminais:
                    if prod[0] not in first_prods:
                        first_prods.update({prod[0]: [prod]})
                    else:
                        first_prods.get(prod[0]).append(prod)
            for nt in first_prods:
                if len(first_prods.get(nt)) > 1:
                    self.non_determinism_alert(estado, first_prods.get(nt))
        return None
    
    def non_determinism_alert(self, estado, prods):
        print(f'nao determinismo detectado no estado: {estado}, producoes nao deterministicas: {estado} -> {prods}\n')

    def factorization(self):
        novoGLC = GLC(self.nao_terminais.copy(), self.terminais.copy(), self.regras.copy(), self.inicial)
        regras = self.regras
        for estado in list(regras):
            first_prods = {}
            for prod in regras.get(estado):
                if prod[0] in self.terminais:
                    if prod[0] not in first_prods :
                        first_prods.update({prod[0]: [prod]})
                    else:
                        first_prods.get(prod[0]).append(prod)
            additional_states = 0
            for nt in first_prods:
                if len(first_prods.get(nt)) > 1:
                    new_state = f'{estado}`'
                    self.non_determinism_alert(estado, first_prods.get(nt))
                    if f'{estado}`' not in self.regras:
                        new_prods = nt + new_state
                        additional_states += 1
                    else:
                        state = f'{estado}`'
                        for i in range(additional_states):
                            state = state + '`'
                        new_state = state
                        new_prods = nt + state
                    for i in range(len(first_prods.get(nt))):
                        regras.get(estado).remove(first_prods.get(nt)[i])
                        first_prods.get(nt)[i] = first_prods.get(nt)[i].replace(nt, '')

                    regras.update({new_state: []})
                    for prod in first_prods.get(nt):
                        regras.get(new_state).append(prod)
                    regras.get(estado).append(new_prods)
        self.regras.update(regras)

        return novoGLC # Retorna o GLC antes da fatoração

    def remove_indirect(self):
        pass
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=- FIRST
    def assemble_first(self): 
        self.First = {T:set() for T in self.nao_terminais}
        for NT, regra in self.regras.items():
            if not self.First[NT]:
                self.First[NT] = self.First[NT] | self.pegaFirst(regra, NT)
        return None

    def pegaFirst(self, regra, NT):
        first = set()
        for r in regra:
            for ind, i in enumerate(r):
                if i in self.terminais+['&']:
                    first.add(i)
                    break
                elif NT == i:
                    break
                elif self.First[i]:
                    passo = self.First[i].copy()
                    if '&' not in passo:
                        first = first | passo
                        break
                    elif ind+1 < len(r):
                        passo.remove('&')
                    first = first | passo
                else:
                    passo = self.pegaFirst(self.regras[i], i)
                    self.First[i] = passo.copy()
                    if '&' not in passo:
                        first = first | passo
                        break
                    elif ind+1 < len(r):
                        passo.remove('&')
                    first = first | passo
        return first
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= FOLLOW
    
    def assemble_follow(self): # Tem que ter feito o First primeiro
        self.Follow = {X:set() for X in self.nao_terminais}
        self.Follow[self.inicial].add('$')
        follow = dict()
        while follow != self.Follow:
            follow = self.Follow.copy()
            for X in self.nao_terminais:
                self.Follow[X] = self.pegaFollow(X)
        return None
            
    def pegaFollow(self, X):
        conjunto = self.Follow[X].copy()
        for Y in self.nao_terminais:
            for prod in self.regras[Y]:
                if X in prod:
                    ind = prod.index(X)
                    while ind < len(prod):
                        if ind >= len(prod)-1:
                            conjunto = conjunto | self.Follow[Y].copy()
                            break
                        else:
                            ind += 1
                            if prod[ind] in self.terminais:
                                conjunto.add(prod[ind])
                                break
                            else:
                                if prod[ind] == X:
                                    continue
                                passo = self.First[prod[ind]].copy()
                                if '&' not in passo:
                                    conjunto = conjunto | passo
                                    break
                                passo.remove('&')
                                conjunto = conjunto | passo
        return conjunto

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def MostraFirst_Follow(self):
        print("  X  |             FIRST(X)              |        FOLLOW(X)")
        for E in self.nao_terminais:
            print(f"  {E}  |", end="")
            if self.First is None:
                print("{None}", 27*" ", "|{None}")
                continue
            conjunto = self.First[E].copy()
            tam = 33-len(str(conjunto))
            if self.Follow is None:
                print(f"{conjunto}", tam*" ", "|{None}")
                continue
            print(f"{str(conjunto)}", tam*" ", f"|{self.Follow[E]}")
        return None

 # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-= TABElA LL(1)
    def Cria_Tabela_LL1(self):
        if self.First is None:
            self.assemble_first()
        if self.Follow is None:
            self.assemble_follow()
        # Tabela M -> nº de linhas = len(N) , nº de colunas = len(T)+1
        self.M = {N:{T:"" for T in self.terminais+['$']} for N in self.nao_terminais}
        for NT in self.nao_terminais:
            for regra in self.regras[NT]:
                conjunto = self.pegaFirstRegra(NT, regra)
                for terminais in conjunto:
                    if terminais == '&':
                        continue
                    self.M[NT][terminais] = regra # Verifica se repete
                if '&' in conjunto:
                    for terminais in self.Follow[NT]:
                        self.M[NT][terminais] = regra # Verifica se repete
        return None

    def pegaFirstRegra(self, NT, regra):
        if regra[0] in self.terminais+['&']:
            return set([regra[0]])
        passo = self.First[regra[0]].copy()
        if '&' not in passo:
            return passo
        if len(regra) > 1:
            passo.remove('&')
        ind = 1
        while ind < len(regra):
            if regra[ind] in self.terminais:
                passo.add(regra[ind])
                break

            first = self.First[regra[ind]].copy()
            if '&' not in first:
                passo = passo | first
                break
            ind += 1
            if ind >= len(regra):
                passo = passo | first
                break
            first.remove('&')
            passo = passo | first
        return passo

    def MostraTabelaLL1(self):
        if self.M is None:
            print("A tabela não foi criada") 
            return None
        print('  |', end='')
        for i in self.terminais+['$']:
            print("  ",i,"  |", end='')
        print()
        for lin,v in self.M.items():
            print(lin, end=' |')
            for col in v.values():
                if col == '':
                    col = '--'
                tam = 7 - len(col)
                print(col, end='')
                print(tam*' ', end='|')
            print()
        return None

    def Testa_Palavra(self, w, passo_A_passo=False):
        if self.M is None:
            self.Cria_Tabela_LL1()
        pilha = ['$', self.inicial]

        if passo_A_passo: # APENAS PRINTS -=-=-=-=-
            print(f"Palavra:\n-=-=-=- {w} -=-=-=-\n")
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        for ind, simbolo in enumerate(w):
            if not pilha or pilha[-1] == '$':
                return False

            while simbolo != pilha[-1] and pilha[-1] != '$':
                if pilha[-1] in self.terminais: # Simbolo diferente do esperado
                    return False

                # Pega o corpo de produção a partir da tabela
                producao = [caractere for caractere in self.M[pilha[-1]][simbolo]]
                
                if passo_A_passo: # APENAS PRINTS -=-=-=-=-
                    tam = len(f"Pilha: {pilha}")
                    tam2 = len(f"  ({simbolo}) |   {pilha[-1]} -> {self.M[pilha[-1]][simbolo]}")
                    print(f"Pilha: {pilha}", (60-tam)*" ",f"  ({simbolo}) |   {pilha[-1]} -> {self.M[pilha[-1]][simbolo]}", end='') 
                    print((25-tam2)*" ","|   ", w[ind:])
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                
                if not producao: # Não tem caminho na tabela
                    return False
                
                pilha.pop(-1) # Remove a cabeça da produçao

                if producao[0] != '&': # Caso não seja Epsilon, colocar o corpo da produção invertido na pilha
                    pilha += reversed(producao)
            
            if passo_A_passo: # APENAS PRINTS -=-=-=-=-
                tam = len(f"Pilha: {pilha}")
                tam2 = len(f"  ({simbolo}) |   {simbolo} -> &")
                print(f"Pilha: {pilha}", (60-tam)*" ",f"  ({simbolo}) |   {simbolo} -> &", end='')
                print((25-tam2)*" ","|   ", w[ind+1:])
            # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

            pilha.pop(-1) # Quando topo da pilha == simbolo

        if passo_A_passo: # APENAS PRINTS -=-=-=-=-
            tam = len(f"Pilha: {pilha}")
            print(f"Pilha: {pilha}", (60-tam)*" ",f" (--) |")
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        return True if pilha and pilha[-1] == '$' else False