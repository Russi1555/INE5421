from Gramatica_Regular import GR
from Automato_finito import AF
from Expressao_Regular import ER

# AF(
#  [estados],
#  [alfabeto],
#  {estados: {simbolo:estadosDestino},
#            {simbolo:estadosDestino},
#            {simbolo:estadosDestino}
#            },
#  Qo,
#  [Estados Finais]
# )


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

print("Verdadeiro ", automato.TestaPalavra("abbaa"))
print("Falso ", automato.TestaPalavra("bbb"))
print("Falso ", automato.TestaPalavra("aba"))

print("Verdadeiro ", automato2.TestaPalavra("b"))
print("Verdadeiro ", automato2.TestaPalavra("ba"))
print("Verdadeiro ", automato2.TestaPalavra("aabb"))
print("Verdadeiro ", automato2.TestaPalavra("babbbb"))
print("Falso ", automato2.TestaPalavra(""))


