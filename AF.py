class AF():
    def __init__(self,Estados,Alfabeto,Transicao,Qo,F):
        self.Estados = Estados
        self.Alfabeto = Alfabeto
        self.Transicoes = Transicao #[estado,simbolo,estado]
        self.Qo = Qo
        self.F = F
        
    def fechamento_epsilon(self, estado):
        fechamento = {estado}
        
        pilha = [estado]
        while pilha:
            estado_atual = pilha.pop()
            
            for transicao in self.Transicoes:
                if transicao[0] == estado_atual and transicao[1]=='&':
                    proximo_estado = transicao[2]
                    if proximo_estado not in fechamento:
                        fechamento.add(proximo_estado)
                        pilha.append(proximo_estado)
        return fechamento
    
    def fechamento_simbolo(self, estado,simbolo): # simbolo != &
        fechamento = set()       
        for transicao in self.Transicoes:
            if transicao[0] == estado and transicao[1]==simbolo:
                proximo_estado = transicao[2]
                fechamento.add(proximo_estado)
        return fechamento
    
    def definir_novas_transicoes(self):
        novas_transicoes = []
        
        for estado in self.Estados:
            fechamento = self.fechamento_epsilon(estado)
            for simbolo in self.Alfabeto:
                novo_estado = []
                for fechado in fechamento:
                    for transicao in self.Transicoes:
                        if transicao[0] == fechado and transicao[1] == simbolo:
                            novo_estado.append(self.fechamento_epsilon(transicao[2]))
                    
                    if novo_estado:
                        nova_transicao = [fechamento, simbolo, novo_estado]
                        novas_transicoes.append(nova_transicao)
        
        for t in novas_transicoes:
            c = 0
            l = 0
            for x in novas_transicoes:
                if t == x:
                    c = c+1
                if c == 2:
                    novas_transicoes.remove(x)
                if t in x[2]:
                    l = l+1
            
        return novas_transicoes
    
    def AFND_pra_AFD(self):
        AFD_estados = []
        AFD_transicoes = []
        
        estado_inicial = self.fechamento_epsilon(self.Qo)
        transicoes_fecho = self.definir_novas_transicoes()
        
        for estado in self.Estados: 
            AFD_estados.append(self.fechamento_epsilon(estado))
        
        AFD_transicoes = self.definir_novas_transicoes()
        
        print(AFD_estados)
        #resultado = AF(AFD_estados, self.Alfabeto, AFD_transicoes, estado_inicial, [])
        return AFD_transicoes
        
                        
automata = AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              [['q0', 'a', 'q1'],
               ['q0', 'a', 'q2'],
               ['q1', '&', 'q2'],
               ['q1', 'a', 'q3'],
               ['q2', 'b', 'q0']],
              'q0',
              ['q3'])

state = 'q1'
closure = automata.fechamento_epsilon(state)
#print(automata.definir_novas_transicoes())
print(automata.fechamento_simbolo('q0','a'))
#print(closure)  # Output: {'q1', 'q2'}