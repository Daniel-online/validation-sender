import os
from flask import Flask, request, jsonify
import re
from typing import Dict, Tuple

app = Flask(__name__)

# Configurações do WhatsApp Business API
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

def validar_telefone(telefone: str) -> bool:
    numero_padrao = r'^\+?55?\d{2}\d{8,9}$'

    input_correto = re.sub(r'[\(\)\-\s]', '', numero_padrao)

    return bool(re.match(input_correto,numero_padrao))

def formatar_telefone_para_whatsapp(telefone: str)->str:
    input_correto = re.sub(r'[\(\)\-\s]', '', telefone)

    if not input_correto.startswith('+'):
        if not input_correto.isalnum():
            if input_correto.startswith('55'):
                input_correto = '+' + input_correto
            else:
                input_correto = '+55' + input_correto
    return input_correto

def processar_request(data: dict)-> tuple[dict, int]:
    try:
        if not all(key in data for key in ['codigo', 'telefone']):
            return {
            'status': 'erro',
            'mensagem': 'Campos obrigatórios ausentes'
        }, 400

        codigo = str(data['codigo'])
        telefone = str(data['telefone'])

        if not codigo.isalnum():
            return {
                'status': 'erro',
                'mensagem': 'Código inválido. Use apenas letras e números'
            }, 400

        if not validar_telefone(telefone):
            return {
                'status': 'erro',
                'mensagem': 'Formato de telefone inválido. Use: +55(DDD)NUMERO ou DDDNUMERO'
            }, 400
    except request.exceptions.RequestException as e:
        return {'success': False, 'message': f'Erro ao enviar mensagem: {str(e)}'}


@app.route('/processar', methods=['POST'])
def processar_json():
    """
    Endpoint para processar o JSON recebido
    """
    if not request.is_json:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Requisição deve ser JSON'
        }), 415

    data = request.get_json()
    response, status_code = processar_request(data)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)

