
import graphviz
OPERATORS = ['|', '.', '*', '+', '?', '(', ')']
PARENTESIS = ['(', ')']
# TOKEN = {0: 'Return ID', 1: 'Return X', 2: 'Return YZ'}
# TOKEN = {0: 'Return DIGIT', 1: 'Return DIFERENCIA',
#          2: 'Return IGUAL', 3: 'Return ESPACIO', 4: 'Return SUMA', 5: 'Return MULTIPLICACION', 6: 'Return LPAREN', 7: 'Return RPAREN'}
TOKEN = {0: 'Return Number'}


class Simbolo:
    def __init__(self, simbolo, is_operator=False):
        self.val = simbolo
        self.id = ord(simbolo)
        self.is_operator = is_operator


class Trancision:
    def __init__(self, simbolo, estado):
        self.simbolo = simbolo
        self.estado = estado

# La clase Estado es la encargada de almacenar el id del estado, si es final o no, y las trancisiones que tiene un estado hacia otros estados


class Estado:
    def __init__(self, id, es_final=False, token=None):
        self.id = id
        self.es_final = es_final
        self.token = token
        self.trancisiones = {}
    # Se agrega una trancision al estado

    def agregar_trancision(self, simbolo, estado):
        # Si el simbolo ya existe en las trancisiones se agrega el estado al que se va a transicionar
        if simbolo in self.trancisiones:
            self.trancisiones[simbolo].append(estado)
        # Si el simbolo no existe en las trancisiones se crea una nueva trancision
        else:
            self.trancisiones[simbolo] = [estado]
    # Se obtienen las trancisiones de un estado

    def get_trancisiones(self, simbolo):
        if simbolo in self.trancisiones:
            return self.trancisiones[simbolo]
        else:
            return []
    # Se borra una trancision de un estado

    def borra_trancision(self, simbolo):
        if simbolo in self.trancisiones:
            del self.trancisiones[simbolo]


class AFD:

    def __init__(self):
        self.estados = set()
        self.estados_iniciales = set()
        self.estados_finales = set()

    def get_estados(self):
        return self.estados

    def get_estados_finales(self):
        return self.estados_finales

    def draw_afd(self):
        dot = graphviz.Digraph(comment='AFD')
        for estado in self.estados:
            if estado.es_final:
                dot.node(str(estado.id), str(estado.id), shape="doublecircle")
            else:
                dot.node(str(estado.id), str(estado.id))
        for estado in self.estados:
            for simbolo in estado.trancisiones:
                for estado_siguiente in estado.get_trancisiones(simbolo):
                    dot.edge(str(estado.id), str(
                        estado_siguiente.id), label=simbolo)
        dot.format = 'png'
        dot.attr(rankdir='LR')
        dot.render('AFD2', view=True)

    def get_estado(self, id):
        for estado in self.estados:
            # print(estado.id)
            if estado.id == id:
                return estado

    def get_estado_inicial(self):
        for estado in self.estados:
            if estado.id == 0:
                return estado


class Node:
    def __init__(self, valor, id):
        self.valor = valor
        self.id = id
        self.izquierda = None
        self.derecha = None
        self.nulabilidad = None
        self.primera_posicion = set()
        self.ultima_posicion = set()
        self.siguiente_posicion = set()
        self.siguientes_posiciones = []


def build_tree(postfix):
    # Se crea una pila vacía
    stack = []
    id = 0
    # Se recorre la expresión regular
    for c in postfix:
        # Si se encuentra un simbolo alfanumerico se crea un nodo con el simbolo y se agrega a la pila
        if not c.is_operator:
            if c.val == 'ε':
                stack.append(Node(c, None))
            else:
                stack.append(Node(c, id))
                id += 1
        # Si se encuentra un operador unario se crea un nodo con el operador y se saca un nodo de la pila y se agrega como hijo del nodo creado
        elif c.val == '*' or c.val == '+' or c.val == '?':
            node = Node(c, None)
            node.izquierda = stack.pop()
            stack.append(node)
        # Si se encuentra un operador se crea un nodo con el operador y se sacan los dos nodos de la pila y se agregan como hijos del nodo creado
        elif c.val == "|" or c.val == ".":
            node = Node(c, None)
            # print(stack.val)
            node.derecha = stack.pop()
            node.izquierda = stack.pop()
            node.valor = c
            stack.append(node)
    return stack.pop()


def draw_tree(root):
    # Se crea un grafo dirigido
    dot = graphviz.Digraph()
    # Se recorre el árbol de expresiones regulares

    def traverse(node):
        # Si el nodo no es nulo se crea un nodo con el id del nodo y el dato del nodo y se agregan las aristas correspondientes
        if node:
            pp = [str(x) for x in node.primera_posicion]
            up = [str(x) for x in node.ultima_posicion]
            r = node.valor + " " + str(pp) + " " + \
                str(up) + " " + str(node.nulabilidad)
            s = [str(x) for x in node.siguiente_posicion]
            dot.node(str(id(node)), str(r))
            # Si el nodo tiene un hijo izquierdo se crea una arista entre el nodo y el hijo izquierdo
            if node.izquierda:
                dot.edge(str(id(node)), str(id(node.izquierda)))
            # Si el nodo tiene un hijo derecho se crea una arista entre el nodo y el hijo derecho
            if node.derecha:
                dot.edge(str(id(node)), str(id(node.derecha)))
            # Se recorre el hijo izquierdo y el hijo derecho utilizando recursividad
            traverse(node.izquierda)
            traverse(node.derecha)

    traverse(root)
    return dot


def calculate_nullable(root):
    if root is None:
        return False
    if not root.valor.is_operator:
        if root.valor.val == 'ε':
            root.nulabilidad = True
        else:
            root.nulabilidad = False
        return False
    if root.valor.val == '|':
        nullable = root.izquierda.nulabilidad or root.derecha.nulabilidad
    elif root.valor.val == '.':
        nullable = root.izquierda.nulabilidad and root.derecha.nulabilidad
    elif root.valor.val == '*':
        nullable = True
    elif root.valor.val == '+':
        nullable = root.izquierda.nulabilidad
    elif root.valor.val == '?':
        nullable = True
    else:
        nullable = False
    root.nulabilidad = nullable
    return nullable or False


def traverse_postorder(node, func):
    if node is not None:
        traverse_postorder(node.izquierda, func)
        traverse_postorder(node.derecha, func)
        func(node)


def calculate_first_position(node):
    if node:
        # Si el nodo es una hoja, su primera posición es su propio índice
        if node.izquierda is None and node.derecha is None:
            node.primera_posicion.add(node.id)
        # Si el nodo es un operador ., su primera posición es la primera posición de su hijo izquierdo
        elif node.valor.val == '.' and node.valor.is_operator:
            calculate_first_position(node.izquierda)
            calculate_first_position(node.derecha)
            if node.izquierda.nulabilidad:
                node.primera_posicion = node.izquierda.primera_posicion.union(
                    node.derecha.primera_posicion)
            else:
                node.primera_posicion = node.izquierda.primera_posicion
        # Si el nodo es un operador |, su primera posición es la unión de las primeras posiciones de sus dos hijos
        elif node.valor.val == '|' and node.valor.is_operator:
            calculate_first_position(node.izquierda)
            calculate_first_position(node.derecha)
            if list(node.izquierda.primera_posicion)[0] == None:
                node.primera_posicion = node.derecha.primera_posicion
            elif list(node.derecha.primera_posicion)[0] == None:
                node.primera_posicion = node.izquierda.primera_posicion
            else:
                node.primera_posicion = node.izquierda.primera_posicion.union(
                    node.derecha.primera_posicion)
        # Si el nodo es un operador *, su primera posición es la primera posición de su hijo
        elif node.valor.val == '*' and node.valor.is_operator:
            calculate_first_position(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion
        elif node.valor.val == '+' and node.valor.is_operator:
            calculate_first_position(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion
        elif node.valor.val == '?' and node.valor.is_operator:
            calculate_first_position(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion

        # Calcular la primera posición del hijo izquierdo y derecho utilizando recursividad
        # calculate_first_position(node.izquierda)
        # calculate_first_position(node.derecha)

    # Calcular la primera posición del nodo raíz
    if node and node.valor.val is not None and node.primera_posicion is None:
        node.primera_posicion = node.izquierda.primera_posicion


def calculate_last_position(node):
    if node:
        # Si el nodo es una hoja, su última posición es su propio índice
        if node.izquierda is None and node.derecha is None:
            node.ultima_posicion.add(node.id)
        # Si el nodo es un operador ., su última posición es la última posición de su hijo derecho
        elif node.valor.val == '.' and node.valor.is_operator:
            calculate_last_position(node.izquierda)
            calculate_last_position(node.derecha)
            if node.derecha.nulabilidad:
                node.ultima_posicion = node.izquierda.ultima_posicion.union(
                    node.derecha.ultima_posicion)
            else:
                node.ultima_posicion = node.derecha.ultima_posicion
        # Si el nodo es un operador |, su última posición es la unión de las últimas posiciones de sus dos hijos
        elif node.valor.val == '|' and node.valor.is_operator:
            calculate_last_position(node.izquierda)
            calculate_last_position(node.derecha)
            if list(node.izquierda.ultima_posicion)[0] == None:
                node.ultima_posicion = node.derecha.ultima_posicion
            elif list(node.derecha.ultima_posicion)[0] == None:
                node.ultima_posicion = node.izquierda.ultima_posicion
            else:
                node.ultima_posicion = node.izquierda.ultima_posicion.union(
                    node.derecha.ultima_posicion)
        # Si el nodo es un operador *, su última posición es la última posición de su hijo
        elif node.valor.val == '*' and node.valor.is_operator:
            calculate_last_position(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion
        elif node.valor.val == '+' and node.valor.is_operator:
            calculate_last_position(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion
        elif node.valor.val == '?' and node.valor.is_operator:
            calculate_last_position(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion

        # Calcular la última posición del hijo izquierdo y derecho utilizando recursividad
        # calculate_last_position(node.izquierda)
        # calculate_last_position(node.derecha)

    # Calcular la última posición del nodo raíz
    if node and node.valor.val is not None and node.ultima_posicion is None:
        node.ultima_posicion = node.derecha.ultima_posicion


def print_tree(arbol):
    if arbol:
        print(arbol.valor.val, arbol.nulabilidad)
        print_tree(arbol.izquierda)
        print_tree(arbol.derecha)


table = []


def calculate_follow_position(arbol):
    val = True
    if arbol:

        if arbol.valor.val == '.' and arbol.valor.is_operator:
            for i in arbol.izquierda.ultima_posicion:
                for k in table:
                    if k[0] == i:
                        k[2].extend(list(arbol.derecha.primera_posicion))
                        val = False
                if val:
                    simbol = get_val_from_node(arbol, i)
                    table.append(
                        [i, simbol, list(arbol.derecha.primera_posicion)])
        elif arbol.valor.val == '*' and arbol.valor.is_operator:
            for i in arbol.ultima_posicion:
                for k in table:
                    if k[0] == i:
                        k[2].extend(list(arbol.primera_posicion))
                        val = False
                if val:
                    simbol = get_val_from_node(arbol, i)
                    table.append([i, simbol, list(arbol.primera_posicion)])
                    # arbol.siguientes_posiciones[i].append(j)
        elif arbol.valor.val == '+' and arbol.valor.is_operator:
            for i in arbol.ultima_posicion:
                for k in table:
                    if k[0] == i:
                        k[2].extend(list(arbol.primera_posicion))
                        val = False
                if val:
                    simbol = get_val_from_node(arbol, i)
                    table.append([i, simbol, list(arbol.primera_posicion)])
                    # arbol.siguientes_posiciones[i].append(j)
        val = False
        for k in table:
            if k[0] == arbol.id:
                val = True
        if not val:
            simbol = get_val_from_node(arbol, arbol.id)
            table.append([arbol.id, simbol, []])
        # delete list with None in first position
        for i in table:
            if i[0] is None:
                table.remove(i)

        calculate_follow_position(arbol.izquierda)
        calculate_follow_position(arbol.derecha)


def get_val_from_node(arbol, id):
    if arbol:
        if arbol.id == id:
            return arbol.valor.val
        else:
            return get_val_from_node(arbol.izquierda, id) or get_val_from_node(arbol.derecha, id)


def get_first_position(arbol, id):
    if arbol:
        if arbol.id == id:
            return arbol.primera_posicion
        else:
            return get_first_position(arbol.izquierda, id) or get_first_position(arbol.derecha, id)


def get_siguiente_posicion(tab, id):
    for i in tab:
        if i[0] == id:
            return i[2]


def Trans(state, simbol, tab):
    conj = []
    for i in state:
        for j in tab:
            if j[0] == i and j[1] == simbol:
                for k in j[2]:
                    if k not in conj:
                        conj.append(k)
    return conj


def get_simbols(tab):
    simbols = []
    for i in tab:
        if i[1] not in simbols:
            simbols.append(i[1])
    return simbols


def get_final_state(tab):
    # print(tab)
    final_state = []
    for i in tab:
        if i[1] == '#':
            final_state.append(i[0])
    # print('final state')
    # print(final_state)
    return final_state


def regex_to_afd(regex, token_dic):
    TOKEN = token_dic
    print('Iniciando contruccion de AFD')

    arbol = build_tree(regex)
    print('arbol contruido')
    calculate_nullable(arbol)
    traverse_postorder(arbol, calculate_nullable)
    print('nulabilidad calculada')
    calculate_first_position(arbol)
    print('primera posicion calculada')
    calculate_last_position(arbol)
    print('ultima posicion calculada')
    calculate_follow_position(arbol)
    print('siguientes posiciones calculadas')
    tab = sorted(table, key=lambda x: x[0])
    root = arbol.primera_posicion
    alfabeto = get_simbols(tab)
    # remove # from alphabet
    alfabeto.remove('#')
    id_estado = 0
    afd = AFD()
    conjunto_estados = {}
    transiciones = []
    id = 0
    x = []
    for y in root:
        x.append(y)
    conjunto_estados[id] = x
    # print(conjunto_estados)
    id += 1
    estados_visitados = []
    estados_por_visitar = []
    # print(conjunto_estados[0])
    estados_por_visitar.append(conjunto_estados[0])
    # print(alfabeto)
    # afd.estados.add(es)
    final = get_final_state(tab)
    # print(tab)
    while len(estados_por_visitar) > 0:
        estado_actual = estados_por_visitar.pop()
        # print(estado_actual)
        estados_visitados.append(estado_actual)
        for simbolo in alfabeto:
            # print(simbolo)
            transicion = Trans(estado_actual, simbolo, tab)
            # print(id)

            # print(transicion)
            # if transicion is not an empty list
            # if transicion != []:
            transicion = sorted(transicion)
            # print(transicion)

            if transicion != [] and not None:
                transiciones.append([estado_actual, simbolo, transicion])
                if transicion not in estados_visitados and transicion not in estados_por_visitar:
                    # print('not in estados_visitados and estados_por_visitar')
                    # print(transicion)
                    conjunto_estados[id] = transicion
                    # print(conjunto_estados)
                    estados_por_visitar.append(transicion)
                    estados_por_visitar = sorted(
                        estados_por_visitar, reverse=True)
                    # print("estados por visitar")
                    # print(estados_por_visitar)
                    id += 1
            # if len(estados_por_visitar) == 0:
            #     estados_num = []
            #     for k in new_transiciones:
            #         estados_num.append(k[0])
            #     if len(estados_num) < len(conjunto_estados):

    # if list in value in conjunto_estados.values() is NULL, delete item
    # validate if all nodes

    for key, value in conjunto_estados.items():
        if value == []:
            del conjunto_estados[key]
            break
    # print(conjunto_estados)
    # print()
    # print(transiciones)

    # sustituir en transiciones: estado_actual por id
    new_transiciones = []
    for key, value in conjunto_estados.items():
        for i in transiciones:
            if i[0] == value:
                new_transiciones.append([key, i[1], i[2]])
    # sustituir en transiciones: transicion por id
    for key, value in conjunto_estados.items():
        for i in new_transiciones:
            if i[2] == value:
                i[2] = key

    # print(new_transiciones)

    estados_num = []
    for key, value in conjunto_estados.items():
        estados_num.append(key)
    # for k in new_transiciones:
    #     estados_num.append(k[0])
    estados_num = set(estados_num)
    for e in estados_num:
        # print(e)
        es = Estado(e)
        # is final state
        for key, value in conjunto_estados.items():
            # print(key, value)
            # print(final in value)
            if key == e:
                for val in value:
                    if val in final:
                        # print("entro")
                        es.es_final = True
                        # get index of final where val is
                        k = final.index(val)
                        es.token = TOKEN[k]
        afd.estados.add(es)

    for estado in afd.estados:
        for k in new_transiciones:
            # print(k[0], estado.id)
            if k[0] == estado.id:
                # print("entro")
                # print(k[2])
                # print(afd.get_estado(k[2]))
                estado.agregar_trancision(k[1], afd.get_estado(k[2]))

    # graph = draw_tree(arbol)
    # graph.format = 'png'
    # graph.render('tree2', view=True)
    return afd


# def simular_afd(afd, cadena):
#     estado_actual = afd.get_estado_inicial()
#     cadena_aceptada = False
#     print(estado_actual.id)
#     for char in cadena:
#         print(char)
#         estado_siguiente = estado_actual.get_trancisiones(char)
#         if estado_siguiente:
#             estado_actual = estado_siguiente[0]
#             print(estado_actual.id)
#         else:
#             return False
#     if estado_actual.es_final:
#         cadena_aceptada = True
#         print(estado_actual.token)
#     return cadena_aceptada


def simular_afd2(afd, cadena):
    estado_actual = afd.get_estado_inicial()
    cadena_aceptada = False
    estado_aceptado = []
    # print(estado_actual.id)
    cadena_leida = ''
    while len(cadena) > 0:
        for char in cadena:
            # print(char)
            estado_siguiente = estado_actual.get_trancisiones(char)
            if estado_siguiente:
                cadena_leida += char
                estado_actual = estado_siguiente[0]
                # print(estado_actual.id)
                if estado_actual.es_final:
                    estado_aceptado.append([estado_actual, cadena_leida])
            else:
                if estado_aceptado != []:
                    token_encontrado = estado_aceptado.pop()
                    print(token_encontrado[1], token_encontrado[0].token)

                    cadena = cadena[len(token_encontrado[1]):]
                    estado_actual = afd.get_estado_inicial()
                    cadena_leida = ''
                    estado_aceptado = []
                    break
                else:
                    cadena_leida += char
                    print(cadena_leida, 'Lexema no encontrado')
                    cadena = cadena[len(cadena_leida):]
                    estado_actual = afd.get_estado_inicial()
                    cadena_leida = ''
                    break
        if estado_aceptado != []:
            token_encontrado = estado_aceptado.pop()
            print(token_encontrado[1], token_encontrado[0].token)
            break


EPSILON = 'ε'
CONCAT = "."
UNION = "|"
STAR = "*"
QUESTION = "?"
PLUS = "+"
LEFT_PARENTHESIS = "("
RIGHT_PARENTHESIS = ")"

OPERADORES = [EPSILON, CONCAT, UNION, STAR, QUESTION,
              PLUS, LEFT_PARENTHESIS, RIGHT_PARENTHESIS]


def convert_to_Simbolo(string):
    array = []
    for char in string:
        array.append(char)

    res = []
    while array:
        char = array.pop(0)
        if char == "'":
            res.append(Simbolo(array.pop(0)))
            array.pop(0)
        elif char in OPERADORES:
            res.append(Simbolo(char, True))
        else:
            res.append(Simbolo(char))
    return res


def shunting_yard(infix):
    # precedencia de los operadores
    precedence = {'|': 1, '.': 2, '?': 3, '*': 3, '+': 3}
    # pila de operadores
    stack = []
    # cola de salida
    postfix = []
    for c in infix:
        # Si se encuentra un ( se agrega a la pila
        if c.val == '(' and c.is_operator == True:
            stack.append(c)
        # Si se encuentra un ) se sacan los operadores de la pila hasta encontrar un (
        elif c.val == ')' and c.is_operator == True:
            while stack[-1].val != '(' and stack[-1].is_operator == True:
                postfix.append(stack.pop())
            stack.pop()
        # Si se encuentra un operador se sacan los operadores de la pila hasta encontrar un operador de menor precedencia
        elif c.val in precedence and c.is_operator == True:
            while stack and stack[-1].val != '(' and stack[-1].is_operator == True and precedence[c.val] <= precedence[stack[-1].val]:
                postfix.append(stack.pop())
            stack.append(c)
        # Si se encuentra un simbolo se agrega a la cola de salida
        else:
            postfix.append(c)
    # Se sacan los operadores restantes de la pila y se agregan a la cola de salida
    while stack:
        postfix.append(stack.pop())

    return postfix


# regex = 'a*b*|c.#.'
# regex = 'bb|*a.b.b.ab|*.#.'
# regex = 'ab|*a.ab|.ab|.#.'
# regex = 'ab|c|d|ab|c|d|ab|c|d||*.#.X#.|YZ.#.|'
# regex = '01|2|3|4|5|6|7|8|9|#.-#.|=#.| #.|'
# regex = "01|2|3|4|5|6|7|8|9|#.-#.|=#.| #.|'+'#.|'*'#.|'('#.|')'#.|"
# regex = 'AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|01|2|3|4|5|6|7|8|9||*.#.'
# regex = "(((0|1|2|3|4|5|6|7|8|9)+.('.'.(0|1|2|3|4|5|6|7|8|9)+)?.('E'.('+'|'-')?.(0|1|2|3|4|5|6|7|8|9)+)?).#)"
# regex = "((0|1|2|3|4|5|6|7|8|9)*).#"

# convert every char to simbol and add to list
# regex_list = convert_to_Simbolo(regex)
# regex_list = shunting_yard(regex_list)
# print(regex_list)


# afd = regex_to_afd(regex_list, TOKEN)
# print(simular_afd2(afd, 'abcXYZabbbtaa='))
# print(simular_afd2(afd, '1 - 2 + (3 * 4) = 13'))
# print(simular_afd2(afd, '25.87E-8xd'))
# afd.draw_afd()
