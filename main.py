from Gramatica_Regular import GR
from Automato_finito import AF
from Gramatica_LC import GLC
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


#print(automato.convert_to_GR())

#teste_gr = GR(['S','A','B','C'],['a','b','c'],{'S': ["ABB","CAC"],'A':['a'],'B':['Bc','ABB'],'C':["bB",'a']},'S')

#teste_glc = GLC(['E','T','F'], ['+', '-', '*', '/', '(', ')', 'i'], {'E': ["E+T", "E-T", "T"], 'T': ["T*F", "T/F", "F"], 'F': ["(E)", "i"]}, 'E')

"""teste_First = GLC(['S','A','B', 'C'],
                ['a','b','c','d'],
                {'S':['ABC'],
                'A':['aA', '&'],
                'B':['bB', 'ACd'],
                'C':['cC','&']},
                'S')
teste_First.assemble_first()
for i,v in teste_First.First.items():
    print(f"{i} -> {v}")
print()
teste_First.assemble_follow()
for i,v in teste_First.Follow.items():
    print(f"{i} -> {v}")"""
                
teste_Tabela_LL = GLC(['P','K','V','F','C'],
                        ['c','v','f',';','b','e','g'],
                        {'P':['KVC'],
                         'K':['cK', '&'],
                         'V':['vV', 'F'],
                         'F':['fP;F', '&'],
                         'C':['bVCe', 'g;C', '&']},
                         'P')
print(teste_Tabela_LL)
teste_Tabela_LL.Cria_Tabela_LL1()
teste_Tabela_LL.MostraTabelaLL1()
"""
teste_nao_determinismo_direto = GLC(['S', 'A', 'B'], ['a', 'b'], {'S': ["aSB", "aSA"], 'A': ['a'], 'B': ['b']}, 'S')
teste_nao_determinismo_direto2 = GLC(['S', 'A', 'B', 'C', 'D'], ['a', 'c', 'd', 'e', 'f'], {'S': ["aDC", "cCC", "aBC", "dDC"], 'A': ["aD", "cC"], 'B': ["aB", "dD"], 'C': ["eC", "eA"], 'D': ["fD", "CB"]}, 'S')

print("----------------teste_fatoracao--------------------")
print(teste_nao_determinismo_direto2)
teste_nao_determinismo_direto2.factorization()
print(teste_nao_determinismo_direto2)
print("----------------teste_fatoracao-------------------")

teste_recursao_direta = GR(['S'],['a','b'],{'S' : ['Sa','b']},'S')

teste_recursao_indireta = GR(['S','A'],['a','b','c','d'],{'S': ["Aa",'b'], 'A': ['Ac','Sd','a']},'S')

teste_recursao_ambas = GR(['S','A'],['a','b','c','d'],{'S':['Aa','Sb'],'A':['Sc','d'],},'S')

print("----------------------------------------------------------------")
print(teste_recursao_direta)
teste_recursao_direta.remove_recursividades()
print(teste_recursao_direta)
print("----------------------------------------------------------------")

print("----------------------------------------------------------------")
print(teste_recursao_indireta)
teste_recursao_indireta.remove_recursividades()
print(teste_recursao_indireta)
print("----------------------------------------------------------------")

print("----------------------------------------------------------------")
print(teste_recursao_ambas)
teste_recursao_ambas.remove_recursividades()
print(teste_recursao_ambas)
print("----------------------------------------------------------------")
"""


