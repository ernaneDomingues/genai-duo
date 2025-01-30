# GenAI Project - Assistente Conversacional com Flask e Kubernetes

Este projeto é um assistente conversacional baseado em Flask e integrado com Google Gemini AI. Ele possui suporte a buscas inteligentes via Tavily Search e está preparado para deploy em Docker e Kubernetes.

## 📌 Estrutura do Projeto

```
genai-project/
│   ├── templates/              # Templates HTML do front-end
│   ├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   ├── agents/                 # Lógica dos agentes conversacionais
│   │   ├── agents.py           # Configuração do chatbot e integração com Gemini AI
│   ├── routes/                 # Definição das rotas da API
│   │   ├── routes.py           # Configuração das rotas para interação com o chatbot
│   ├── logs/                    # Arquivos de logs
│   ├── app.py                  # Inicialização do app Flask e configuração geral
│   ├── requirements.txt        # Dependências do projeto
│   ├── Dockerfile              # Configuração do container Docker
│   ├── k8s/                    # Configurações para Kubernetes
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   ├── aws-architecture.png    # Arquitetura do projeto na AWS
│   ├── .env.example            # Exemplo do arquivo de variáveis de ambiente
│   └── README.md               # Documentação do projeto
```

---

## 🔎 Explicação dos Principais Arquivos

### `agents.py`
Este arquivo contém a implementação do agente conversacional. Ele integra a API do Google Gemini AI para fornecer respostas inteligentes e usa o Tavily Search para buscas na web. Também define a lógica do fluxo de conversa e a moderação de conteúdo sensível.

### `routes.py`
Define as rotas da API do Flask. Contém:
- `/`: Rota para exibir a interface do chatbot.
- `/api/ask`: Rota para receber perguntas e retornar respostas usando o agente conversacional.

### `app.py`
Arquivo principal para inicializar o Flask. Ele:
- Configura as blueprints das rotas.
- Carrega variáveis de ambiente.
- Configura CORS.
- Implementa verificações de saúde (`/health`).
- Garante segurança com HSTS quando usando HTTPS.

---

## 🚀 Configuração e Execução do Projeto

### 1️⃣ Pré-requisitos
- **Python 3.10+**
- **Docker & Docker Compose**
- **Kubernetes & Kubectl (para deploy em K8s)**
- **Google Gemini API Key**
- **Tavily API Key**

### 2️⃣ Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```
GEMINI_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
SECRET_KEY=your_secret_key
CORS_ORIGINS=*
```

### 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Rodar Localmente

```bash
python app.py
```

Acesse a interface no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 5️⃣ Executar com Docker

**Construir a imagem:**
```bash
docker build -t flask-app .
```

**Rodar o container:**
```bash
docker run -d -p 5000:5000 --name flask-container flask-app
```

**Logs o container:**
```bash
docker logs -f flask-container
```


### 6️⃣ Deploy no Kubernetes

**Aplicar os arquivos de configuração:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml  # Opcional
```

**Verificar os pods:**
```bash
kubectl get pods
```

### 7️⃣ Testar API

```bash
curl -X POST http://localhost:5000/api/ask -H "Content-Type: application/json" -d '{"question": "O que é Machine Learning?"}'
```

Saída esperada:
```json
{
  "answer": "Machine Learning é um campo da inteligência artificial que ..."
}
```

---

## 📜 Licença
Este projeto é open-source e segue a Apache License.

---

👨‍💻 **Desenvolvido por Ernane Domingues** 🚀

