# Use a imagem oficial do Python 3.12
FROM python:3.12-slim

# Define o diretório de trabalho no container
WORKDIR /whatsapp_code_sender

# Copia os arquivos de requisitos primeiro (boa prática para cache)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Expõe a porta que a aplicação usa
EXPOSE 5000

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para executar a aplicação
CMD ["python", "app.py"]