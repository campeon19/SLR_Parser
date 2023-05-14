import graphviz
import copy


class Estado:
    def __init__(self, id, gramatica):
        self.id = id
        self.gramatica = gramatica
        self.transiciones = {}
    # Se agrega una transicion al estado

    def agregar_transicion(self, simbolo, estado):
        # Si el simbolo ya existe en las transiciones se agrega el estado al que se va a transicionar
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(estado)
        # Si el simbolo no existe en las transiciones se crea una nueva transicion
        else:
            self.transiciones[simbolo] = [estado]
    # Se obtienen las transiciones de un estado

    def get_transiciones(self, simbolo):
        if simbolo in self.transiciones:
            return self.transiciones[simbolo]
        else:
            return []
    # Se borra una transicion de un estado

    def borra_transicion(self, simbolo):
        if simbolo in self.transiciones:
            del self.transiciones[simbolo]


class SLR:

    def __init__(self):
        self.estados = set()
        self.estado_inicial = set()

    def get_estados(self):
        return self.estados

    def get_estados_finales(self):
        return self.estados_finales

    def draw_afd(self):
        dot = graphviz.Digraph(comment='SLR')
        for estado in self.estados:
            pr = ""
            for produccion in estado.gramatica:
                pr += str(produccion) + "\n"
            dot.node(str(estado.id), str(pr), shape='square')
        for estado in self.estados:
            for simbolo in estado.transiciones:
                for estado_siguiente in estado.get_transiciones(simbolo):
                    dot.edge(str(estado.id), str(
                        estado_siguiente.id), label=simbolo.nombre)
        dot.format = 'png'
        dot.attr(rankdir='LR')
        dot.render('SLR', view=True)

    def get_estado(self, id):
        for estado in self.estados:
            # print(estado.id)
            if estado.id == id:
                return estado

    def get_estado_inicial(self):
        for estado in self.estados:
            if estado.id == 0:
                return estado


class Terminal:

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Terminal) and self.nombre == __value.nombre

    def __hash__(self) -> int:
        return hash(self.nombre)


class NoTerminal:

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoTerminal) and self.nombre == __value.nombre

    def __hash__(self) -> int:
        return hash(self.nombre)


class Punto:
    def __init__(self):
        self.nombre = "."

    def __str__(self):
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Punto) and self.nombre == __value.nombre


class Produccion:
    def __init__(self, head, produccion: list):
        self.head = head
        self.produccion = produccion

    def __str__(self):
        return self.head.nombre + " -> " + " ".join(str(x) for x in self.produccion)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Produccion) and self.head == __value.head and self.produccion == __value.produccion

    def __hash__(self) -> int:
        return hash(self.head) + hash(self.produccion)

    def get_head(self):
        return self.head

    def get_produccion(self):
        return self.produccion

    def copy(self):
        return Produccion(self.head, self.produccion.copy())

# cerradura de un estado


def cerradura_inicial(gramatica_evaluar, gramatica_inicial):
    gramatica_in = gramatica_inicial.copy()
    gramatica = []
    # add "." to the first production if it doesn't have it in any of its productions
    for produccion in gramatica_evaluar:
        if Punto() not in produccion.produccion:
            print("no tiene punto")
            print(str(produccion))
            produccion.produccion.insert(0, Punto())
            gramatica.append(produccion)
        else:
            # shift Punto to the next position in the list of productions
            index = produccion.produccion.index(Punto())
            if index + 1 < len(produccion.produccion):
                produccion.produccion[index], produccion.produccion[index +
                                                                    1] = produccion.produccion[index + 1], produccion.produccion[index]
                gramatica.append(produccion)

    def cerradura(gramatica, gramatica_in):
        for produccion in gramatica:
            if produccion.produccion[-1] != Punto():
                index = produccion.produccion.index(Punto())
                simbol = produccion.produccion[index + 1]
                for produccion_gramatica in gramatica_in:
                    if simbol == produccion_gramatica.head:
                        if produccion_gramatica not in gramatica:
                            gramatica.append(produccion_gramatica)
                            produccion_gramatica.produccion.insert(0, Punto())
                            cerradura(gramatica, gramatica_in)
    cerradura(gramatica, gramatica_in)
    return gramatica


def ir_a(gramatica, simbolo):
    res = []
    # print(gramatica)
    for produccion in gramatica:
        # print(str(produccion))
        index = produccion.produccion.index(Punto())
        # print(index)
        # print(produccion.produccion[index + 1])
        if index + 1 < len(produccion.produccion):
            if produccion.produccion[index + 1] == simbolo:
                res.append(produccion)
    return res


def extender_gramatica(gramatica):
    element = list(gramatica.keys())[0]
    gramatica_extendida = {element + "'": [element]}
    gramatica_extendida.update(gramatica)
    print(gramatica_extendida)
    return gramatica_extendida


def terminales_to_obj(terminales):
    terminales_obj = []
    for terminal in terminales:
        terminales_obj.append(Terminal(terminal))
    return terminales_obj


def no_terminales_to_obj(no_terminales):
    no_terminales_obj = []
    for no_terminal in no_terminales:
        no_terminales_obj.append(NoTerminal(no_terminal))
    return no_terminales_obj


def gramatica_to_obj(gramatica_extendida, terminales, no_terminales):
    gramatica_inicial = []
    for no_terminal in gramatica_extendida:
        print(no_terminal)
        for produccion in gramatica_extendida[no_terminal]:
            s = produccion.split()
            prod = []
            for word in s:
                if word in terminales:
                    prod.append(Terminal(word))
                elif word in no_terminales:
                    prod.append(NoTerminal(word))
            new_prod = Produccion(NoTerminal(no_terminal), prod)
            gramatica_inicial.append(new_prod)
    return gramatica_inicial


def construccion_slr(gramatica, terminales, no_terminales):
    gramatica_extendida = extender_gramatica(gramatica)
    gramatica_inicial = gramatica_to_obj(
        gramatica_extendida, terminales, no_terminales)
    simbolos = []
    alt = copy.deepcopy(no_terminales)
    # delete the first element of the list
    alt.pop(0)
    simbolos.extend(no_terminales_to_obj(alt))
    simbolos.extend(terminales_to_obj(copy.deepcopy(terminales)))
    # print(simbolos)
    l = []
    l.append(copy.deepcopy(gramatica_inicial[0]))

    res = cerradura_inicial(l, copy.deepcopy(gramatica_inicial))
    # res2 = cerradura_inicial(
    #     ir_a(res, NoTerminal(no_terminales[1])), gramatica_inicial)
    # for x in res2:
    #     print(str(x))
    # id = 0
    # newEstado = Estado(id, res)
    # slr = SLR()
    # slr.estados.add(newEstado)
    # slr.estado_inicial.add(newEstado)
    estados_por_evaluar = []

    id = 0
    newEstado = Estado(id, res)
    id += 1
    estados_por_evaluar.append(newEstado)
    slr = SLR()
    slr.estados.add(newEstado)
    slr.estado_inicial.add(newEstado)

    while len(estados_por_evaluar) > 0:
        estado = estados_por_evaluar.pop(0)
        for simbolo in simbolos:
            gr = ir_a(copy.deepcopy(estado.gramatica), copy.deepcopy(simbolo))
            gr = cerradura_inicial(gr, copy.deepcopy(gramatica_inicial))
            if len(gr) > 0:
                for x in slr.estados:
                    if gr == x.gramatica:
                        # for v in gr:
                        #     print(str(v))
                        # for v in x.gramatica:
                        #     print(str(v))
                        # print("ya existe")
                        estado.agregar_transicion(simbolo, x)
                        break
                else:
                    # for v in gr:
                    #     print(str(v))
                    # print("no existe")
                    newEstado = Estado(id, gr)
                    id += 1
                    estado.agregar_transicion(simbolo, newEstado)
                    slr.estados.add(newEstado)
                    estados_por_evaluar.append(newEstado)

    # for x in range(3):
    #     estado = estados_por_evaluar.pop(0)
    #     for simbolo in simbolos:
    #         gr = ir_a(copy.deepcopy(estado.gramatica), copy.deepcopy(simbolo))
    #         gr = cerradura_inicial(gr, copy.deepcopy(gramatica_inicial))
    #         if len(gr) > 0:
    #             for x in slr.estados:
    #                 if gr == x.gramatica:
    #                     # for v in gr:
    #                     #     print(str(v))
    #                     # for v in x.gramatica:
    #                     #     print(str(v))
    #                     # print("ya existe")
    #                     estado.agregar_transicion(simbolo, x)
    #                     break
    #             else:
    #                 for v in gr:
    #                     print(str(v))
    #                 print("no existe")
    #                 newEstado = Estado(id, gr)
    #                 id += 1
    #                 slr.estados.add(newEstado)
    #                 estados_por_evaluar.append(newEstado)

    # ordenar los estados en slr en orden de estado.id
    slr.estados = sorted(slr.estados, key=lambda estado: estado.id)
    for estado in slr.estados:
        print("estado: " + str(estado.id))
        for x in estado.gramatica:
            print(str(x))
    slr.draw_afd()
    return slr


# terminales = ['PLUS', 'TIMES', 'LPAREN', 'RPAREN', 'ID']
# no_terminales = ["e'", 'e', 't', 'f']
# gramatica = {'e': ['e PLUS t', 't'], 't': [
#     't TIMES f', 'f'], 'f': ['LPAREN e RPAREN', 'ID']}

terminales = ['ID', 'PLUS', 'TIMES', 'LPAREN', 'RPAREN']
no_terminales = ['expression', 'term', 'factor']
gramatica = {'expression': ['expression PLUS term', 'term'], 'term': [
    'term TIMES factor', 'factor'], 'factor': ['LPAREN expression RPAREN', 'ID']}

slr = construccion_slr(gramatica, terminales, no_terminales)

# count estados in slr
# count = 0
# for estado in slr.estados:
#     count += 1
# print(count)
