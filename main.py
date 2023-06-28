from Gramatica_Regular import GR
from Automato_finito import AF
from Gramatica_LC import GLC
from Expressao_Regular import ER
from Objetos_Salvos import Pega_Json, Salva_Json
import os

LISTA_OBJETOS = []
SELECIONADO = None


def Menu():
    os.system('cls')
    print(f"\n-=-=- {len(LISTA_OBJETOS)} Objetos carregados -=-=- Selecionado: {SELECIONADO if SELECIONADO is None else SELECIONADO+1} -=-=-\n")
    
    if SELECIONADO is not None:
        print("\n",LISTA_OBJETOS[SELECIONADO], "\n")

    print("1- Seleciona um Objeto\n2- Importa um Objeto\n3- Deleta Objeto\n4- Edita Objeto\n5- Salvar Objeto")
    print("6- Sair\n")
    
    tipo = " "
    while type(tipo) != type(1) or tipo < 1 or tipo > 6:
        tipo = input("Digite um valor entre 1 e 6: ")
        if tipo.isnumeric():
            tipo = int(tipo)
    
    if tipo != 6:
        os.system('cls')
        [SelecionaObjeto, 
            ImportaObjeto,
            DeletarObjeto,
            EditaObjeto,
            SalvaObjeto][tipo-1]()
        return True
    return False

# -=-=-=-=-=-=-=- OPÇÕES DO MENU -=-=-=-=-=-=-=-=-=-=-=        
def SelecionaObjeto():
    global LISTA_OBJETOS, SELECIONADO
    if not LISTA_OBJETOS:
        return
    for ind, i in enumerate(LISTA_OBJETOS):
        print(f"-=-=-=- {ind+1} -=-=-=-")
        print(i)
        print()

    tipo = " "
    while type(tipo) != type(1) or tipo < 1 or tipo > len(LISTA_OBJETOS):
        tipo = input("Digite o número do objeto: ")
        if tipo.isnumeric():
            tipo = int(tipo)
    
    SELECIONADO = tipo-1

def ImportaObjeto():
    global LISTA_OBJETOS, SELECIONADO
    dicio = Pega_Json()
    if dicio is None:
        return
    elif dicio["TIPO"] == "AF":
        LISTA_OBJETOS.append(AF(dicio["Estados"],
                        dicio["Alfabeto"],
                        dicio["Transicao"],
                        dicio["Qo"],
                        dicio["F"]))
    elif dicio["TIPO"] == "GR":
        LISTA_OBJETOS.append(GR(
            dicio["N"], dicio["T"], dicio["P"], dicio["S"]
        ))
    
    elif dicio["TIPO"] == "GLC":
        LISTA_OBJETOS.append(GR(
            dicio["N"], dicio["T"], dicio["P"], dicio["S"]
        ))
    else:
        LISTA_OBJETOS.append(ER(dicio["expressao"]))
    SELECIONADO = len(LISTA_OBJETOS)-1

def DeletarObjeto():
    global SELECIONADO
    if SELECIONADO is None:
        return

    LISTA_OBJETOS.pop(SELECIONADO)
    SELECIONADO = None

def EditaObjeto():
    pass

def SalvaObjeto():
    global LISTA_OBJETOS, SELECIONADO
    Salva_Json(LISTA_OBJETOS[SELECIONADO])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
while Menu(): # Deixa o menu em loop
    pass

"""
automatoAFND = AF(['p','q','r','s'],
                  ['0','1'],
                  {'p':{'0':'p', '1':'p', '&':'q'},
                   'q':{'0':'r', '1':'r'},
                   'r':{'0':'s'},
                   's':{'0':'s', '1':'s'}},
                   'p',
                   ['s'])
        
automato = AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              {'q0':{'a':'q1'},
               'q1':{'b':'q2','a':'q3'},
               'q2':{'b':'q0'}},
              'q0',
              ['q3'])


automato2 = AF(['1','2','3'],
               ['a','b'],
               {'1':{'b':'2','&':'3'},
                '2':{'a':'1','b':'2'},
                '3':{'a':'2,3','b':'3'}},
               '1',
               ['2'])


automato3 = AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              {'q0':{'a':'q1'},
               'q1':{'b':'q2','a':'q3'},
               'q2':{'b':'q3'},
               'q3':{'b':'q0', 'a':'q0'}},
              'q0',
              ['q3'])

automatoParaMinimizar = AF(['S','A','B','C','D','E','F','G', 'H'],
                            ['a', 'b'],
                            {'S':{'a':'A','b':'E'},
                            'A':{'a':'B', 'b':'F'},
                            'B':{'a':'A', 'b':'C'},
                            'C':{'a':'G', 'b':'D'},
                            'D':{'a':'C', 'b':'G'},
                            'E':{'b':'F'},
                            'F':{'a':'G'},
                            'G':{'a':'F'},
                            'H':{'b':'D'}},
                            'S',
                            ['C','D'])

"""