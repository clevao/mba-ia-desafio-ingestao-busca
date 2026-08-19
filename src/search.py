import os
import ssl
import httpx
import truststore

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None, context=""):
    if not question:
        raise RuntimeError("Question must be provided to generate the prompt.")

    question_template = PromptTemplate(
        template=PROMPT_TEMPLATE.format(contexto=context, pergunta=question)
    )

    tls_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    http_client = httpx.Client(verify=tls_context)
    model = ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        temperature=0.5,
        http_client=http_client,
    )

    chain = question_template | model

    return chain