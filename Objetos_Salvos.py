import json
from tkinter import filedialog
import os

PATH = os.getcwd()+"/Objetos"


def Salva_AF(AF):
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    nome = "AF"
    i = 1
    while os.path.exists(PATH+f"{nome}.json"):
        nome = nome[0:2]+f"({i})"
        i += 1
    path_ = filedialog.asksaveasfilename(initialdir=PATH, defaultextension='.json', initialfile=f"{nome}.json")
    if path_ == '':
        return
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
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    nome = "GR"
    i = 1
    while os.path.exists(PATH+f"{nome}.json"):
        nome = nome[0:2]+f"({i})"
        i += 1
    path_ = filedialog.asksaveasfilename(initialdir=PATH, defaultextension='.json', initialfile=f"{nome}.json")
    if path_ == '':
        return
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"GR",
            "N":GR.nao_terminais,
            "T":GR.terminais,
            "P":GR.regras,
            "S":GR.inicial
        }))

def Salva_GLC(GLC):
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    nome = "GLC"
    i = 1
    while os.path.exists(PATH+f"{nome}.json"):
        nome = nome[0:3]+f"({i})"
        i += 1
    path_ = filedialog.asksaveasfilename(initialdir=PATH, defaultextension='.json', initialfile=f"{nome}.json")
    if path_ == '':
        return
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"GCL",
            "N":GR.nao_terminais,
            "T":GR.terminais,
            "P":GR.regras,
            "S":GR.inicial
        }))

def Salva_ER(ER):
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    nome = "ER"
    i = 1
    while os.path.exists(PATH+f"{nome}.json"):
        nome = nome[0:2]+f"({i})"
        i += 1
    path_ = filedialog.asksaveasfilename(initialdir=PATH, defaultextension='.json', initialfile=f"{nome}.json")
    if path_ == '':
        return
    with open(path_, 'w') as arquivo:
        arquivo.writelines(json.dumps({
            "TIPO":"ER",
            "expressao":ER.expressao,
            "alfabeto":ER.alfabeto}))

def Pega_Json():
    path = RecebeArquivo()
    if path == '': 
        return None
    with open(path, 'r') as arquivo:
        return json.loads(arquivo.readline())
    
def RecebeArquivo():
    global PATH
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    return filedialog.askopenfilename(initialdir=PATH, filetypes=[("Arquivos JSON", "*.json")])



