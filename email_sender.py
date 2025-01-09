from flask import Flask, request, jsonify
import re
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Tuple
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do email
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

if not EMAIL_USER or not EMAIL_PASSWORD:
    raise ValueError("Environment variables EMAIL_USER and EMAIL_PASSWORD must be set.")

def validate_email(email: str) -> bool:
    """
    Valida o formato do email usando regex
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def send_email(to_email: str, code: str) -> Dict:
    """
    Envia email usando SMTP
    """
    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = 'Seu Código de Verificação'

        # Corpo do email
        body = f"""
        <html>
          <body>
            <h2>Código de Verificação</h2>
            <p>Seu código é: <strong>{code}</strong></p>
            <p>Este código é válido por 10 minutos.</p>
            <p>Se você não solicitou este código, por favor ignore este email.</p>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))

        # Conectar ao servidor SMTP
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        
        # Enviar email
        text = msg.as_string()
        server.send_message(msg)
        server.quit()
        
        return {'success': True, 'message': 'Email enviado com sucesso'}
        
    except Exception as e:
        return {'success': False, 'message': f'Erro ao enviar email: {str(e)}'}

def process_request(data: Dict) -> Tuple[Dict, int]:
    """
    Processa a requisição e envia o código por email
    """
    try:
        # Validar campos obrigatórios
        if not all(key in data for key in ['codigo', 'email']):
            return {
                'status': 'erro',
                'mensagem': 'Campos obrigatórios ausentes. Necessário: codigo e email'
            }, 400

        codigo = str(data['codigo'])
        email = str(data['email'])

        # Validar código
        if not codigo.isalnum():
            return {
                'status': 'erro',
                'mensagem': 'Código inválido. Use apenas letras e números'
            }, 400

        # Validar email
        if not validate_email(email):
            return {
                'status': 'erro',
                'mensagem': 'Formato de email inválido'
            }, 400

        # Enviar email
        email_result = send_email(email, codigo)
        
        if not email_result['success']:
            return {
                'status': 'erro',
                'mensagem': email_result['message']
            }, 500

        return {
            'status': 'sucesso',
            'mensagem': 'Código enviado com sucesso para o email'
        }, 200

    except Exception as e:
        return {
            'status': 'erro',
            'mensagem': f'Erro interno: {str(e)}'
        }, 500

@app.route('/enviar-codigo', methods=['POST'])
def enviar_codigo():
    """
    Endpoint para processar o JSON e enviar código por email
    """
    if not request.is_json:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Requisição deve ser JSON'
        }), 415

    data = request.get_json()
    response, status_code = process_request(data)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)