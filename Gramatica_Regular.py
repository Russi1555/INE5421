class GR():
    def __init__(self,N,T,P,S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = P # {Tx : {N : Ty}}
        self.inicial = S
    
    def __repr__(self):
        string = ""
        for estado in self.regras:
            if estado == self.inicial:
                substring = (f"*{estado} -> | ")
            else:
                substring = (f"{estado} -> | ")
            for producao in self.regras[estado]:                
                substring += producao
                substring += " | "
            string += substring
            string += "\n"
        
        return string


    
    def convert_to_AFND(self):
        from Automato_finito import AF
        estados = self.nao_terminais
        estados.append('NEF') #Novo Estado Final
        alfabeto = self.terminais
        Qo = self.inicial
        transicoes = {}
        estados_aceitacao = ['NEF']
        for NT in self.regras:
            transicoes[NT] = {}
            for producao in self.regras[NT]:
                print(producao)
                if producao == producao.lower(): #verifica se vai para final ex: a == a | aN1 != an1
                    transicoes[NT][producao] = 'NEF'
                else:
                    simbolo = producao[0]
                    estado = producao.replace(simbolo,'')
                    transicoes[NT][simbolo] = estado
        
        print(transicoes)
        print(estados)

        AFND_resultante = AF(estados,alfabeto,transicoes,Qo,estados_aceitacao)
        #print(AFND_resultante)
        return AFND_resultante
                
            
        
        
        
                
        #AFND_resultante = AF(estados, alfabeto, transicoes, Qo, estados_aceitacao)
        #return AFND_resultante
        