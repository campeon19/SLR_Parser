from YAPar_reader import Yapar_reader
from SLR import construccion_slr
# from scanners.scanner_slr1 import get_tokens
# from scanners.scanner_slr2 import get_tokens
# from scanners.scanner_slr3 import get_tokens
from scanners.scanner_slr4 import get_tokens


def main():
    archivo_yapar = 'yapars/slr-4.yalp'
    terminals, no_terminals, gramatica = Yapar_reader(archivo_yapar)
    tokens = get_tokens()
    for val in terminals:
        if val in tokens.values():
            pass
        else:
            print("Token no definidos", val)
            exit(1)
    print('todos los tokens estan definidos')
    slr = construccion_slr(gramatica, terminals, no_terminals)
    slr.draw_afd()


if __name__ == '__main__':
    main()
