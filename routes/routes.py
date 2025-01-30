from flask import Blueprint, request, jsonify, render_template
from agents.agents import converse

# Criar Blueprints para organizar as rotas da aplicação
api_bp = Blueprint("api", __name__)
chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/")
def index():
    """Rota para renderizar a página principal do chatbot."""
    return render_template("index.html")


@api_bp.route("/ask", methods=["POST"])
def ask():
    """Rota para processar perguntas enviadas pelo usuário.

    input: {"question": "Qual é a capital da França?"}

    output: {"answer": "Paris"}
    """
    try:
        data = request.get_json()

        question = data.get("question", "").strip()
        if not question:
            return jsonify({"error": "A pergunta é obrigatória"}), 400

        answer = converse(question)

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
