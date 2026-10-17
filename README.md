# Desafio MBA Engenharia de Software com IA - Full Cycle


## Configuração do Ambiente

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Subir o banco de dados com Docker**
   ```bash
   docker compose up -d
   ```


3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais
   - Configure a conexão com o banco de dados nas variáveis `DATABASE_URL` e `PG_VECTOR_COLLECTION_NAME`

## Execução dos Scripts

Para as instruções abaixo funcionarem, tem que acessar o diretório `src` no terminal
```bash
cd /src
```

### Ingestão dos dados do PDF


Rode o script `ingest.py`:
```bash
python ingest.py
```

### Chat
1. Rode o script:
```bash
python chat.py
```
2. Digite a sua pergunda no terminal. Ex: `Qual é o fatura da empresa Alfa Energia S.A.`

Uma outra opção é rodar o script passando a pergunta como parâmetro: 
```bash
python chat.py --question="Qual é o fatura da empresa Alfa Energia S.A."
```

#### Exemplo de Interações: 
**Informação existente no contexto**
```bash
(venv)  > python chat.py
Digite sua pergunta: Qual é o faturamento da empresa Alfa Energia S.A.
Iniciando o chat com a pergunta: Qual é o faturamento da empresa Alfa Energia S.A.
Resposta do modelo: O faturamento da empresa Alfa Energia S.A. é R$ 722.875.391,46.
(venv)  > python chat.py
Digite sua pergunta: Qual é o faturament da emprea Alfa Energia Holding
Iniciando o chat com a pergunta: Qual é o faturament da emprea Alfa Energia Holding
Resposta do modelo: O faturamento da empresa Alfa Energia Holding é R$ 858.537,02.
```
**Informação inexistente no contexto**
```bash
(venv)  > python chat.py
Digite sua pergunta: qual é o faturamento da empresa Não Existe S/A
Iniciando o chat com a pergunta: qual é o faturamento da empresa Não Existe S/A
Resposta do modelo: Não tenho informações necessárias para responder sua pergunta.
```