# Analisador de Investimentos com IA (Diagrama do Cerrado)

Este projeto automatiza a avaliação de ativos (Ações e Fundos Imobiliários) com base nos critérios estabelecidos pelo "Diagrama do Cerrado". A ferramenta utiliza a inteligência artificial do **Google Gemini (flash)** aliada ao **Google Search Grounding**, o que significa que ela pesquisa os dados na internet em tempo real para responder cada critério de forma fundamentada e estruturada.

## 🚀 Arquitetura e Decisões Técnicas

Em vez de criarmos *web-scrapers* tradicionais (que frequentemente quebram devido a proteções como o Cloudflare em sites como StatusInvest, Investidor10, etc.), adotamos o moderno **SDK `google-genai`**. Essa abordagem apresenta diversas vantagens:
- **Resiliência**: Sem elementos HTML *hard-coded* para extrair dados.
- **Validação com Pydantic**: A ferramenta obriga o Gemini a retornar um objeto JSON validado contendo estritamente as respostas esperadas (`Sim` ou `Não`), prevenindo alucinações.
- **Busca em Tempo Real (Grounding)**: O modelo de IA faz a pesquisa diretamente na web antes de gerar as respostas, garantindo dados (como DY, ROE, P/VP) atualizados.

## 📦 Estrutura do Projeto

```text
├── main.py                # Script de execução principal
├── requirements.txt       # Dependências do Python
├── .env.example           # Exemplo do arquivo de variáveis de ambiente
├── src/                   # Código fonte principal
│   ├── __init__.py        
│   ├── analyzer.py        # Lógica de integração com API do Gemini (Search + Structured Output)
│   ├── data.py            # Perguntas, critérios e filtros por diagrama 
│   └── models.py          # Modelos de dados usando Pydantic (validação estrutural)
```

## 🛠️ Passo a Passo para Executar

### 1. Pré-requisitos
- Ter o **Python 3.10+** instalado em seu sistema operativo Windows (`python --version`).
- Obter uma API Key do Google Gemini.

### 2. Criando Conta e Obtendo a API Key (Gratuito)
1. Acesse o [Google AI Studio](https://aistudio.google.com/).
2. Faça login com sua conta do Google.
3. No painel, clique em **"Get API Key"** e depois em **"Create API Key em novo projeto"**.
4. Copie a chave gerada.

### 3. Configurando o Ambiente

Abra o PowerShell na pasta do projeto e execute os comandos:

```powershell
# Criação do ambiente virtual (recomendado)
python -m venv venv
.\venv\Scripts\activate

# Instalação das dependências
pip install -r requirements.txt

# Configuração da variável de ambiente
cp .env.example .env
```

Após copiar o `.env.example`, abra o arquivo `.env` com um editor de texto e insira a chave que você gerou no AI Studio:
```env
GEMINI_API_KEY="AIzaSy_SUA_CHAVE_AQUI"
```

### 4. Executando o Script
Com o ambiente ativado e configurado, rode o projeto:
```powershell
python main.py
```

Siga os prompts da tela:
1. Informe o **Ticker** do ativo (ex: `WEGE3`, `ITUB3`, `MXRF11`, `HGLG11`).
2. Escolha o grupo de análise digitando o número correspondente (`investimentos-imobiliarios` ou `diagrama-do-cerrado`).
3. Aguarde o fim da análise. O log aparecerá na tela e o modelo detalhado será salvo em JSON na raiz do projeto (ex: `resultado_WEGE3.json`).

## 🔮 Possíveis Melhorias para o Futuro

- **Cache de Pesquisa**: Implementar um sistema de banco de dados simples (SQLite) para consultar dados que foram buscados muito recentemente, evitando gastar tempo de pesquisa e requisições para o mesmo ativo no mesmo dia.
- **Interface Gráfica (Web)**: Converter esse script para uma aplicação web usando frameworks leves e reativos (como FastAPI no backend e Vue.js/React no frontend).
- **Processamento em Lote**: Permitir ao usuário fazer upload de uma base de tickers (CSV) ou fornecer uma lista para analisar uma carteira inteira de uma vez só.
- **Histórico Comparativo**: Armazenar arquivos `.json` das avaliações do mesmo ativo ao longo dos meses para identificar se o ativo teve melhora ou piora nas suas notas do Diagrama.

## 🤝 Contribuição e Licença
Feito como uma ferramenta auxiliar para gestão e escolha de ativos fundamentadas. Código limpo e modelagem focada em IA Resiliente.
