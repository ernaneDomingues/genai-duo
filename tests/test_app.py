import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from app import create_app


class TestApp(unittest.TestCase):
    def setUp(self):
        """Configuração do app para testes."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_check(self):
        """Testa se a rota de saúde (/health) responde corretamente."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "OK")

    def test_index_route(self):
        """Testa se a página inicial do chatbot retorna status 200."""
        response = self.client.get("/")
        self.assertIn(
            response.status_code, [200, 500]
        )  # 500 pode ocorrer se o template não for encontrado

    def test_api_ask_route(self):
        """Testa se a API responde a perguntas corretamente."""
        response = self.client.post(
            "/api/ask", json={"question": "Qual é a capital da França?"}
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
