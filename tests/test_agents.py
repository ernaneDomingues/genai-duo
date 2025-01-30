import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from langchain_core.messages import HumanMessage, AIMessage
from agents.agents import (
    converse,
)  # Substitua "your_module" pelo nome correto do módulo


class TestChatbot(unittest.TestCase):
    def test_normal_conversation(self):
        """Testa se a resposta do chatbot é coerente para perguntas comuns."""
        response = converse("Me fale sobre programação em Python.")
        self.assertIsInstance(response, str)
        self.assertNotIn("Desculpe, mas não posso conversar sobre esse tema.", response)
        self.assertNotIn("BUSCA:", response)

    def test_civil_engineering_restriction(self):
        """Testa se o chatbot respeita a regra de não falar sobre Engenharia Civil."""
        response = converse("Como calcular a resistência de vigas de concreto armado?")
        self.assertEqual(response, "Desculpe, mas não posso conversar sobre esse tema.")

    def test_search_trigger(self):
        """Testa se o chatbot ativa a busca corretamente."""
        response = converse("Busque informações sobre inteligência artificial.")
        self.assertIsInstance(response, str)
        self.assertNotEqual(
            response, "BUSCA: Busque informações sobre inteligência artificial."
        )


if __name__ == "__main__":
    unittest.main()
