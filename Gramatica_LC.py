class GLC():
    def __init__(self, N, T, P, S):
        self.nao_terminais = N
        self.terminais = T
        self.regras = P  # {Tx : ['T'], Ty: ['TN', 'T'], Tz: ['NTN', 'N', 'T']}
        self.inicial = S

    def __repr__(self):
        string = ""
        for estado in self.regras:
            if estado == self.inicial:
                substring = (f"*{estado} -> ")
            else:
                substring = (f"{estado} -> ")
            for producao in self.regras[estado]:
                substring += producao
                substring += " | "
            string += substring[:-2]
            string += "\n"
        return string

    def remove_non_determinism(self):
        pass  # TODO

    def remove_direct(self):
        regras = self.regras
        for estado in list(regras):
            first_prods = {}
            for prod in regras.get(estado):
                if prod[0] in self.terminais:
                    if prod[0] not in first_prods :
                        first_prods.update({prod[0]: [prod]})
                    else:
                        first_prods.get(prod[0]).append(prod)
            for nt in first_prods:
                if len(first_prods.get(nt)) > 1:
                    new_prods = nt + f'{estado}`'
                    for i in range(len(first_prods.get(nt))):
                        regras.get(estado).remove(first_prods.get(nt)[i])
                        first_prods.get(nt)[i] = first_prods.get(nt)[i].replace(nt, '')

                    regras.update({estado + '`': []})
                    for prod in first_prods.get(nt):
                        regras.get(estado+'`').append(prod)
                    regras.get(estado).append(new_prods)
        self.regras.update(regras)

    def remove_indirect(self):
        pass

    def assemble_first(self):
        pass  # TODO

    def assemble_follow(self):
        pass  # TODO
