from langchain_cohere import CohereEmbeddings
import os
from dotenv import load_dotenv
from config.settings import settings


def get_embedding():
    load_dotenv()
    
    try:
        embeddings = CohereEmbeddings(
            cohere_api_key=os.environ['COHERE_API_KEY'], 
            model=settings.cohere_embedding_settings.model
        )
        return embeddings
    except Exception as e:
        print(f"Error initializing embeddings: {e}")
        return None