# genai-duo

genai-project/
├── app/                        # Pasta principal da aplicação Flask
│   ├── templates/              # Templates HTML do front-end
│   │   ├── index.html          # Página principal da interface
│   ├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/
│   │   │   └── styles.css      # Estilos personalizados
│   │   └── js/
│   │       └── script.js       # Lógica do front-end em JavaScript
│   ├── __init__.py             # Inicialização da aplicação Flask
│   ├── app.py                  # Criação do APP.
│   ├── agents/
│   │   └── agents.py           # Agents de Conversa, Search e Moderation
│   ├── routes/
│   │   └── routes.py           # Rotas para a API
│   └── utils.py                # Funções utilitárias (ex.: validações, logs)
├── requirements.txt            # Dependências do projeto
├── Dockerfile                  # Dockerfile para a aplicação Flask
├── k8s/                        # Arquivos de configuração do Kubernetes
│   ├── deployment.yaml         # Deployment para o Flask
│   ├── service.yaml            # Service para expor a API e front-end
│   └── ingress.yaml            # Configuração de ingress (se necessário)
├── aws-architecture.png        # Diagrama de arquitetura para a AWS
└── README.md                   # Documentação do projeto
