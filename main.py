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
# 0 1
#→ p {p, q} {p}
#q {r} {r}
#r {s} ∅
#∗s {s} {s}

automatoAFND = AF(['p','q','r','s'],
                  ['0','1'],
                  {'p':{'0':'p', '1':'p', '&':'q'},
                   'q':{'0':'r', '1':'r'},
                   'r':{'0':'s'},
                   's':{'0':'s', '1':'s'}},
                   'p',
                   ['s'])
        
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


automato3 = AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              {'q0':{'a':'q1'},
               'q1':{'b':'q2','a':'q3'},
               'q2':{'b':'q3'},
               'q3':{'b':'q0', 'a':'q0'}},
              'q0',
              ['q3'])

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

Novo = automato.convert_to_GR()
print(automato)
print(Novo.convert_to_AFND())
print(Novo)



