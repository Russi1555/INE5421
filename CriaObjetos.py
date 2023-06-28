from Objetos_Salvos import Salva_Json
from Gramatica_Regular import GR
from Automato_finito import AF
from Gramatica_LC import GLC
from Expressao_Regular import ER



def Cria_AF():
    Salva_Json(AF([],  # ESTADOS
                  [],  # ALFABETO
                  {},  # TRANSIÇÕES
                  "",  # Qo
                  [])) # Estados Finais
    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-

     AF(['1','2','3'],              # ESTADOS
        ['a','b'],                  # ALFABETO
        {'1':{'b':'2','&':'3'},     # TRANSIÇÕES \ 
        '2':{'a':'1','b':'2'},      # TRANSIÇÕES  > '2,3' significa que desvia para os dois estados 
        '3':{'a':'2,3','b':'3'}},   # TRANSIÇÕES /
        '1',                        # ESTADO INICIAL (Qo)
        ['2'])                      # ESTADOS FINAIS 
    """

def Cria_GR():
    Salva_Json(GR([], # Não Terminais
                  [], # Terminais
                  {}, # Regras
                  "")) # Inicial

    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-
    GR(['S','A','B','C'],       # Não Terminais
        ['a','b','c'],          # Terminais
        {'S': ["ABB","CAC"],    # REGRAS \ 
        'A':['a'],              # REGRAS  \ CADA Elemento da lista é uma produção
        'B':['Bc','ABB'],       # REGRAS  / 
        'C':["bB",'a']},        # REGRAS /
        'S')                    # Não Terminal Inicial

    """

def Cria_GLC():
    Salva_Json(GLC([], # Não Terminais
                  [], # Terminais
                  {}, # Regras
                  "")) # Inicial
    
    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-
    
    GLC(['E','T','F'],                          # Não Terminais
        ['+', '-', '*', '/', '(', ')', 'i'],    # Terminais
        {'E': ["E+T", "E-T", "T"],              # REGRAS \ 
         'T': ["T*F", "T/F", "F"],              # REGRAS  > CADA Elemento da lista é uma produção
         'F': ["(E)", "i"]},                    # REGRAS / 
         'E')                                   # Não Terminal Inicial
    
    """

def Cria_ER():
    Salva_Json(ER("")) # Expressão
    
    """
    -=-=-=-=-=- EXEMPLO -=-=-=-=-=-=-
    ER("abba(b|&)*aa") #  Expressao
    
    """


# TROQUE PARA SALVAR UM OBJETO

#Cria_AF()
#Cria_GR()
#Cria_GLC()
#Cria_ER()