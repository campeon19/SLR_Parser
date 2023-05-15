from YALex_reader3 import Yalex_reader
from direct_afd1 import regex_to_afd, simular_afd2
from jinja2 import Template
import pickle


def main():
    archivo_yalex = 'slr-4.yal'
    rule_token, token_dic = Yalex_reader(archivo_yalex)
    with open('template.j2', 'r') as f:
        template = f.read()

    template = Template(template)
    rendered = template.render(tokens=token_dic)
    with open('scanner.py', 'w') as f:
        f.write(rendered)
    afd = regex_to_afd(rule_token, token_dic)

    print("afd generado")
    with open('afd.pickle', 'wb') as f:
        pickle.dump(afd, f)


if __name__ == '__main__':
    main()
