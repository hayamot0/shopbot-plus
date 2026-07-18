import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_INDEX = os.getenv("PINECONE_INDEX")
