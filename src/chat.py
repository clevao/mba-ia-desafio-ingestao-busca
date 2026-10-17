import argparse
import os
import ssl
import httpx
import truststore
from search import search_prompt
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")


def main(query):
    print("Iniciando o chat com a pergunta:", query)


    tls_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    http_client = httpx.Client(verify=tls_context)
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"),
        http_client=http_client,
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    results = store.similarity_search_with_score(query, k=10)
    context = "\n\n".join(doc.page_content.strip() for doc, _ in results)
    
    chain = search_prompt(query, context)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    result = chain.invoke({})
    print(f"Resposta do modelo: {result.content}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask a question about the ingested PDF.")
    parser.add_argument("--question", help="Question to ask")
    args = parser.parse_args()

    question = args.question or input("Digite sua pergunta: ")
    main(question)