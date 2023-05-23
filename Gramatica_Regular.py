
class GR():
    def __init__(self,N,T,R,S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = R
        self.inicial = S
    
    def __repr__(self):
        string =""
        for regra in self.regras:
            if len(regra) == 3:
                string +=(f" {regra[0]} -> {regra[1]}{regra[2]}\n")
            else:
                string +=(f"*{regra[0]} -> {regra[1]}\n")
        return string