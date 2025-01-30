import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from unittest import mock
from flask import Flask, json
from routes.routes import api_bp, chat_bp


class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.app = Flask(__name__, template_folder="../templates")
        self.app.register_blueprint(api_bp, url_prefix="/api")
        self.app.register_blueprint(chat_bp)
        self.client = self.app.test_client()

    def test_index_route(self):
        """Testa se a rota index retorna o template correto."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_ask_route_valid(self):
        """Testa se a rota /api/ask responde corretamente a uma pergunta válida."""
        response = self.client.post(
            "/api/ask",
            data=json.dumps({"question": "Qual é a capital da França?"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", response.get_json())

    def test_ask_route_invalid(self):
        """Testa se a rota /api/ask retorna erro quando a pergunta está vazia."""
        response = self.client.post(
            "/api/ask",
            data=json.dumps({"question": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "A pergunta é obrigatória"})

    def test_ask_route_exception_handling(self):
        """Testa se a rota /api/ask lida corretamente com exceções."""
        with mock.patch(
            "agents.agents.converse", side_effect=Exception("Erro interno")
        ):
            response = self.client.post(
                "/api/ask",
                data=json.dumps({"question": "Teste de erro"}),
                content_type="application/json",
            )
            self.assertEqual(
                response.get_json(), {"answer": "Desculpe, não entendi sua pergunta."}
            )


if __name__ == "__main__":
    unittest.main()
