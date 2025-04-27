# validation-sender

# 📧 API de Envio de Código por Email

Simple **Flask** API for verification code sending by email (for auth). It validates the passed **email** and **code**, then sends an email respons via **SMTP**.

---

## 🚀 Tecnologias usadas

- Python 3.x
- Flask
- SMTP (smtplib)
- dotenv 

---

## 📦 Instalação

1. Clone the directory:

```bash
git clone https://github.com/Daniel-online/validation-sender.git
cd validation-sender
```

2. Start virtual envirnoment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Setup `.env`in project's root similar to this config:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seuemail@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
```

> ⚠️ Atenção: gmail requires special setup from the Google account.

---

## 🛠️ Uso

Init Flask server:

```bash
python app.py
```

Go to: `http://localhost:5000`

---

## 📮 Endpoint

### `POST /enviar-codigo`

 Recebe um `email` e um `codigo` no corpo da requisição e envia o código para o email informado.

#### Corpo da Requisição (JSON):

```json
{
  "email": "usuario@example.com",
  "codigo": "123456"
}
```

#### Possible Responses (in Portuguese):

| Código HTTP | Resposta | Descrição |
|:-----------:|:--------:|:--------- |
| 200 | Código enviado com sucesso | Email enviado corretamente |
| 400 | Erro de validação | Campos obrigatórios faltando ou inválidos |
| 415 | Erro de tipo | Requisição não é JSON |
| 500 | Erro interno | Problemas ao enviar o email |

---

## 🔒Implemented validations

- `email` must be ina valid format.
- `codigo`is **alphanumeric**.
- both field are required (non null).

---

## 🧹 Future updates

- Add sending limit for IP/email to avoid spam.
- Build a better email template.
- API's internationalization.
- Setup async fixes.

---

## 📄 Licence

Este projeto está sob a licença [MIT](LICENSE).
