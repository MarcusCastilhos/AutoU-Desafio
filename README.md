# 📧 Email Analyzer AI – Desafio AutoU

<div align="center">

![Email Analyzer AI](https://img.shields.io/badge/Email%20Analyzer-AI-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Sistema inteligente de análise e classificação automática de emails**

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#️-tecnologias-utilizadas)
- [Instalação e Execução](#-instalação-e-execução)
- [Como Usar](#-como-usar)
- [API Reference](#-api-reference)
- [Testes](#-testes)
- [Configuração](#-configuração)
- [FAQ](#-faq)
- [Solução de Problemas](#-solução-de-problemas)
- [Screenshots](#-screenshots)
- [Melhorias Futuras](#-melhorias-futuras)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 🎯 Visão Geral

Solução desenvolvida para o **Desafio Técnico da AutoU**, com foco na automação da **análise e classificação de emails corporativos**.

O sistema identifica se um email é:

- **Produtivo** → requer ação
- **Improdutivo** → apenas informativo

E gera **respostas automáticas contextualizadas**, utilizando IA ou um serviço mock.

---

## 📁 Estrutura do Projeto

```text
projeto-autou/
├── backend/
│   ├── core/
│   │   └── config.py
│   │   └── exceptions.py
│   ├── models/
│   │   └── email_schema.py
│   ├── routes/
│   │   └── analyze.py
│   ├── services/
│   │   └── ai/
│   │       ├── ai_interface.py
│   │       ├── openai_service.py
│   │       ├── mock_ai_service.py
│   │       └── factory.py
│   ├── tests/
│   │   ├── test_analyze_endpoint.py
│   │   └── test_mock_ai_service.py
│   ├── main.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── frontend/
    ├── index.html
    ├── styles.css
    └── script.js
```

## ⚙️ Tecnologias Utilizadas

### Backend

- **Python 3.11+**  
  Linguagem principal do projeto.

- **FastAPI**  
  Framework web moderno, rápido e com documentação automática.

- **Pydantic**  
  Validação e tipagem de dados.

- **Uvicorn**  
  Servidor ASGI de alta performance.

- **Pytest**  
  Framework de testes automatizados.

- **Python-dotenv**  
  Gerenciamento de variáveis de ambiente.

### Frontend

- **HTML5**  
  Estrutura semântica da aplicação.

- **CSS3**  
  Estilização moderna e responsiva.

- **JavaScript (ES6+)**  
  Interatividade e comunicação com a API.

- **PDF.js**  
  Extração de texto de arquivos PDF no navegador.

- **Fontes Google**  
  Tipografias Inter e JetBrains Mono.

### DevOps

- **Docker**  
  Containerização da aplicação.

- **Docker Compose**  
  Orquestração de serviços.

- **Git**  
  Controle de versão.

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- Navegador web moderno
- Docker e Docker Compose (opcional)

---

### Método 1: Execução Rápida (Recomendado)

#### Passo 1: Clonar o repositório

Execute os comandos abaixo no terminal:

```
git clone https://github.com/seu-usuario/email-analyzer-ai.git
cd email-analyzer-ai
```

#### Passo 2: Iniciar o Backend

Acesse a pasta do backend e prepare o ambiente:

```
cd backend
```

Crie e ative o ambiente virtual:

```
python -m venv venv
```

Linux ou Mac:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

Instale as dependências:

```
pip install -r requirements.txt
```

Inicie o servidor:

```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Passo 3: Iniciar o Frontend

Em outro terminal, volte para a raiz do projeto:

```
cd ..
```

Acesse a pasta do frontend:

```
cd frontend
```

Sirva os arquivos estáticos:

```
python -m http.server 8080
```

#### Passo 4: Acessar a aplicação

- Backend (API): http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Frontend: http://localhost:8080

---

### Método 2: Usando Docker

Na pasta backend, execute:

```
cd backend
docker-compose up --build
```

O frontend pode ser servido com qualquer servidor HTTP simples.  
Exemplo:

```
python -m http.server 8080
```

---

## 📖 Como Usar

### 1. Análise de Texto Direto

- Acesse http://localhost:8080
- Cole o conteúdo do email na caixa de texto
- Clique em **Analisar**
- Veja a categoria e a resposta gerada

### 2. Upload de Arquivo

- Clique em **Carregar arquivo**
- Selecione um arquivo .txt ou .pdf
- Aguarde a extração do texto (para PDFs)
- Clique em **Analisar**

### 3. Histórico de Análises

- Todas as análises são salvas no histórico
- Clique em uma análise para expandir ou contrair
- Visualize o conteúdo original e a resposta
- O histórico persiste durante a sessão

---

## 🔌 API Reference

### Endpoint Principal

```
POST /analyze
Content-Type: multipart/form-data
```

### Exemplo de Requisição

```
curl -X POST http://localhost:8000/analyze
-F "file=@email.txt"
```

### Exemplo de Resposta

```
{
  "category": "Produtivo",
  "response": "Agradecemos seu contato. Iremos analisar sua solicitação."
}
```

### Documentação Interativa

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testes

### Executar Testes do Backend

```
cd backend
pytest -v
```

### Cobertura de Testes

```
pytest --cov=.
```

### Testes Disponíveis

- Teste do endpoint /analyze
- Teste de classificação de emails
- Teste do MockAIService
- Teste de respostas automáticas

---

## 🔧 Configuração

### Modos de IA

#### 1. Mock AI (Padrão)

Não requer configuração e funciona sem internet.

#### 2. OpenAI (Opcional)

Copie o arquivo de exemplo:

```
cp .env.example .env
```

Edite o arquivo .env e configure:

```
AI_PROVIDER=openai
OPENAI_API_KEY=sua-chave-aqui
```

### Variáveis de Ambiente

Backend:

```
PORT=8000
AI_PROVIDER=mock
OPENAI_API_KEY=
```

Frontend:

```
BACKEND_URL=http://localhost:8000
```

---

## ❓ FAQ

**O sistema funciona sem internet?**  
Sim. Por padrão utiliza o MockAIService.

**Posso analisar PDFs protegidos por senha?**  
Não. Apenas PDFs não protegidos.

**Quantas páginas de PDF são suportadas?**  
Até 10 páginas por documento.

**Como limpar o histórico?**  
Atualize a página no navegador.

**Posso usar minha própria chave da OpenAI?**  
Sim, configurando no arquivo .env.

**O projeto possui suporte a Docker?**  
Sim, via docker-compose.

---

## 🐛 Solução de Problemas

### Falha ao conectar ao backend

- Verifique se o backend está rodando em http://localhost:8000/docs
- Confirme a URL no script.js
- Verifique os logs do backend

### PDF não extrai texto

- Confirme que o PDF possui texto selecionável
- Verifique se não está protegido por senha
- Veja erros no console do navegador

### Erro de CORS

- Reinicie o backend
- Limpe o cache do navegador
- Confirme acesso via localhost

---

## 📈 Melhorias Futuras

- Autenticação de usuários
- Persistência de dados (SQLite ou PostgreSQL)
- Exportação de relatórios
- Análise em lote
- Dashboard com métricas
- Suporte a múltiplos idiomas
- Integração com Gmail e Outlook

---

## 🤝 Contribuindo

- Faça um fork do projeto
- Crie uma branch para sua feature
- Commit suas alterações
- Envie para o repositório
- Abra um Pull Request

---

## 📄 Licença

xxx

---

## 👨‍💻 Autor

Marcus Castilhos – Desenvolvedor Full Stack

GitHub: @seu-usuario  
LinkedIn: Seu Perfil  
Email: seu.email@exemplo.com

---

## 🙏 Agradecimentos

- Equipe AutoU pelo desafio técnico
- Comunidade open source
- Todos os contribuidores e testadores
