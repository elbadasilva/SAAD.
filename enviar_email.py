import smtplib
from email.message import EmailMessage
from autorizar_entrega import ler_dados_aluno

dados_aluno = ler_dados_aluno()


def enviar_email():

    REMETENTE = 'saad.modulos@gmail.com'
    PASSWORD = 'ltdnwlofbvoifvjb'
    DESTINATARIO = dados_aluno["email_aluno"]
    MAIL_SERVER = "smtp.gmail.com"
    PORT = 465

    message = EmailMessage()
    message.set_content("Prezado(a) Responsável,\nHá módulos disponíveis para retirada.\n\nAtenciosamente,\nA Direção.")
    message["Subject"] = "Módulos disponíveis para retirada"
    message["From"] = REMETENTE
    message["To"] = DESTINATARIO

    try:
        server = smtplib.SMTP_SSL(MAIL_SERVER, PORT)

        server.login(REMETENTE, PASSWORD)
        server.sendmail(REMETENTE, DESTINATARIO, message.as_string())

        server.quit()
    except Exception as erro:
        print("Ocorreu um erro ao enviar o e-mail.")
        print(erro)

if __name__ == '__main__':
    enviar_email()
