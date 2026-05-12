# Envio Automático de E-mails com Anexos

Automação em Python que compacta pastas de clientes em arquivos ZIP e envia um e-mail personalizado para cada um — com o ZIP anexado.

> Desenvolvido para reduzir o envio mensal de kits de prestação de contas de mais de 15 horas para cerca de 10 minutos.

---

## O que o script faz

1. Lê a pasta do mês definida em `PATH_FOLDER`
2. Para cada subpasta de cliente, cria um arquivo `KIT MES ANO - CLIENTE.zip`
3. Carrega a planilha `lista_emails.xlsx` com os e-mails cadastrados
4. Envia o ZIP por e-mail para cada cliente encontrado na planilha

---

## Estrutura de pastas esperada

O `PATH_FOLDER` deve apontar para uma pasta organizada assim:

```
2026/
└── 02 - FEVEREIRO/          ← PATH_FOLDER aponta aqui
    ├── NOME DO CLIENTE A/
    │   ├── documento1.pdf
    │   └── documento2.pdf
    ├── NOME DO CLIENTE B/
    │   └── documento1.pdf
    └── ...
```

O mês (`FEV`) e o ano (`26`) são extraídos automaticamente do caminho da pasta.

---

## Pré-requisitos

- Python 3.10+
- Conta de e-mail com SMTP habilitado (padrão: Office 365)
  - Para contas Microsoft, use uma [App Password](https://support.microsoft.com/account-billing/manage-app-passwords-for-two-step-verification)

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/envio_emails_git.git

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Crie o arquivo de configuração
cp .env.example .env
```

---

## Configuração

Edite o arquivo `.env` com suas informações:

| Variável          | Obrigatória | Descrição                                                              |
|-------------------|-------------|------------------------------------------------------------------------|
| `PATH_FOLDER`     | Sim         | Caminho completo para a pasta do mês                                   |
| `SENDER_EMAIL`    | Sim         | E-mail que aparece como remetente                                      |
| `LOGIN_EMAIL`     | Sim         | E-mail usado para autenticar no SMTP                                   |
| `LOGIN_PASSWORD`  | Sim         | Senha ou App Password                                                  |
| `BODY_MESSAGE`    | Sim         | Corpo do e-mail (suporta HTML)                                         |
| `LISTA_EMAILS`    | Não         | Caminho para o xlsx (padrão: `exemplo/lista_emails_exemplo.xlsx`)      |
| `CC_EMAILS`       | Não         | E-mails em cópia, separados por `;`                                    |
| `SMTP_SERVER`     | Não         | Servidor SMTP (padrão: `smtp.office365.com`)                           |
| `SMTP_PORT`       | Não         | Porta SMTP (padrão: `587`)                                             |

---

## Planilha de e-mails

Crie um arquivo `lista_emails.xlsx` com duas colunas:

| CLIENTE             | EMAIL                                  |
|---------------------|----------------------------------------|
| NOME DO CLIENTE A   | email@cliente.com                      |
| NOME DO CLIENTE B   | email1@cliente.com; email2@cliente.com |

- O nome do cliente deve ser **idêntico** ao nome da pasta
- Múltiplos e-mails são separados por `;`
- Clientes sem e-mail cadastrado são pulados (uma mensagem é exibida no console)

Veja o arquivo de exemplo em [`exemplo/lista_emails_exemplo.xlsx`](exemplo/lista_emails_exemplo.xlsx).

---

## Uso

```bash
python envio_automatico.py
```

Exemplo de saída:

```
Arquivos de ACME COMERCIO LTDA compactados em: ...
Arquivos de BETA RESTAURANTE compactados em: ...
E-mail enviado para ACME COMERCIO LTDA com email: ['financeiro@acmecomercio.com']
E-mail enviado para BETA RESTAURANTE com email: ['adm@betarestaurante.com.br']
ZIP não encontrado para SIGMA ACADEMIA, pulando.
```

---

## Testando localmente

O repositório já inclui uma estrutura de exemplo com dados fictícios em `exemplo/relatorios/`:

```
exemplo/relatorios/
└── 2026/
    └── 01 - JANEIRO/
        ├── ACME COMERCIO LTDA/
        ├── BETA RESTAURANTE/
        ├── GAMA INDUSTRIA SA/
        ├── DELTA LAVANDERIA/
        └── SIGMA ACADEMIA/
```

Para usar, basta configurar o `.env` com os caminhos já incluídos no repositório:

```env
PATH_FOLDER=exemplo/relatorios/2026/01 - JANEIRO
LISTA_EMAILS=exemplo/lista_emails_exemplo.xlsx
```

E então executar:

```bash
python envio_automatico.py
```

