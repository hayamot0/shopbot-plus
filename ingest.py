import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from config import PINECONE_INDEX

load_dotenv()


def populate_index():
    embeddings=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",task_type="retrieval_document")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    loader=DirectoryLoader(os.path.join(BASE_DIR, "knowledge_base/"),glob="*.txt",loader_cls=TextLoader)

    documents=loader.load()

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100,separators=["\n\n", "\n", ".", "،", " "])

    chunks=text_splitter.split_documents(documents)


    PineconeVectorStore.from_documents(
        chunks, 
        embeddings, 
        index_name=PINECONE_INDEX
)


if __name__ == "__main__":
    populate_index()
    print("Pinecone index populated successfully.")