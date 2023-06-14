from Gramatica_Regular import GR


class AF():
    def __init__(self,Estados,Alfabeto,Transicao,Qo,F):
        self.Estados = Estados
        self.Alfabeto = Alfabeto
        self.Transicoes = Transicao #{estado:{simbolo:estado}}
        self.Qo = Qo
        self.F = F
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

    def epsilon_fechamento(self):
        fechamento = []
        SELF_Transicoes = self.Transicoes.copy()
        fila = self.Estados.copy()
        SELF_Estados = self.Estados.copy()
        SELF_Qo = self.Qo

        while fila:
            estado = fila.pop(0)
        #    print("Estado atual: " + str(estado))
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
            

         #   print(fechamento)
           # print(novo_inicial)
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
                            if simbolo in SELF_Transicoes[subestado]:
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
  
    def convert_to_GR(self):  #TODO: ajeitar variaveis e comentar
        nao_terminais = [f'N{i}' for i in range(len(self.Estados))]
        #print(nao_terminais)
        simbolo_inicial = nao_terminais[self.Estados.index(self.Qo)]
        #print(simbolo_inicial)

        estados_finais = []
        for estado_aceitacao in self.F:
            #regras.append([nao_terminais[self.Estados.index(estado_aceitacao)], '$'])
            estados_finais.append(estado_aceitacao)
        
        regras = []
        for transicao in sorted(self.Transicoes):
            inicio = nao_terminais[self.Estados.index(transicao[0])]
            terminal = transicao[1]
            if transicao[2] != []:
                fim = nao_terminais[self.Estados.index(sorted(transicao[2]))]

            if transicao[2] in estados_finais:
                regras.append([inicio, terminal])              
            if fim:
               # print(f"{inicio} -> {terminal}")
                regras.append([inicio, terminal, fim])
        
        
       # print(regras)
        GR_resultante = GR(nao_terminais, self.Alfabeto, regras, simbolo_inicial)
        return GR_resultante

    def minimiza_AFD(self): # Minimiza Automato finito
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
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def TestaPalavra(self, palavra):
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
        Qo = "S"
        while Qo in self.Estados or Qo in OutroAF.Estados:
            Qo += "'"
        # Salva o equivalente dos estados -=-=-=-=-=-=-=-=-=-=-=-=-
        TabelaEstados = {i:f"q{h}" for h,i in enumerate(self.Estados)}
        TabelaEstados2 = {i:f"q{h}" for h,i in zip(range(len(self.Estados), len(self.Estados)+len(OutroAF.Estados)),OutroAF.Estados)}
        # -=-=-=-=-=-=-=- Traduz as Transições -=-=-=-=-=-=-=-=-=
        novaTransicao = {Qo:{'&':f"{TabelaEstados[self.Qo]},{TabelaEstados2[OutroAF.Qo]}"}}

        for k,v in self.Transicoes.items():
            for k2,v2 in v.items():
                est = v2.split(',')
                nova = {k2:TabelaEstados[est[0]]}
                if len(est) > 1:
                    for i in est[1:]:
                        nova[k2] += f",{TabelaEstados[i]}"
                novaTransicao[TabelaEstados[k]] = nova
            
        for k,v in OutroAF.Transicoes.items():
            for k2,v2 in v.items():
                est = v2.split(',')
                nova = {k2:TabelaEstados2[est[0]]}
                if len(est) > 1:
                    for i in est[1:]:
                        nova[k2] += f",{TabelaEstados2[i]}"
                novaTransicao[TabelaEstados2[k]] = nova
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        return AF([Qo]+[f"E{i}" for i in range(len(self.Estados+OutroAF.Estados))], 
                    list(set(self.Alfabeto+OutroAF.Alfabeto)), novaTransicao, Qo,
                     list(map(lambda x: TabelaEstados[x],self.F))+list(map(lambda x: TabelaEstados2[x],OutroAF.F)))

    def Interseccao_AFs(self, OutroAF): # Não testado, falta alterar
        A_Transicao, A_Estados, A_Qo, A_F, h = MudaEstados(self.Transicoes, self.Estados, self.Alfabeto, self.Qo, self.F)

        B_Transicao, B_Estados, B_Qo, B_F = MudaEstados(OutroAF.Transicoes, OutroAF.Estados, OutroAF.Alfabeto, OutroAF.Qo, OutroAF.F, h)[:4]

        Novo_alfabeto = list(set(self.Alfabeto) | set(OutroAF.Alfabeto))

        A_Transicao.update(B_Transicao)

        Novo_Qo = f"{A_Qo},{B_Qo}"
        novo_Estados = [Novo_Qo]
        tempEstados = [Novo_Qo]
        NovoF = []
        if any(ele in A_F for ele in Novo_Qo.split(',')) and any(ele in B_F for ele in Novo_Qo.split(',')):
            NovoF.append(Novo_Qo)
        
        while tempEstados:
            est = tempEstados.pop(0)
            for alf in Novo_alfabeto:
                novEst = ""
                for i in est.split(','):
                    if i in A_Transicao.keys() and alf in A_Transicao[i].keys():
                        novEst += f"{A_Transicao[i][alf]},"
                if novEst[:-1] != "" and novEst[:-1] not in novo_Estados:
                    tempEstados.append(novEst[:-1])
                    novo_Estados.append(novEst[:-1])
                    if any(ele in A_F for ele in novEst[:-1].split(',')) and any(ele in B_F for ele in novEst[:-1].split(',')):
                        NovoF.append(novEst[:-1])

        return AF(novo_Estados, Novo_alfabeto, A_Transicao, Novo_Qo, NovoF)

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