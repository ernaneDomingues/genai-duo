# GenAI Duo - Assistente Conversacional com Flask e Kubernetes

## 📌 Visão Geral
Este é um projeto Flask baseado em **LLMs (Large Language Models)** que utiliza a API do **Google Gemini** para conversas inteligentes e a **Tavily Search API** para buscas na web. A aplicação é escalável e pode ser implantada na **AWS** usando **Kubernetes (EKS)**.


## 🌍 Acessando o Chat no Heroku

O projeto foi implantado no Heroku para testes. Para experimentar, basta acessar o link abaixo:

[GenAI Duo - Heroku](https://genai-duo-56838a644146.herokuapp.com/)


## 📂 Estrutura do Projeto

```
genai-duo/
│   ├── templates/              # Templates HTML do front-end
│   ├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   ├── agents/                 # Lógica dos agentes conversacionais
│   │   ├── agents.py           # Configuração do chatbot e integração com Gemini AI
│   ├── routes/                 # Definição das rotas da API
│   │   ├── routes.py           # Configuração das rotas para interação com o chatbot
│   ├── logs/                   # Arquivos de logs
│   ├── tests/                  # Arquivos de testes unitários
│   │   ├── test_app.py         # Testes unitários do app.py
│   │   ├── test_routes.py      # Testes unitários do routes.py
│   │   ├── test_agents.py      # Testes unitários do agents.py
│   ├── app.py                  # Inicialização do app Flask e configuração geral
│   ├── requirements.txt        # Dependências do projeto
│   ├── Dockerfile              # Configuração do container Docker
│   ├── k8s/                    # Configurações para Kubernetes
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   ├── .env.example            # Exemplo do arquivo de variáveis de ambiente
│   └── README.md               # Documentação do projeto
```

---

## 📝 Explicação dos Principais Arquivos

### 📌 `agents.py`
- Implementa o **Google Gemini AI** para conversas.
- Usa a **Tavily Search API** para buscas na web.
- Define um fluxo de controle para decidir entre responder diretamente ou realizar uma busca.

### 📌 `routes.py`
- Define **rotas da API** com Flask.
- `POST /api/ask` recebe uma pergunta e retorna uma resposta do agente conversacional.
- `GET /` renderiza a interface do chatbot.

### 📌 `app.py`
- Inicializa o **Flask** e registra as rotas.
- Configura **CORS** e segurança (HSTS).
- Expõe a rota `/health` para verificação de status.

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

### 3️⃣ Configuração Local
1. Clone o repositório:
   ```bash
   git clone https://github.com/ernaneDomingues/genai-duo.git
   cd genai-duo
   ```
2. Mova o arquivo .env para a pasta genai-duo.

3. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # (Linux/macOS)
   venv\Scripts\activate     # (Windows)
   pip install -r requirements.txt
   ```
4. Execute a aplicação Flask:
   ```bash
   python app.py
   ```
5. Acesse no navegador: `http://127.0.0.1:5000`

---

### 4️⃣ Executar com Docker

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


### 5️⃣ Deploy no Kubernetes (EKS)
1. Configure o **kubectl** para acessar o cluster EKS.
2. **Crie os deployments e services:**
   ```bash
   kubectl apply -f k8s/
   ```
3. **Verifique os pods:**
   ```bash
   kubectl get pods
   ```
4. **Exponha o serviço:**
   ```bash
   kubectl port-forward svc/genai-service 5000:5000
   ```

### 6️⃣ Testar API

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

## 🏗️ Arquitetura AWS

A arquitetura do projeto na AWS utiliza **EKS (Elastic Kubernetes Service)** para escalar o Flask e gerenciar os recursos.

### 📌 Componentes:
1. **Usuário → Route 53 + CloudFront**
2. **Aplicação Flask → Amazon EKS**
3. **Banco de Dados → Amazon RDS (PostgreSQL)**
4. **Cache → Amazon ElastiCache (Redis)**
5. **Monitoramento → CloudWatch**
6. **CI/CD → CodePipeline + ECR**

```
          [ Usuário ]
              │
       ┌─────▼──────┐
       │ Route 53   │
       └─────┬──────┘
             │
       ┌────▼───────┐
       │ CloudFront │
       └─────┬──────┘
             │
       ┌────▼──────┐
       │   EKS    │  (Flask App)
       ├──────────┤
       │   API    │
       └────┬─────┘
            │
     ┌─────▼──────┐
     │ ElastiCache│
     └─────┬──────┘
            │
   ┌────────▼────────┐
   │    RDS (PostgreSQL) │
   └────────────────────┘
            │
     ┌─────▼───────┐
     │ CloudWatch  │  (Logs e Monitoramento)
     └─────────────┘
```

### 🚀 Fluxo de Deploy na AWS
1️⃣ **CodePipeline** recebe mudanças do repositório GitHub/GitLab.
2️⃣ **CodeBuild** cria a imagem Docker e armazena no **Amazon ECR**.
3️⃣ **EKS** atualiza os pods automaticamente.
4️⃣ **CloudWatch** monitora logs e métricas.

---

---

## 📜 Licença
Este projeto é open-source e segue a Apache License.

---

👨‍💻 **Desenvolvido por Ernane Domingues** 🚀

