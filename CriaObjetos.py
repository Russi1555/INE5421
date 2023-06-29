from Objetos_Salvos import Salva_Json
from Gramatica_Regular import GR
from Automato_finito import AF
from Gramatica_LC import GLC
from Expressao_Regular import ER


def Cria_AF():
    Salva_Json(AF(['q0', 'q1', 'q2', 'q3'],     # ESTADOS
                  ['a', 'b'],                   # ALFABETO
                  {'q0':{'a':'q1,q2'},          # Transições
                   'q1':{'b':'q2','a':'q3'},    # Transições
                   'q2':{'b':'q0'}},            # Transições
                   'q0',                        # Estado inicial (So)
                   ['q3']),                     # Estados Finais
                   "AFND")  # Nome do Arquivo

    Salva_Json(AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              {'q0':{'a':'q1'},
               'q1':{'b':'q2','a':'q3'},
               'q2':{'b':'q0'}},
              'q0',
              ['q3']), "AFD")

    Salva_Json(AF(['A','B','C','D','E','F','G', 'H'],
                    ['0', '1'],
                    {
                    'A':{'0':'G', '1':'B'},
                    'B':{'0':'F', '1':'E'},
                    'C':{'0':'C', '1':'G'},
                    'D':{'0':'A', '1':'H'},
                    'E':{'0':'E', '1':'A'},
                    'F':{'0':'B', '1':'C'},
                    'G':{'0':'G', '1':'F'},
                    'H':{'0':'H', '1':'D'}},
                    'A',
                    ['A','G','D']), "Minimizar_AF")
    
    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-

    Salva_Json(AF(['1','2','3'],    # ESTADOS
        ['a','b'],                  # ALFABETO
        {'1':{'b':'2','&':'3'},     # TRANSIÇÕES \ 
        '2':{'a':'1','b':'2'},      # TRANSIÇÕES  > '2,3' significa que desvia para os dois estados 
        '3':{'a':'2,3','b':'3'}},   # TRANSIÇÕES /
        '1',                        # ESTADO INICIAL (Qo)
        ['2'])()                    # ESTADOS FINAIS 

    Salva_Json(AF(['1','2','3'],
                ['a','b'],
                {'1':{'b':'2','&':'3'},
                    '2':{'a':'1','b':'2'},
                    '3':{'a':'2,3','b':'3'}},
                '1',
                ['2']))


    Salva_Json(AF(['q0', 'q1', 'q2', 'q3'],
                ['a', 'b'],
                {'q0':{'a':'q1'},
                'q1':{'b':'q2','a':'q3'},
                'q2':{'b':'q3'},
                'q3':{'b':'q0', 'a':'q0'}},
                'q0',
                ['q3']))

    """

def Cria_GR():
    Salva_Json(GR(['A','B','C'],    # Não Terminais
                  ['a','b'],                                # Terminais
                  {'A': ["aB"],                        # REGRAS  
                    'B':['bC', 'a'],                       # REGRAS  > CADA Elemento da lista é uma produção
                    'C':['bA']                    # REGRAS  
                    },                      # Regras
                    "A"),                                   # Inicial
                    "GR")     # Nome do Arquivo

    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-
    GR([],          # Não Terminais
        [],        # Terminais
        {},        # REGRAS 
        '')        # Não Terminal Inicial

    """

def Cria_GLC(): 
    # Questão 1 da prova 3 (moodle) "cvfopbepbe" -> palavra da prova
    Salva_Json(GLC(['P','K','V','F','C'],           # Não Terminais
                  ['c','v','f','p','b','e','o'],    # Terminais
                  {'P':['KVC'],                     # Regras
                  'K':['cK', '&'],                  # Regras
                  'V':['vV', 'F'],                  # Regras
                  'F':['fPpF', '&'],                # Regras
                  'C':['bVCe', 'opC', '&']},        # Regras
                  "P"),                             # Inicial
                "Questao_Prova")   # Nome do Arquivo
    
    Salva_Json(GLC(['S','A','B'],
                    ['a','b','c','d'],
                    {'S': ["Sb","Bc", "Ab"],
                        'A':['Sc', "ab"],
                        'B':['Scd','Bba', 'b']},       
                        "S"),                   
                        "RecursaoEsquerda")

    Salva_Json(GLC(['S','A','B','C','D'],
                    ['a','b','c','d','e'],
                    {'S': ["AD","BC"],
                    'A':["aC",'cC'],
                    'B':["aB", "cD"],
                    'C':['dC', 'dA'],
                    'D':['eD', 'AB']},
                    'S'),
                "Fatoracao")

    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-
    
    Salva_Json(GLC(['S','A','B','C'],        # Não Terminais
                  ['a','b','c'],            # Terminais
                  {'S': ["ABB","CAC"],      # REGRAS \ 
                    'A':['a'],              # REGRAS  \ CADA Elemento da lista é uma produção
                    'B':['Bc','ABB'],       # REGRAS  / 
                    'C':["bB",'a']},        # Regras
                    "S"),                     # Não Terminal Inicial
                    "Fatoracao")              # Nome do arquivo
    
    """

def Cria_ER():
    Salva_Json(ER("(a|b)*abb"), # Expressão
                "ER") # Nome do Arquivo
    
    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-
    ER("abba(b|&)*aa") #  Expressao
    
    """


# TROQUE PARA SALVAR UM OBJETO

Cria_AF()
Cria_GR()
Cria_GLC()
Cria_ER()
