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

    def ApresentarOpcoes(self):
        print("1- Converte para AFND") # Retorna AF
        print("2- Cancelar")

        return (2, [self.convert_to_AFND])

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
    




        
        
        






        