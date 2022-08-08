import json
import abrir_dict


dicionario = abrir_dict.abrir_dicionario()


def tratar_nome_aluno():
    aluno = str(input('Digite o nome completo do aluno(a): ')).lower()
    # Retirar os espaços desnecessários, pois atrapalham a pesquisa.
    nome_lis = aluno.split()
    nome_aluno = " ".join(nome_lis)
    return nome_aluno


def percorrer_lista_infantil(aluno):
    global nome_aluno, matricula, segmento
    nome_aluno, matricula, segmento = None, None, None
    for aluno_cadastrado in dicionario["alunos"]["alunos_infantil"]:
        if aluno in aluno_cadastrado["nome"].lower():
            # Pegar o nome diretamente do dicionário para o usuário conferir se retornou o aluno certo.
            nome_aluno = aluno_cadastrado["nome"]
            matricula = aluno_cadastrado["matricula"]
            segmento = 'infantil'
            break
    return nome_aluno, matricula, segmento


def percorrer_lista_primario(aluno):
    global nome_aluno, matricula, segmento
    nome_aluno, matricula, segmento = None, None, None
    for aluno_cadastrado in dicionario["alunos"]["alunos_primario"]:
        if aluno in aluno_cadastrado["nome"].lower():
            # Pegar o nome diretamente do dicionário para o usuário conferir se retornou o aluno certo.
            nome_aluno = aluno_cadastrado["nome"]
            matricula = aluno_cadastrado["matricula"]
            segmento = 'primario'
            break
    return nome_aluno, matricula, segmento


def percorrer_lista_ginasio(aluno):
    global nome_aluno, matricula, segmento
    nome_aluno, matricula, segmento = None, None, None
    for aluno_cadastrado in dicionario["alunos"]["alunos_ginasio"]:
        if aluno in aluno_cadastrado["nome"].lower():
            # Pegar o nome diretamente do dicionário para o usuário conferir se retornou o aluno certo.
            nome_aluno = aluno_cadastrado["nome"]
            matricula = aluno_cadastrado["matricula"]
            segmento = 'ginasio'
            break
    return nome_aluno, matricula, segmento


def calcular_valor_total(matricula, segmento):
    valor_total = 0
    for aluno in dicionario["alunos"][f"alunos_{segmento}"]:
        if matricula == aluno["matricula"]:

            # Calcular a soma das parcelas cadastradas (valor total da compra).
            num_parcelas = aluno["num_parcelas"]
            parcelas = []
            for n in range(1, num_parcelas + 1):
                valor_parcela = aluno["parcelas"][f"parcela{n}"]["valor_parcela"]
                parcelas.append(valor_parcela)
            valor_total = sum(parcelas)

            email_aluno = aluno["email"]

    # Incluir informações que serão usadas no módulo de entrega no arquivo do aluno pesquisado.
    chave = ['nome_aluno', 'segmento', 'matricula', 'valor_total', 'email_aluno']
    valor = [nome_aluno, segmento, matricula, valor_total, email_aluno]
    dados_aluno = {k: v for k, v in zip(chave, valor)}
    return dados_aluno


def criar_json(objeto):
    with open('dados_aluno.json', 'w') as json_file:
        json.dump(objeto, json_file, indent=4)
        json_file.close()


# Função que organiza a execução deste script.
def executar_valor_modulo(aluno):
    nome_aluno, matricula, segmento = percorrer_lista_infantil(aluno)
    if matricula is None:
        nome_aluno, matricula, segmento = percorrer_lista_primario(aluno)
        if matricula is None:
            nome_aluno, matricula, segmento = percorrer_lista_ginasio(aluno)
            if matricula is None:
                print("Aluno(a) não encontrado(a).")
    if matricula is not None:
        dados_aluno = calcular_valor_total(matricula, segmento)
        criar_json(dados_aluno)


if __name__ == '__main__':
    aluno = tratar_nome_aluno()
    executar_valor_modulo(aluno)
