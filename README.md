# 📧 Email Analyzer AI – Desafio AutoU

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
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
- [Solução de Problemas](#-solução-de-problemas)
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
autou-desafio/
│   ├── backend/
│   │   ├── controller/
│   │   │   └── analize_controller.py
│   │   ├── core/
│   │   │   └── config.py
│   │   │   └── exceptions.py
│   │   ├── models/
│   │   │   └── email_schema.py
│   │   ├── prompts/
│   │   │   └── email_analysis_prompt.py
│   │   ├── services/
│   │   │   ├── ai_executor_service
│   │   │   ├── ai_interface.py
│   │   │   ├── openai_executor.py
│   │   │   ├── mock_executor.py
│   │   │   ├── mock_ai_service.py
│   │   │   └── factory.py
│   │   ├── tests/
│   │   │   ├── test_analyze_email_usecase.py
│   │   │   ├── test_analyze_endpoint.py
│   │   │   └── test_mock_executor.py
│   │   ├── usecases/
│   │   │   └── analyze_email_usecase.py
│   │   ├── utils/
│   │   │   └── file_reader.py
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── .env.example
│   └── frontend/
│       │   ├── public/
│       │   ├── index.html
│       │   ├── styles.css
│       │   └── script.js
│       ├── Dockerfile
|       └── nginx.conf
├── docker-compose.yml
├── README.md
```

## ⚙️ Tecnologias Utilizadas

### Backend

- **Python 3.14.2**  
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

- Python 3.14
- Navegador web moderno
- Docker e Docker Compose (opcional)

---

### Método 1: Execução Rápida Usando Docker (Recomendado)

#### Passo 1: Clonar o repositório

Execute os comandos abaixo no terminal:

```
git clone https://github.com/MarcusCastilhos/AutoU-Desafio.git
cd autou-desafio
```

#### Passo 2: Rodar o comando docker

```
docker-compose up --build
```

#### Passo 3: Acessar

- Documentação Swagger: http://localhost:8000/docs
- Pagina Web: http://localhost:3000

### Método 2: Rodar Local

#### Passo 1: Clonar o repositório

Execute os comandos abaixo no terminal:

```
git clone https://github.com/MarcusCastilhos/AutoU-Desafio.git
cd autou-desafio
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
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

#### Passo 3: Iniciar o Frontend

Em outro terminal, volte para a raiz do projeto:

```
cd ..
```

Acesse a pasta do frontend:

```
cd frontend/public
```

Sirva os arquivos estáticos:

```
python -m http.server
```

#### Passo 4: Acessar a aplicação

- Documentação Swagger: http://localhost:8000/docs
- Frontend: http://localhost:8000

---

## 📖 Como Usar

### 1. Análise de Texto Direto

- Acesse http://localhost:8000
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
python -m pytest tests/ -v
```

### Para Testes Com Docker

```
docker compose exec backend pytest
```

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

## 🙏 Agradecimentos

- Equipe AutoU pelo desafio técnico
