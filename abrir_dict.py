import json
from main import arquivo_teste


def abrir_dicionario():
    arquivo_json = open(arquivo_teste, 'r')
    dicionario_json = json.load(arquivo_json)
    arquivo_json.close()
    return dicionario_json


if __name__ == '__main__':
    dicionario = abrir_dicionario()
    print(dicionario)
