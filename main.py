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
        print(LISTA_OBJETOS[SELECIONADO], "\n")

    print("1- Seleciona um Objeto")
    print("2- Importa um Objeto")
    print("3- Deleta Objeto")
    print("4- Edita Objeto")
    print("5- Salvar Objeto")
    print("6- Testar palavra")
    print("7- Sair\n")
    
    tipo = " "
    while type(tipo) != type(1) or tipo < 1 or tipo > 7:
        tipo = input("Digite um valor entre 1 e 7: ")
        if tipo.isnumeric():
            tipo = int(tipo)
    
    if tipo != 7:
        os.system('cls')
        [SelecionaObjeto, 
            ImportaObjeto,
            DeletarObjeto,
            EditaObjeto,
            SalvaObjeto,
            TestaPalavra][tipo-1]()
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

def TestaPalavra():
    global LISTA_OBJETOS, SELECIONADO
    if SELECIONADO is None or LISTA_OBJETOS[SELECIONADO].TIPO not in ["GLC", "AF"]:
        return
    print(LISTA_OBJETOS[SELECIONADO],"\n")
    palavra = input("Digite a palavra: ")
    resultado = LISTA_OBJETOS[SELECIONADO].Testa_Palavra(palavra, True)
    if resultado:
        print(f"A palavra '{palavra}' pertence a Linguagem")
    else:
        print(f"A palavra '{palavra}' não pertence a Linguagem")
    input('\n\nAperte ENTER para continuar')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
while Menu(): # Deixa o menu em loop
    pass
