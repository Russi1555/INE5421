class GR():
    def __init__(self,N,T,P,S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = P # {Tx : ['T'], Ty: ['TN', 'T']}
        self.inicial = S
    
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



        
