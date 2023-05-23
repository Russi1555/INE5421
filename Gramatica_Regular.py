class GR():
    def __init__(self,N,T,R,S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = R #[nao terminal, terminal, nao_terminal]  nt -> tnt
        self.inicial = S
    
    def __repr__(self):
        string =""
        for regra in self.regras:
            if len(regra) == 3:
                string +=(f" {regra[0]} -> {regra[1]}{regra[2]}\n")
            else:
                string +=(f" {regra[0]} -> {regra[1]}\n")
        return string
    
    def convert_to_AFND(self):
        from Automato_finito import AF
        estados = self.nao_terminais
        estados.append('NEF') #Novo Estado Final
        alfabeto = self.terminais
        Qo = self.inicial
        transicoes = []
        estados_aceitacao = ['NEF']
        for regra in self.regras:
            if len(regra) == 2:
                transicao = [regra[0],regra[1],'NEF']
            else:
                transicao = [regra[0],regra[1],regra[2]]
            transicoes.append(transicao)
        
        AFND_resultante = AF(estados,alfabeto,transicoes,Qo,estados_aceitacao)
        #print(AFND_resultante)
        return AFND_resultante
                
            
        
        
        
                
        #AFND_resultante = AF(estados, alfabeto, transicoes, Qo, estados_aceitacao)
        #return AFND_resultante
        