import json
import os

PATH = os.getcwd()+"/Objetos"


def Salva_AF(AF):
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"AF",
            "Estados":AF.Estados,
            "Alfabeto":AF.Alfabeto,
            "Transicao":AF.Transicoes,
            "Qo":AF.Qo,
            "F":AF.F
        }))

def Salva_GR(GR):
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"GR",
            "N":GR.nao_terminais,
            "T":GR.terminais,
            "P":GR.regras,
            "S":GR.inicial
        }))

def Salva_GLC(GLC):
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"GCL",
            "N":GR.nao_terminais,
            "T":GR.terminais,
            "P":GR.regras,
            "S":GR.inicial
        }))

def Salva_ER(path, ER):
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"ER",
            "expressao":ER.expressao}))

def Salva_Json(Obj):
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    nome = Obj.TIPO
    i = 1
    while os.path.exists(PATH+f"{nome}.json"):
        nome = nome[0:2]+f"({i})"
        i += 1

    if input(f"Nome do arquivo é '{nome}, deseja alterar? (s/n): '") == 's':
        nome_ = input('Digite o nome (não digite nada para cancelar)')
        if nome_ != '':
            nome = nome_

    path_ = PATH+f"{nome}.json"
    if path_ == '':
        return
    {"AF":Salva_AF, "GR":Salva_GR, "GLC":Salva_GLC, "ER":Salva_ER}[Obj.TIPO](path_, Obj)
    
def Pega_Json():
    path = RecebePath()
    if path == None: 
        return None
    with open(path, 'r') as arquivo:
        return json.loads(arquivo.readline())
    
def RecebePath():
    global PATH
    if not os.path.exists(PATH): # Pasta Objetos não existe
        os.mkdir(PATH)
        return None

    opcoes = []
    for arquivos in os.walk(PATH):
        for ind, arq in enumerate(arquivos[2]):
            print(f"{ind+1}- {arq}")
            opcoes.append(arq)
    
    if not opcoes: # Nenhum objeto na pasta
        return None

    val = " "
    while type(val) != type(1) or val < 1 or val > len(opcoes):
        val = input("Digite o valor do objeto: ")
        if val.isnumeric():
            val = int(val)

    return PATH+"/"+opcoes[val-1]



