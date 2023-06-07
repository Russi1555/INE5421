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


automata = AF(['q0', 'q1', 'q2', 'q3'],
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

automatoParaMinimizar = AF(['A','B','C','D','E','F','G','H'],
                           ['0','1'],
                           {'A':{'0':'G','1':'B'},
                            'B':{'0':'F','1':'E'},
                            'C':{'0':'C','1':'G'},
                            'D':{'0':'A','1':'H'},
                            'E':{'0':'E','1':'A'},
                            'F':{'0':'B','1':'C'},
                            'G':{'0':'G','1':'F'},
                            'H':{'0':'H','1':'D'}},
                           'A',
                           ['A','D','G'])
teste21 = AF(['S','A','B','C','D','E','F','G', 'H'],
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



#expressaoRegular = ER("(a|b)*abb", ['a','b'])
#AFD = expressaoRegular.ER_para_AFD()
#print(AFD)
#state = '3'
print(teste21)
teste21.minimiza_AFD()
print(teste21)
#closure = automato2.fechamento_ep('q1')
#print(automata)
#automata_DFA = automata.convert_to_AFD()
#print(automata_DFA)
#Gramatica = automata_DFA.convert_to_GR()
#AFND_final = Gramatica.convert_to_AFND()
#print(automata_DFA)
#print(Gramatica)
#print(AFND_final)
#print(closure)  # Output: {'q1', 'q2'}
