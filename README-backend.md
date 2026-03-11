# Enrich Investments - Backend API

Esta é a API central responsável por orquestrar análises financeiras através do **Modelo Gemini (Google AI)**.

## Tecnologias Principais
*   **Servidor e Framework**: FastAPI
*   **Banco de Dados**: MongoDB (Motor Async)
*   **Segurança e Autenticação**: Google OAuth2 + JWT Customizado
*   **Testes**: Pytest

## Como Rodar Localmente

1. Suba para raiz do projeto: `cd enrich-investments`
2. Crie e ative um ambiente virtual:
   *   Windows: `python -m venv venv` e depois `venv\Scripts\Activate.ps1`
   *   Linux/Mac: `python3 -m venv venv` e `source venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Crie um arquivo `.env` na raiz, copiando o modelo de `.env.example`.
   *   Você precisará de uma string de conexão com o MongoDB Atlas.
   *   Gere a `SECRET_KEY` executando no terminal: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
   *   Cole o Client ID do Google OAuth2 lá.
5. Inicie o servidor em modo de desenvolvimento:
   ```bash
   uvicorn src.api.main:app --reload
   ```

A API estará rodando em `http://localhost:8000`.
A documentação interativa OpenAPI (Swagger) estará em: `http://localhost:8000/docs`.

## Estrutura do Banco de Dados
A API gerenciará automaticamente as seguintes coleções (`Collections`) no database `enrich_investments`:
*   `users`: Perfis, emails e chaves de API encriptadas.
*   `questions`: Banco de perguntas customizadas atreladas a cada usuário.
*   `processings`: Todos os históricos de análises do Gemini.
*   `tickers`: Cache local da B3 (Ações e FIIs) com auto-rotate semanal.

## Deployment (GCP Cloud Run)
A aplicação está conteinerizada (`Dockerfile` presente). Se quiser realizar o deploy para o Google Cloud Run:

1. Autentique na gcloud: `gcloud auth login`
2. Configure seu projeto: `gcloud config set project SEU_PROJETO`
3. Envie o código com Buildpacks ou construa localmente e faça o push:
   ```bash
   gcloud builds submit --tag gcr.io/SEU_PROJETO/enrich-api
   ```
4. Implante no Cloud Run:
   ```bash
   gcloud run deploy enrich-api --image gcr.io/SEU_PROJETO/enrich-api --platform managed --allow-unauthenticated
   ```
5. *(Opcional)*: Não se esqueça de preencher os "Secrets/Environment Variables" diretamente na interface do Cloud Run após subrir a imagem, copiando do seu `.env`.
