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

    def remove_non_determinism(self):
        pass  # TODO

    def factorization(self):
        regras = self.regras
        for estado in list(regras):
            first_prods = {}
            for prod in regras.get(estado):
                if prod[0] in self.terminais:
                    if prod[0] not in first_prods :
                        first_prods.update({prod[0]: [prod]})
                    else:
                        first_prods.get(prod[0]).append(prod)
            for nt in first_prods:
                if len(first_prods.get(nt)) > 1:
                    new_prods = nt + f'{estado}`'
                    for i in range(len(first_prods.get(nt))):
                        regras.get(estado).remove(first_prods.get(nt)[i])
                        first_prods.get(nt)[i] = first_prods.get(nt)[i].replace(nt, '')

                    regras.update({estado + '`': []})
                    for prod in first_prods.get(nt):
                        regras.get(estado+'`').append(prod)
                    regras.get(estado).append(new_prods)
        self.regras.update(regras)

    def remove_indirect(self):
        pass
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=- FIRST
    def assemble_first(self): 
        self.First = {T:set() for T in self.nao_terminais}
        for NT, regra in self.regras.items():
            if not self.First[NT]:
                self.First[NT] = self.First[NT] | self.pegaFirst(regra, NT)

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