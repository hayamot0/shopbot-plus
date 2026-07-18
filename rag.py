
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import PINECONE_INDEX
from dotenv import load_dotenv

load_dotenv()

def load_rag_pipeline():
    embeddings=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",task_type="retrieval_query")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
    vectorstore = PineconeVectorStore.from_existing_index(
    index_name=PINECONE_INDEX,
    embedding=embeddings
)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    template="""
    You are a helpful customer support assistant for ShopBot, an online clothing store.
    1. Use ONLY the following pieces of retrieved context to answer the question.
    2. If the answer is not in the context, say "Specifications for this query are unavailable."
    3. If the user is just greeting you (like saying "Hi" or "Hello"), respond politely as the shop's representative without looking at the context.
    ---
    context:
    {context}
    ---
    user question:
    {question}
    """

    prompt=ChatPromptTemplate.from_template(template)

    chain=(
            {"context":retriever,"question":RunnablePassthrough()}
            |prompt
            |llm
            |StrOutputParser()
        )
    return chain




