from Automato_finito import AF

class Node:
    def __init__(self, valor, first=None, last=None, esq=None, dir=None):
        self.valor = valor
        if valor == '&':
            self.first = set([])
            self.last = set([])
            self.vazio = True
        else:
            self.first = first
            self.last = last
            self.vazio = False
        self.esq = esq
        self.dir = dir

class ER:
    def __init__(self, expressao):
        self.expressao = expressao
        self.alfabeto = set(filter(lambda x: x not in ['.', '(', ')', '|', '*', '&'], self.expressao))
        self.TIPO = "ER"
    
    def __repr__(self):
        return self.expressao

    def ER_para_AFD(self):
        global simbolos, h, p
        h = 0
        simbolos = {i:[] for i in self.alfabeto} # Salva os números de cada simbolo
        for i in self.alfabeto:
            h += self.expressao.count(i)
        p = len(self.expressao)-1 # i passa pela expressão
        raiz = Node('.', dir=Node('#', first=set([h+1]), last=set([h+1])))
        raiz.esq = self.SubArvore()
        # -=-=-=-=-=-=-=-=-=-=-=- Pega o automato da Árvore -=-=-=-=-=-=-=-=-=-=-=-=-=-
        ValorDoFinal = list(raiz.dir.last)[0]
        global follows
        follows = {i:set() for i in range(1, ValorDoFinal+1)}
        ini = self.PegaFollow(raiz)[0]
        #print(f"Inicial: {ini}, Final:{fim}, Vazio:{vazio}")
        #print(follows)
        # Pega o estado inicial -=-=-=-=-=--=-=
        Qo = ""
        for i in ini:
            Qo += str(i)
        Estados = [Qo]

        # Pega as transições e estados finais -=-=-=-=-=-
        if ValorDoFinal in follows[1]:
            Final = [Qo]
        else:
            Final = []
        Transicoes = {Qo:{}}
        PilhaEstados = [Qo]
        #print(simbolos)
        while PilhaEstados:
            estadoAtual = PilhaEstados.pop(0)
            for simb in self.alfabeto:
                est = set()
                for val in simbolos[simb]:
                    if str(val) in estadoAtual: # Verifica se tem um caminho para esse símbolo
                        est = est | follows[val]
                if est:
                    Qi = ""
                    for i in est:
                        Qi += str(i)
                    if ValorDoFinal in est and Qi not in Final: # Caso seja um estado final
                        Final.append(Qi)
                    if estadoAtual in Transicoes.keys():
                        Transicoes[estadoAtual][simb] = Qi
                    else:
                        Transicoes[estadoAtual] = {simb:Qi}
                    if Qi not in Estados:
                        PilhaEstados.append(Qi)
                        Estados.append(Qi)
        return AF(Estados, self.alfabeto, Transicoes, Qo, Final)

    def SubArvore(self):
        global simbolos, p
        nodo = self.Folha()
        if p < 0 or nodo is None:
            return nodo
        if self.expressao[p] == '.':
            p -= 1
        str1 = self.expressao[p]

        if str1 == '|':
            p -= 1
            nodos = Node('|', dir=nodo, esq=self.Folha())
            if p >= 0 and self.expressao[p] == '(':
                return nodos
            return Node('.', dir=nodos, esq=self.SubArvore())

        elif str1 in self.alfabeto+['&','*',')']:
            node2 = self.SubArvore()
            if node2 is None:
                return nodo
            return Node('.', dir=nodo, esq=node2)

        elif str1 == '(':
            return nodo
        return None

    def Folha(self):
        global simbolos, h, p
        if self.expressao[p] == '.':
            p -= 1
        str1 = self.expressao[p]
        p -= 1
        if str1 == '*':
            return Node('*', esq=self.Folha())
        
        elif str1 in self.alfabeto:
            simbolos[str1].append(h)
            h -= 1
            return Node(str1, first=set([h+1]), last=set([h+1]))
        
        elif str1 == '&':
            return Node('&')
        
        elif str1 == ')':
            node = self.SubArvore()
            node2 = self.SubArvore()
            if node2 is None:
                return node
            return Node('.', dir=node, esq=node2)
        
        return None
        
    def PegaFollow(self, raiz): # Depois que a Árvore foi criada
        global follows
        if raiz.first is None or raiz.last is None:
            if raiz.esq is not None:
                raiz.esq.first, raiz.esq.last, raiz.esq.vazio = self.PegaFollow(raiz.esq)

            if raiz.dir is not None:
                raiz.dir.first, raiz.dir.last, raiz.dir.vazio = self.PegaFollow(raiz.dir)

        if raiz.valor in self.alfabeto+['&','#']:
            return (raiz.first, raiz.last, raiz.vazio)

        elif raiz.valor == '.':
            for i in raiz.esq.last:
                follows[i] = follows[i] | raiz.dir.first
            ini = raiz.esq.first if not raiz.esq.vazio else raiz.esq.first | raiz.dir.first
            fim = raiz.dir.last if not raiz.dir.vazio else raiz.esq.last | raiz.dir.last
            return (ini, fim, raiz.dir.vazio and raiz.esq.vazio)

        elif raiz.valor == '*':
            for i in raiz.esq.last:
                follows[i] = follows[i] | raiz.esq.first
            return (raiz.esq.first, raiz.esq.last, True)

        elif raiz.valor == '|':
            return (raiz.dir.first | raiz.esq.first, raiz.dir.last | raiz.esq.last, raiz.dir.vazio or raiz.esq.vazio)