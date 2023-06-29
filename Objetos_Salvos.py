import json
import os

PATH = os.getcwd()+"/Objetos"


def Salva_AF(path, AF):
    with open(path, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"AF",
            "Estados":AF.Estados,
            "Alfabeto":AF.Alfabeto,
            "Transicao":AF.Transicoes,
            "Qo":AF.Qo,
            "F":AF.F
        }))

def Salva_G(path, G):
    with open(path, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":G.TIPO,
            "N":G.nao_terminais,
            "T":G.terminais,
            "P":G.regras,
            "S":G.inicial
        }))

def Salva_ER(path, ER):
    with open(path, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"ER",
            "expressao":ER.expressao}))

def Salva_Json(Obj):
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    nome = Obj.TIPO
    tam = len(nome)
    i = 1
    while os.path.exists(PATH+f"/{nome}.json"):
        nome = nome[0:tam]+f"({i})"
        i += 1

    print(f"Nome do arquivo é '{nome}'")
    nome_ = input('Digite o novo nome (não digite nada para usar o padrão): ')
    if nome_ != '':
        nome = nome_

    path_ = PATH+f"/{nome}.json"
    if path_ == '':
        return
    {"AF":Salva_AF, "GR":Salva_G, "GLC":Salva_G, "ER":Salva_ER}[Obj.TIPO](path_, Obj)
    
def Pega_Json():
    path = RecebePath()
    if path == None: 
        return None
    with open(path, 'r') as arquivo:
        return json.loads(arquivo.readline())
    
def RecebePath():
    global PATH
    if not os.path.exists(PATH): # Pasta Objetos não existe
        print("Pasta dos objetos não existe, criando...")
        os.mkdir(PATH)
        return None

    opcoes = []
    for arquivos in os.walk(PATH):
        for ind, arq in enumerate(arquivos[2]):
            print(f"{ind+1}- {arq}")
            opcoes.append(arq)
    
    if not opcoes: # Nenhum objeto na pasta
        print("Não tem nenhum objeto que possa ser importado")
        return None

    val = " "
    while type(val) != type(1) or val < 1 or val > len(opcoes):
        val = input("Digite o valor do objeto: ")
        if val.isnumeric():
            val = int(val)

    return PATH+"/"+opcoes[val-1]

def Pega_Json_Tudo():
    global PATH
    if not os.path.exists(PATH): # Pasta Objetos não existe
        print("Pasta dos objetos não existe, criando...")
        os.mkdir(PATH)
        return None

    opcoes = []
    for arquivos in os.walk(PATH):
        for ind, arq in enumerate(arquivos[2]):
            print(f"{ind+1}- {arq}")
            opcoes.append(arq)
    
    if not opcoes: # Nenhum objeto na pasta
        print("Não tem nenhum objeto que possa ser importado")
        return None
    dicionarios = []
    for path in opcoes:
        with open(PATH+"/"+path, 'r') as arquivo:
            dicionarios.append(json.loads(arquivo.readline()))

    return dicionarios


