from Gramatica_Regular import GR
from Automato_finito import AF
from Gramatica_LC import GLC
from Expressao_Regular import ER
from Objetos_Salvos import Pega_Json, Salva_Json, Pega_Json_Tudo
import os


LISTA_OBJETOS = []
SELECIONADO = None


def Menu():
    print(f"\n-=-=- {len(LISTA_OBJETOS)} Objetos carregados -=-=- Selecionado: {SELECIONADO if SELECIONADO is None else SELECIONADO+1} -=-=-\n")
    
    if SELECIONADO is not None:
        print(LISTA_OBJETOS[SELECIONADO], "\n")

    print("1- Importa todos os objetos")
    print("2- Seleciona um Objeto")
    print("3- Importa um Objeto")
    print("4- Deleta Objeto")
    print("5- Metodos do Objeto")
    print("6- Salvar Objeto")
    print("7- Testar palavra")
    print("8- Sair\n")
    
    tipo = " "
    while type(tipo) != type(1) or tipo < 1 or tipo > 8:
        tipo = input("Digite um valor entre 1 e 8: ")
        if tipo.isnumeric():
            tipo = int(tipo)
    
    if tipo != 8:
        os.system('cls')
        [ImportaTudo,
            SelecionaObjeto, 
            ImportaObjeto,
            DeletarObjeto,
            Acao_Objeto,
            SalvaObjeto,
            TestaPalavra][tipo-1]()
        return True
    return False

# -=-=-=-=-=-=-=- OPÇÕES DO MENU -=-=-=-=-=-=-=-=-=-=-=
def ImportaTudo():
    global LISTA_OBJETOS
    dicionarios = Pega_Json_Tudo()
    if dicionarios is None or not dicionarios:
        input("\nAperte ENTER para voltar ao MENU")
        return

    for dicio in dicionarios:
        if dicio["TIPO"] == "AF":
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
            LISTA_OBJETOS.append(GLC(
                dicio["N"], dicio["T"], dicio["P"], dicio["S"]
            ))
        else:
            LISTA_OBJETOS.append(ER(dicio["expressao"]))

def SelecionaObjeto():
    global LISTA_OBJETOS, SELECIONADO
    if not LISTA_OBJETOS:
        print("Não tem nenhum objeto que possa ser selecionado")
        input("\nAperte ENTER para voltar ao MENU")
        return
    print(5*"\n")
    for ind, i in enumerate(LISTA_OBJETOS):
        print(f"-=-=-=- {ind+1} -=-=-=-")
        print(i)
        print()
    #print("LISTA_OBJETOS: ",LISTA_OBJETOS)
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
        input("\nAperte ENTER para voltar ao MENU")
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
        LISTA_OBJETOS.append(GLC(
            dicio["N"], dicio["T"], dicio["P"], dicio["S"]
        ))
    else:
        LISTA_OBJETOS.append(ER(dicio["expressao"]))
    SELECIONADO = len(LISTA_OBJETOS)-1

def DeletarObjeto():
    global SELECIONADO
    if SELECIONADO is None:
        print("Nenhum objeto foi selecionado")
        input("\nAperte ENTER para voltar ao MENU")
        return

    LISTA_OBJETOS.pop(SELECIONADO)
    SELECIONADO = None

def Acao_Objeto():
    global SELECIONADO

    if SELECIONADO is None:
        print("Nenhum objeto foi selecionado")
        input("\nAperte ENTER para voltar ao MENU")
        return
    print(LISTA_OBJETOS[SELECIONADO])
    if LISTA_OBJETOS[SELECIONADO].TIPO == 'GLC':
        print("\n")
        LISTA_OBJETOS[SELECIONADO].MostraFirst_Follow()
        print()
        LISTA_OBJETOS[SELECIONADO].MostraTabelaLL1()

    print("\n\nO que você quer realizar?")
    fim, lista_Metodos = LISTA_OBJETOS[SELECIONADO].ApresentarOpcoes()

    tipo = " "
    while type(tipo) != type(1) or tipo < 1 or tipo > fim:
        tipo = input("Digite o número da ação: ")
        if tipo.isnumeric():
            tipo = int(tipo)

    if tipo == fim:  # Não faz nada
        return

    if LISTA_OBJETOS[SELECIONADO].TIPO == "AF" and tipo in [4, 5]:
        os.system('cls')
        print("Selcione o outro Automato")
        SelecionaObjeto()
        obj = lista_Metodos[tipo-1](LISTA_OBJETOS[SELECIONADO]) # Chama o método escolhido
    else:
        obj = lista_Metodos[tipo-1]() # Chama o método escolhido

    if not obj is None:  # Caso o método retorne um novo obj
        LISTA_OBJETOS.append(obj)
        SELECIONADO = len(LISTA_OBJETOS) - 1
    else:  # Caso o método retorn None
        input('\n\nAperte ENTER para continuar')
    
def SalvaObjeto():
    global LISTA_OBJETOS, SELECIONADO
    if SELECIONADO is None:
        print("Nenhum objeto foi selecionado")
        input("\nAperte ENTER para voltar ao MENU")
        return
    Salva_Json(LISTA_OBJETOS[SELECIONADO])

def TestaPalavra():
    global LISTA_OBJETOS, SELECIONADO
    if SELECIONADO is None or LISTA_OBJETOS[SELECIONADO].TIPO not in ["GLC", "AF"]:
        print("Nenhum objeto válido foi selecionado")
        input("\nAperte ENTER para voltar ao MENU")
        return
    print(LISTA_OBJETOS[SELECIONADO],"\n")
    if LISTA_OBJETOS[SELECIONADO].TIPO == 'GLC':
        print("\n")
        LISTA_OBJETOS[SELECIONADO].MostraFirst_Follow()
        print()
        LISTA_OBJETOS[SELECIONADO].MostraTabelaLL1()
    palavra = input("Digite a palavra: ")
    resultado = LISTA_OBJETOS[SELECIONADO].Testa_Palavra(palavra, True) # True para mostrar a pilha passo a passo
    if resultado:
        print(f"A palavra '{palavra}' pertence a Linguagem")
    else:
        print(f"A palavra '{palavra}' não pertence a Linguagem")
    input('\n\nAperte ENTER para continuar')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
while Menu(): # Deixa o menu em loop
    os.system('cls')
    
