# UFSC
# INE5421 : Linguagens Formais e Compiladores
# Data: 28/06/23
# Grupo: Enzo Gomes Sônego (17202002),Eduardo Peres Luckner Goulart (19104096), Gustavo Russi (20100526) 	


## Manipulação de Linguagens Regulares e Linguagens Livres de Contexto

 - [x]  Conversão de AFND (com e sem ε) para AFD (0,5pt)
 - [x]  Conversão de AFD para GR e de GR para AFND (0,5pt) 
 - [x]  Minimização de AFD (1,0pt) 
 - [x]  União e interseção de AFD (1,0pt)
 - [x]  Conversão de ER para AFD (usando o algoritmo baseado em árvore sintática - Livro Aho - seção 3.9) (1,5pt)
 - [x]  Reconhecimento de sentenças em AF (0,5pt)
 
 ## Implementar o analisador sintático do tipo preditivo LL(1)
 
 - [x] Leitura e edição de uma Gramática Livre de contexto (considerando terminais como um único símbolo minúsculo e não terminais maiúsculos) (1pt) 
 - [x] Algoritmo para verificação de não determinismo e fatoração da gramática (1pt) 
 - [x] Algoritmo para eliminação de recursão a esquerda (1pt)
 - [x] Firsts e Follows (1pt)
 - [x] Construção da tabela do preditivo LL(1) e construção do algoritmo que simula a pilha para o reconhecimento de uma sentença de entrada (1pt)

 ## Como usar

 - Execute main.py para visualizar, testar se uma palavra pertence a linguagem ou editar os objetos 
 - Execute CriaObjetos.py se não houver objetos para ser importados
 - Caso use fatoração ou remoção de recursão a esquerda, não utilize a gramatica resultante para outras ações
 - Quando usar UNIÃO ou INTERSECÇÃO que estão na seleção '5- Metodos do Objeto' do menu, selecione apenas AFs para combinar
 - Para editar os objetos, no menu selecione '5- Metodos do Objeto' tendo um objeto selecinado
 - Para visualizar First, Follow e tabela LL(1), entre no '5- Metodos do Objeto' do menu
