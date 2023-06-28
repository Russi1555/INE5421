class GR():
    def __init__(self,N,T,P,S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = P # {Tx : ['T'], Ty: ['TN', 'T']}
        self.inicial = S
        self.TIPO = "GR"
    
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

    def convert_to_AFND(self):
        from Automato_finito import AF
        estados = set()
        alfabeto = self.terminais
        tabela = {N:f"q{i}" for i,N in enumerate(self.nao_terminais)}
        Qo = tabela[self.inicial]
        NovoFinal = set()
        transicoes = {}
        for NT in self.regras:
            transicoes[tabela[NT]] = {}
            for producao in self.regras[NT]:
                if producao == producao.lower(): #verifica se vai para final ex: a == a | aN1 != an1
                    for v in self.regras[NT]:
                        if v != producao and v[0] == producao: # caso já tenha um estado para esse terminal
                            NovoFinal.add(tabela[v[1:]])
                            estados.add(tabela[v[1:]])
                            transicoes[tabela[NT]][producao] = tabela[v[1:]]
                            break
                    else:
                        estados.add('NEF')
                        NovoFinal.add('NEF')
                        transicoes[tabela[NT]][producao] = 'NEF'
                else:
                    simbolo = producao[0]
                    estados.add(tabela[producao[1:]])
                    transicoes[tabela[NT]][simbolo] = tabela[producao[1:]]
        return AF(sorted(list(estados)),alfabeto,transicoes,Qo,sorted(list(NovoFinal)))
    
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

    def check_recursao_direta(self):
        recursao_direta = set()
        
        for nt in self.regras: #Passo 1: Identificar as producoes com recursividade direta
            producoes = self.regras[nt]
            for producao in producoes:
                if producao[0] == nt:
                    recursao_direta.add(nt)
                    break

        return recursao_direta
    
    def remover_recursao_direta(self):

        recursao_direta = self.check_recursao_direta()
        while recursao_direta != set():
            #Passo 2: Para cada nt com recursividade direta
            for nt in recursao_direta:
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

            recursao_direta = set()
            #Checar se foi tudo resolvido, vai retornar o conjunto para ser tratado recursivamente por fora
            for nt in self.regras:
                producoes = self.regras[nt]

                for producao in producoes:

                    if producao[0] == nt:
                        recursao_direta.add(nt)
                        break

            return recursao_direta 
        
        #Talvez precise voltar pra fazer o Passo 3 / 5

    def remove_recursividades(self):
        ciclo_no_inicial = False
        #Verifica há um ciclo na produção do NT inicial
        for producao in self.regras[self.inicial]:
            if self.inicial in producao:
                ciclo_no_inicial = True
                break
        
        #Se há, é necessário fazer uma remoção da recursividade direta ou
        #sofrer com um loop infinito
        if ciclo_no_inicial:
            if self.check_recursao_direta() != set():
                self.remover_recursao_direta()
        
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
        if self.check_recursao_direta() != set():
            self.remover_recursao_direta()





        
        
        






        