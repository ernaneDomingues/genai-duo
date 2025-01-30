import logging
import os
from typing import TypedDict, List, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import operator
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import sys

# Criar diretório de logs se não existir
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Garante que o diretório de logs existe
LOG_FILE = os.path.join(LOG_DIR, "app.log")  # Define o caminho do arquivo de log

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE),
    ],  # Saída para terminal e arquivo
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",  # Adiciona o encoding UTF-8
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Obtém a chave da API do Gemini
if not GEMINI_API_KEY:
    logging.critical("Erro: GEMINI_API_KEY não está definida no .env")
    raise RuntimeError("Erro: GEMINI_API_KEY não está definida no .env")

# Configuração do modelo Gemini
gemini_chat = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Define o modelo utilizado
    api_key=GEMINI_API_KEY,
    safety_settings={  # Define configurações de segurança para filtrar conteúdos indesejados
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
)

# Configuração da ferramenta de busca
search_tool = TavilySearchResults(
    max_results=10
)  # Define o número máximo de resultados retornados


# Definição do estado do grafo
class GraphState(TypedDict):
    messages: Annotated[
        List[HumanMessage | AIMessage], operator.add
    ]  # Lista de mensagens no fluxo da conversa


# Definição do prompt do chatbot
template = """Você é um assistente conversacional especializado em diversos temas, exceto Engenharia Civil.

**Regras:**
- Se perguntarem sobre Engenharia Civil ou tópicos relacionados, responda EXATAMENTE com: "Desculpe, mas não posso conversar sobre esse tema."
- Se a pergunta indicar que o usuário deseja realizar uma busca (por exemplo, conter palavras como "pesquise", "busque", "encontre informações sobre"), então responda EXATAMENTE com: "BUSCA: <pergunta_original>".
- Se a query estiver incompleta ou não fizer sentido, responda EXATAMENTE com: "Desculpe, não entendi sua pergunta."
- Caso contrário, responda normalmente com base no seu conhecimento geral.

"""
conversational_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("user", "{input}"),  # Inserção do input do usuário no prompt
    ]
)

# Cadeia conversacional combinando o prompt com o modelo Gemini
conversational_chain = conversational_prompt | gemini_chat

# Funções do grafo


def conversational_node(state: GraphState):
    """Nó conversacional que processa a entrada do usuário."""
    user_input = state["messages"][
        -1
    ].content  # Obtém a mensagem mais recente do usuário
    logging.info(f"Entrada do usuário: {user_input}")

    result = conversational_chain.invoke(
        {"input": user_input}
    )  # Obtém a resposta do modelo
    logging.info(f"Resposta do LLM: {result.content}")

    return {"messages": [result]}


def should_search(state: GraphState):
    """Decide se deve acionar a busca com base na resposta do LLM."""
    last_msg = state["messages"][-1].content
    return "True" if last_msg.startswith("BUSCA:") else "False"


def search_node(state: GraphState):
    """Executa a busca e gera uma resposta estruturada com base nos resultados."""
    try:
        query = state["messages"][-1].content.replace("BUSCA: ", "").strip()
        if not query:
            return {
                "messages": [
                    AIMessage(content="Erro: Nenhuma consulta válida para busca.")
                ]
            }

        logging.info(f"Executando busca para: {query}")
        results = search_tool.invoke({"query": query})

        if not results:
            return {
                "messages": [
                    AIMessage(content="Nenhum resultado relevante encontrado.")
                ]
            }

        top_results = "\n\n".join(
            [
                f"\u2022 {r['content']}"
                for r in results[:10]
                if "content" in r and r["content"].strip()
            ]
        )
        if not top_results.strip():
            return {
                "messages": [
                    AIMessage(
                        content="Não foi possível encontrar informações relevantes sobre esse tema."
                    )
                ]
            }

        logging.info(f"Resultados da busca processados para Gemini: {top_results}")
        resposta_final = gemini_chat.invoke(
            f"Resuma as informações sobre {query}: {top_results}"
        )

        return {"messages": [AIMessage(content=resposta_final.content)]}
    except Exception as e:
        logging.error(f"Erro ao processar a busca: {e}")
        return {
            "messages": [
                AIMessage(content="Erro ao processar a busca. Tente novamente.")
            ]
        }


# Construção do grafo
workflow = StateGraph(GraphState)
workflow.add_node("conversacional", conversational_node)
workflow.add_node("busca", search_node)
workflow.set_entry_point("conversacional")
workflow.add_conditional_edges(
    "conversacional", should_search, {"True": "busca", "False": END}
)
workflow.add_edge("busca", END)

# Compilação do grafo
app = workflow.compile()


def converse(input_text: str) -> str:
    """Recebe uma entrada do usuário e processa a resposta."""
    response = app.invoke({"messages": [HumanMessage(content=input_text)]})
    return response["messages"][-1].content


if __name__ == "__main__":
    logging.info("Iniciando testes do chatbot...")
    print(converse("Busque informações sobre inteligência artificial."))
    print(converse("Como calcular a resistência de vigas de concreto armado?"))
    print(converse("Me fale sobre programação em Python."))
