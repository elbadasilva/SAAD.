import json
import datetime
import abrir_dict

dicionario = abrir_dict.abrir_dicionario()


# Ler as informações geradas no módulo de pagamento, que serão utilizadas neste.
def ler_dados_aluno():
    arquivo = open("dados_aluno.json", "r")
    global dados_aluno
    dados_aluno = json.load(arquivo)
    arquivo.close()
    return dados_aluno


# Antes de executar as demais funções, testa se os módulos já foram entregues.
def checar_entrega(status_entrega):
    pass


# Verificar se o total pago até o momento cobre o preço total calculado para o aluno pesquisado.
def verificar_total_pago():
    
    global matricula, segmento
    matricula = dados_aluno['matricula']
    segmento = dados_aluno['segmento']
    valor_total = dados_aluno['valor_total']
    valor_pago = 0
    itens_comprados = {}

    # Pegar as informações do aluno com um teste de matrícula.
    for aluno in dicionario["alunos"][f"alunos_{segmento}"]:
        if matricula == aluno["matricula"]:

            # Calcular o valor pago até o momento (soma das parcelas pagas).
            num_parcelas = aluno["num_parcelas"]
            parcelas = []
            for n in range(1, num_parcelas + 1):
                if aluno["parcelas"][f"parcela{n}"]["status_pagamento"]:
                    valor_parcela = aluno["parcelas"][f"parcela{n}"]["valor_parcela"]
                    parcelas.append(valor_parcela)
            valor_pago = sum(parcelas)
                            
            # Pegar os itens comprados para autorizar a entrega.
            if segmento == 'infantil':  # o segmento infantil possui 2 partes
                itens_comprados = {'parte1': aluno['parte1'], 'parte2': aluno['parte2']}
            else:  # os segmentos primário e ginásio possuem 4 cadernos
                itens_comprados = {'caderno1': aluno['caderno1'],
                                   'caderno2': aluno['caderno2'],
                                   'caderno3': aluno['caderno3'],
                                   'caderno4': aluno['caderno4']}

    if valor_pago >= valor_total:
        # Todos os itens comprados estão liberados para a entrega.
        entrega = True
    else:
        entrega = False  # Exige verificação pelo pagamento mensal.

    return itens_comprados, entrega


# Mostrar quais itens podem ser entregues, quando todos estão autorizados.
def autorizar_entrega_total(itens_comprados):
    print("Módulos disponíveis para entrega: ")
    for key, value in itens_comprados.items():
        if value:
            print(key)


# Verificar se o pagamento parcelado está em dia.
def verificar_data_vencimento():
    
    for aluno in dicionario["alunos"][f"alunos_{segmento}"]:
        if matricula == aluno["matricula"]:  # Testa o aluno pela matrícula.
            
            # Para limitar o loop à quantidade de parcelas.
            num_parcelas = aluno["num_parcelas"]

            for n in range(1, num_parcelas + 1):
                
                # Se a parcela estiver sem pagamento.
                if not aluno[f"parcela{n}"]["status_pagamento"]:
                    
                    # Pega a data de vencimento da parcela.
                    vencimento = aluno[f"parcela{n}"]["data_vencimento"]
                    hoje = datetime.datetime.today()
                    # Converte de str para datetime.
                    vencimento = datetime.datetime.strptime(vencimento, "%Y-%m-%d")

                    if vencimento >= hoje:  # Se a parcela não estiver vencida.
                        #  Percorrer as datas de início das unidades.
                        for unidade in dicionario["referencia_datas_unidades"]:

                            # Pega a data da unidade.
                            data_unidade = dicionario["referencia_datas_unidades"][unidade]
                            # Converte de str para datetime.
                            data_unidade = datetime.datetime.strptime(data_unidade, "%Y-%m-%d")
                            if hoje >= data_unidade:
                                print(f'Módulo da {unidade} disponível para a entrega.')
                                return True

                    else:  # Se a parcela estiver vencida.
                        print("Nenhum módulo disponível para a entrega.")
                    # Se encontrou uma parcela sem pagamento, não precisa testar as próximas.
                    break


def status_entrega():  # Se a entrega for efetivada.
    pass


# Função que organiza a execução deste script
def executar_autorizar_entrega():
    global dados_aluno
    dados_aluno = ler_dados_aluno()
    itens_comprados, entrega = verificar_total_pago()
    if entrega:
        autorizar_entrega_total(itens_comprados)
        return True  # Disparar o e-mail de aviso.
    else:
        disparar_email = verificar_data_vencimento()
        if disparar_email:
            return True  # Se algum item puder ser entregue, disparar o e-mail de aviso.


if __name__ == '__main__':
    executar_autorizar_entrega()

