import os
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from routes.routes import api_bp, chat_bp

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


def create_app():
    """
    Função para criar e configurar a aplicação Flask.
    """

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")
    app.config["DEBUG"] = os.getenv("DEBUG", "True") == "True"

    # Registrar Blueprints para modularizar a API
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(chat_bp)

    CORS(app, origins=os.getenv("CORS_ORIGINS", "*"))

    @app.after_request
    def add_hsts_header(resp):
        if request.is_secure:
            resp.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        return resp

    @app.route("/health")
    def health():
        return "OK"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
