import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


# CONFIGURAÇÃO FIXA (Opção B)
EMAIL_REMETENTE = "seuemail@gmail.com"
SENHA_APP = "xxxx xxxx xxxx xxxx"   # senha de app do Gmail


def enviar_email_com_anexo(destinatario, assunto, mensagem, anexo_bytes, nome_arquivo):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = destinatario
        msg["Subject"] = assunto

        msg.attach(MIMEText(mensagem, "plain"))

        parte_pdf = MIMEApplication(anexo_bytes, _subtype="pdf")
        parte_pdf.add_header(
            "Content-Disposition",
            "attachment",
            filename=nome_arquivo
        )
        msg.attach(parte_pdf)

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_APP)
        servidor.send_message(msg)
        servidor.quit()

        return True

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False