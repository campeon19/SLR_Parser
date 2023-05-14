# YAPar reader

def split(line):
    result = []
    word = ""
    for char in line:
        if char == " ":
            result.append(word)
            word = ""
        else:
            word += char
    result.append(word)
    return result


def find(string, char):
    for index, char_ in enumerate(string):
        if char_ == char:
            return index
    return -1

# funcion para buscar un string en una cadena y retornar el indice


def find2(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return index
    return -1

# funcion para buscar un string en una cadena y retornar True o False


def find3(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return True
    return False

# borrar espacios en blanco de una cadena


def delete_white_spaces(string):
    result = ""
    for char in string:
        if char != " ":
            result += char
    return result


def delete_jump_line(string):
    result = ""
    for char in string:
        if char != "\n":
            result += char
    return result

# borrar espacio en blanco de una cadena excepto cuando este rodeado de comillas


def delete_white_spaces2(string):
    result = ""
    for index, char in enumerate(string):
        if char == " ":
            if index == 0 or index == len(string) - 1:
                continue
            elif string[index - 1] != "'" and string[index + 1] != "'" and string[index - 1] != '"' and string[index + 1] != '"':
                continue
        result += char
    return result


def Yapar_reader(archivo):
    with open(archivo, "r") as file:
        content = file.read()

    # eliminar comentarios

    while find3(content, "/*"):
        index = find2(content, "/*")
        index2 = find2(content, "*/")
        content = content[:index] + content[index2 + 2:]

    token_list = []

    while '%token' in content:
        index = find2(content, '%token')
        content = content[index + 7:]
        index2 = find(content, '\n')
        token = content[:index2]
        token_list.append(token)
        content = content[index2 + 1:]

    # print(token_list)

    # separate tokens if there are more than one in the same line
    for index, token in enumerate(token_list):
        if " " in token:
            x = split(token)
            token_list[index] = x[0]
            for i in range(1, len(x)):
                token_list.append(x[i])
    # print(token_list)
    # print(content)

    # read productions
    productions = {}
    while content != "":
        index = find2(content, ":\n")
        index2 = find(content, ";")
        head = content[:index]
        head = delete_jump_line(head)
        body = content[index + 2:index2]
        body = delete_jump_line(body)
        print(body)
        x = split(body)
        # delete empty strings
        while "" in x:
            x.remove("")
        # print(x)
        res = []
        word = ""
        for element in x:
            if element == "|":
                word = word[:len(word) - 1]
                res.append(word)
                word = ""
            else:
                word += element + " "
        # delete last white space
        word = word[:len(word) - 1]
        res.append(word)
        productions[head] = res

        content = content[index2 + 1:]

    # get no terminals by getting keys from productions
    no_terminals = list(productions.keys())
    print(no_terminals)
    print(productions)
    print(token_list)
    return token_list, no_terminals, productions


# Yapar_reader("slr-4.yalp")
