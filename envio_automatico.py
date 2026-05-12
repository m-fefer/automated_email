import os
import zipfile
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

# ── Configurações ──────────────────────────────────────────────────────────────

pasta_mes       = os.getenv('PATH_FOLDER')
pasta_principal = os.path.dirname(os.path.dirname(pasta_mes))
mes             = pasta_mes.split(' - ')[1][0:3]
ano             = os.path.basename(os.path.dirname(pasta_mes))[-2:]

caminho_lista_emails = os.getenv(
    'LISTA_EMAILS',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lista_emails.xlsx')
)

smtp_server    = os.getenv('SMTP_SERVER', 'smtp.office365.com')
smtp_port      = int(os.getenv('SMTP_PORT', '587'))
sender_email   = os.getenv('SENDER_EMAIL')
login_email    = os.getenv('LOGIN_EMAIL')
login_password = os.getenv('LOGIN_PASSWORD')

# ── Funções ────────────────────────────────────────────────────────────────────

def compacta_pastas(caminho_principal, mes, ano):
    for cliente in os.listdir(caminho_principal):
        caminho_cliente = os.path.join(caminho_principal, cliente)

        if os.path.isdir(caminho_cliente):
            nome_zip    = f'KIT {mes} {ano} - {cliente}.zip'
            caminho_zip = os.path.join(caminho_cliente, nome_zip)

            with zipfile.ZipFile(caminho_zip, 'w') as zipf:
                for root, _, files in os.walk(caminho_cliente):
                    for file in files:
                        arquivo_path = os.path.join(root, file)
                        if arquivo_path == caminho_zip:
                            continue
                        zipf.write(arquivo_path, os.path.relpath(arquivo_path, caminho_cliente))

            print(f'Arquivos de {cliente} compactados em: {caminho_zip}')


def send_email(sender_email, to_email, subject, zip_path, cliente):
    msg            = MIMEMultipart()
    msg['From']    = sender_email
    msg['To']      = ', '.join(to_email)
    msg['Subject'] = subject
    cc_emails      = os.getenv('CC_EMAILS', '').split(';')
    msg['Cc']      = ', '.join(cc_emails)

    msg.attach(MIMEText(os.getenv('BODY_MESSAGE'), 'html'))

    with open(zip_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(zip_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_path)}"'
        msg.attach(part)

    try:
        all_recipients = to_email + cc_emails
        server.sendmail(sender_email, all_recipients, msg.as_string())
        print(f'E-mail enviado para {cliente} com email: {to_email}')
    except Exception as e:
        print(f'Falha no envio para {to_email}: {e}')


# ── Execução ───────────────────────────────────────────────────────────────────

df = pd.read_excel(caminho_lista_emails)

compacta_pastas(pasta_mes, mes, ano)

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(login_email, login_password)

    for _, row in df.iterrows():
        cliente       = row['CLIENTE']
        email_cliente = [e.strip() for e in str(row['EMAIL']).split(';')]

        caminho_cliente = os.path.join(pasta_mes, cliente)
        nome_zip        = f'KIT {mes} {ano} - {cliente}.zip'
        caminho_zip     = os.path.join(caminho_cliente, nome_zip)

        if os.path.exists(caminho_zip):
            assunto = f'KIT - PRESTAÇÃO DE CONTAS | {cliente} | {mes} {ano}'
            send_email(sender_email, email_cliente, assunto, caminho_zip, cliente)
        else:
            print(f'ZIP não encontrado para {cliente}, pulando.')
