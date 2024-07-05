from langchain_cohere import CohereEmbeddings
import os
from dotenv import load_dotenv


def get_embedding():
    load_dotenv()
    
    try:
        embeddings = CohereEmbeddings(
            cohere_api_key=os.environ['COHERE_API_KEY'], 
            model="embed-english-light-v3.0"
        )
        return embeddings
    except Exception as e:
        print(f"Error initializing embeddings: {e}")
        return None