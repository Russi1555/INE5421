from Gramatica_Regular import GR
from Automato_finito import AF

automata = AF(['q0', 'q1', 'q2', 'q3'],
              ['a', 'b'],
              [['q0', 'a', 'q1'],
               ['q1', '&', 'q2'],
               ['q1', 'a', 'q3'],
               ['q2', 'b', 'q0']],
              'q0',
              ['q3'])

automato2 = AF(['1','2','3'],
               ['a','b'],
               [['1','b','2'],
                ['1','&','3'],
                ['2','a','1'],
                ['2','b','2'],
                ['3','a','2'],
                ['3','a','3'],
                ['3','b','3']],
               '1',
               ['2'])

state = '3'
closure = automato2.fechamento_ep('q1')
automata_DFA = automata.convert_to_AFD()
Gramatica = automata_DFA.convert_to_GR()
AFND_final = Gramatica.convert_to_AFND()
print(automata_DFA)
print(Gramatica)
print(AFND_final)
#print(closure)  # Output: {'q1', 'q2'}