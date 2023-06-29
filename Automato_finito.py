from Gramatica_Regular import GR


class AF():
    def __init__(self,Estados,Alfabeto,Transicao,Qo,F):
        self.Estados = Estados
        self.Alfabeto = Alfabeto
        self.Transicoes = Transicao #{estado:{simbolo:estado}}
        self.Qo = Qo
        self.F = F
        self.TIPO = "AF"
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

        SIMBOLOS = self.Alfabeto.copy()
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
                es = ""
                if estado not in list(self.Transicoes.keys()):
                    for est in estado.split(','):
                        if est in list(self.Transicoes.keys()) and alf in list(self.Transicoes[est].keys()):
                            es += f"{self.Transicoes[est][alf]},"
                    es = es[:-1]
                elif alf in list(self.Transicoes[estado].keys()):
                    es = self.Transicoes[estado][alf]

                if len(es.split(',')) > 1: # Caso seja ambiguo (a-> B,C)
                    es = f"{'{'+es+'}'}"
                elif es == "":
                    es = "--"
                tam = len(es)
                string += ((5-tam//2)*" ")+es+((5-tam//2)*" ")+"|"
            string = string[:-1] + "\n"+TRACO+"\n"
        return string

    def ApresentarOpcoes(self):
        print("1- Converter AFND para AFD") # Retorna AF
        print("2- Converter AFD para GR") # Retorna GR
        print("3- Minimizar AFD") # Retorna AF
        print("4- União de AFs") # Retorna AF
        print("5- Intersecção de AFs") # Retorna AF
        print("6- Cancelar")

        return (6, [self.convert_to_AFD,
                    self.convert_to_GR,
                    self.minimiza_AFD,
                    self.Uniao_AFs,
                    self.Interseccao_AFs])

    def epsilon_fechamento(self):
        fechamento = []
        SELF_Transicoes = self.Transicoes.copy()
        fila = self.Estados.copy()
        SELF_Estados = self.Estados.copy()
        SELF_Qo = self.Qo

        while fila:
            estado = fila.pop(0)
            if estado in SELF_Transicoes and '&' in SELF_Transicoes[estado]:
                prox_estados = (str(estado) + ',' + str(SELF_Transicoes[estado]['&']))
                if prox_estados not in fechamento:
                    if estado == SELF_Qo:
                        SELF_Estados.remove(SELF_Qo)
                        SELF_Qo = prox_estados

                    novos_estados = prox_estados
                    fechamento.append(novos_estados)
                    fila.extend(novos_estados)
                    #Até aqui descobre os &-fecho. Agora vamos adicionar as transições dele.

            if fechamento:
                for estados_ep in [fechamento]:
                    estado_atual = estados_ep[0]
                    if estado_atual not in SELF_Estados:
                        SELF_Estados.append(estado_atual)
                        sub_estados = estado_atual.split(',')
                        #print(sub_estados)
                        novas_transicoes = {}
                        for simbolo in self.Alfabeto:
                            estado_destino = ""
                            for estado in sub_estados: 
                                if simbolo in SELF_Transicoes[estado]:
                                    if estado_destino == '':
                                        estado_destino = estado_destino + str(SELF_Transicoes[estado][simbolo])
                                    # print(estado_destino)
                                    else:
                                        estado_destino =  estado_destino + "," + str(SELF_Transicoes[estado][simbolo])
                            
                            novas_transicoes[simbolo] = estado_destino
                        if estado_destino not in fechamento:
                                SELF_Estados.append(estado_destino)
                    
                    resultado_transicoes = SELF_Transicoes.copy()
                    resultado_transicoes[estado_atual] = novas_transicoes

                    SELF_Transicoes = resultado_transicoes
        return (SELF_Transicoes, SELF_Estados, SELF_Qo)

    def convert_to_AFD(self):
        SELF_Transicoes, SELF_Estados, SELF_Qo = self.epsilon_fechamento()
        fila = SELF_Estados.copy()
        novo_Transicoes = {}
        
        while fila:
            #print("FILA: " + str(fila))
            estado = fila.pop(0)
            #print("Estado: " + str(estado))
            if ',' in estado:
                subestados = estado.split(',')
                #print("Subestado: " + str(subestados))
                novas_transicoes = {}
                for simbolo in self.Alfabeto:
                    if simbolo != '&':
                        estado_destino = ""
                        for subestado in subestados:
                            if subestado in SELF_Transicoes.keys() and simbolo in SELF_Transicoes[subestado]:
                                #print("ESTADO ATUAL DE DESTINO: " + estado_destino)
                                if subestado not in estado_destino:
                                #   print("SUBESTADO: "+str(subestado)+" NAO ESTÁ EM "+ str(estado_destino))
                                    if estado_destino == '':
                                        estado_destino = estado_destino + str(SELF_Transicoes[subestado][simbolo])
                                    else:
                                        for subsubestado in SELF_Transicoes[subestado][simbolo].split(','):
                                            if subsubestado not in estado_destino:
                                                estado_destino =  estado_destino + "," + subsubestado
                           # print("ESTADO ATUAL DE DESTINO 2: " + estado_destino)
                    
                        novas_transicoes[simbolo] = estado_destino
                    
                    if estado_destino not in SELF_Estados and estado_destino != "":
                        #print("Estado destino: " + str(estado_destino))
                        #print(estado_destino)
                        estado_destino = str(estado_destino)
                        SELF_Estados.append(estado_destino)
                        #print(self.Estados)
                        
                        fila.append(estado_destino)
                        #print("FILA: " + str(fila))

                novo_Transicoes[estado] = novas_transicoes
                #print(self.Transicoes)

        #self.Transicoes = novo_Transicoes
        for estado in SELF_Estados:
            if estado not in novo_Transicoes:
                SELF_Estados.remove(estado)

        fila = [SELF_Qo]
        novos_estados = [SELF_Qo]


        while fila:
            estado_atual = fila.pop()
            #print(estado_atual)
            if estado_atual in novo_Transicoes:
                transicao = novo_Transicoes[estado_atual]
                for simbolo in self.Alfabeto:
                    if simbolo in transicao:
                        if transicao[simbolo] not in novos_estados:
                            novos_estados.append(transicao[simbolo])
                            fila.append(transicao[simbolo])
        
        #self.Estados = novos_estados
        
        for estado in novos_estados:
            if estado not in novo_Transicoes:
                novos_estados.remove(estado)

        novos_finais = []
        for estado_final in self.F:
            for estado in SELF_Estados:
                if estado_final in estado:
                    novos_finais.append(estado)

        #self.F = novos_finais
        return AF(novos_estados, self.Alfabeto, novo_Transicoes, SELF_Qo, novos_finais)
        #print(self.Estados)
        #print(self.F)
        #print(self.Transicoes)
  
    def convert_to_GR(self):  #TEM QUE ESTAR DETERMINIZADO
        nao_terminais = []#self.Estados
        terminais = self.Alfabeto
        P = {}
        dict_T = {}
        count=0
        for estado in self.Transicoes:
            novo_nome = str(chr(65+count)) # A,B,C...Z (65-91)
            nao_terminais.append(novo_nome)
            dict_T[estado] = novo_nome
            count+=1

        S = dict_T[self.Qo]

        for estado in self.Transicoes:
            id = dict_T[estado]
            P[id] = []
            for T in self.Transicoes[estado]:
                NT = self.Transicoes[estado][T]
                if NT in self.F:
                    P[id].append(T)
                if NT not in self.Transicoes:
                    pass
                else:
                    NT = dict_T[NT]
                    producao = str(T.lower() + NT.upper())
                    P[id].append(producao)        

        return GR(nao_terminais,terminais,P,S)
                
    def minimiza_AFD(self): # Minimiza Automato finito
        # Retorna o AF de antes da minimização
        novoAF = AF(self.Estados.copy(), self.Alfabeto.copy(), self.Transicoes.copy(), self.Qo, self.F.copy())

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

        return novoAF
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Testa_Palavra(self, palavra, _):
        return self.TesteSimbolo(0, self.Qo, palavra)
    
    def TesteSimbolo(self, index, est, palavra):
        if est in self.F and index >= len(palavra):
            return True

        elif est in list(self.Transicoes.keys()):
            if '&' in list(self.Transicoes[est].keys()) or (palavra and index < len(palavra) and palavra[index] in list(self.Transicoes[est].keys())):
                for g,h in self.Transicoes[est].items():
                    if g == '&' or (palavra and index < len(palavra) and palavra[index] == g):
                        for i in self.Transicoes[est][g].split(','):
                            if self.TesteSimbolo(index+1 if h != '&' else index, i, palavra):
                                return True
        elif any(ele in list(self.Transicoes.keys()) for ele in est.split(',')):
            for es in est.split(','):
                if es in self.Transicoes.keys() and ('&' in list(self.Transicoes[es].keys()) or (palavra and index < len(palavra) and palavra[index] in list(self.Transicoes[es].keys()))):
                    if self.TesteSimbolo(index, es, palavra):
                        return True
        return False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=     
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
            if l:
                break
            # -=-=-=-=-=-=-=-=-=-=-=- Remove estados Mortos -=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            transicoes = self.Transicoes
            acesso = set(self.F)
            for i in self.F:
                VoltaEstados(i) # Mortos

    def Uniao_AFs(self, OutroAF):
        A_Transicao, A_Estados, A_Qo, A_F, h = MudaEstados(self.Transicoes, self.Estados, self.Alfabeto, self.Qo, self.F)

        B_Transicao, B_Estados, B_Qo, B_F = MudaEstados(OutroAF.Transicoes, OutroAF.Estados, OutroAF.Alfabeto, OutroAF.Qo, OutroAF.F, h)[:4]

        Novo_alfabeto = list(set(self.Alfabeto) | set(OutroAF.Alfabeto))

        A_Transicao.update(B_Transicao)

        Novo_Qo = 'S'

        A_Estados.insert(0,Novo_Qo)

        A_Transicao[Novo_Qo] = {'&':f"{A_Qo},{B_Qo}"}

        Final = A_F+B_F

        return AF(A_Estados+B_Estados, Novo_alfabeto, A_Transicao, Novo_Qo, Final).convert_to_AFD()

        """Novo_Final = []
        for est in NovoAF.Estados:
            if any(Qi in Final for Qi in est.split(',')):
                Novo_Final.append(est)

        return AF(NovoAF.Estados, NovoAF.Alfabeto, NovoAF.Transicoes, NovoAF.Qo, Novo_Final)"""

    def Interseccao_AFs(self, OutroAF):
        A_Transicao, A_Estados, A_Qo, A_F, h = MudaEstados(self.Transicoes, self.Estados, self.Alfabeto, self.Qo, self.F)

        B_Transicao, B_Estados, B_Qo, B_F = MudaEstados(OutroAF.Transicoes, OutroAF.Estados, OutroAF.Alfabeto, OutroAF.Qo, OutroAF.F, h)[:4]

        Novo_alfabeto = list(set(self.Alfabeto) | set(OutroAF.Alfabeto))

        A_Transicao.update(B_Transicao)

        Novo_Qo = 'S'

        A_Estados.insert(0,Novo_Qo)

        A_Transicao[Novo_Qo] = {'&':f"{A_Qo},{B_Qo}"}

        Final = A_F+B_F

        NOVO_AF = AF(A_Estados+B_Estados, Novo_alfabeto, A_Transicao, Novo_Qo, Final).convert_to_AFD()

        Novo_Final = []
        for est in NOVO_AF.Estados:
            if any(Qi in A_F for Qi in est.split(',')) and any(Qi in B_F for Qi in est.split(',')):
                Novo_Final.append(est)

        return AF(NOVO_AF.Estados, NOVO_AF.Alfabeto, NOVO_AF.Transicoes, NOVO_AF.Qo, Novo_Final)

def MudaEstados(transicao, estados, alfabeto, Qo, F, h=0):
    # -=-=-=-=-=-= Novos Estados -=-=-=-=-=--=
    tabela = dict()
    NovoEstados = []
    for est in estados:
        estad = ""
        for i in est.split(','):
            if i not in tabela.keys():
                tabela[i] = f"q{h}"
                h += 1
            estad += f"{tabela[i]},"
        NovoEstados.append(estad[:-1])
    # -=-=-=-=-=- Estado Inicial -=-=-=-=-=-=-
    NovoQo = ""
    for i in Qo.split(','):
        NovoQo += f"{tabela[i]},"
    NovoQo = NovoQo[:-1]
    # -=-=-=-=-= Estados Finais -=-=-=-=-=-=-
    NovoF = []
    for est in F:
        final = ""
        for i in est.split(','):
            final += f"{tabela[i]},"
        NovoF.append(final[:-1])
    # -=-=-=-=- Novas Transições -=-=-=-=-=-=-
    novoTransicao = dict()
    for k,v in transicao.items():
        novoV = dict()
        for kv, nv in v.items():
            v2 = ""
            for i in nv.split(','):
                v2 += f"{tabela[i]},"
            novoV[kv] = v2[:-1]
        novoTransicao[tabela[k]] = novoV

    return (novoTransicao, NovoEstados, NovoQo, NovoF, h)

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