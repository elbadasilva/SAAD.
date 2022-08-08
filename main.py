import sys
import os
import valor_modulo
import autorizar_entrega
import enviar_email


arquivo_teste = sys.argv[1]


if __name__ == '__main__':

    # Calcular pagamentos
    aluno = valor_modulo.tratar_nome_aluno()
    valor_modulo.executar_valor_modulo(aluno)

    # Analisar pagamentos para autorizar a entrega
    disparar_email = autorizar_entrega.executar_autorizar_entrega()

    # Enviar e-mail
    if disparar_email:  # Se algum item puder ser entregue, disparar o e-mail de aviso.
        enviar_email.enviar_email()

    os.remove('dados_aluno.json')  # Apagar o arquivo do aluno depois do uso.
