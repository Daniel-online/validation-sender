from flask import Flask, request, jsonify
import re
app = Flask(__name__)

def validar_telefone(telefone: str) -> bool:
    numero_padrao = r'^\+?55?\d{2}\d{8,9}$'

    input_usuario = re.sub(r'[\(\)\-\s]', '', numero_padrao)

    return bool(re.match(input_usuario,numero_padrao))

def process_request(data: dict)-> tuple[dict, int]:

    return

