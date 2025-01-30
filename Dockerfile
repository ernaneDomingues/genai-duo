# Usando uma imagem base oficial do Python
FROM python:3.10-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos necessários para o container
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta da aplicação Flask
EXPOSE 5000

# Definir a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando de execução da aplicação
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]