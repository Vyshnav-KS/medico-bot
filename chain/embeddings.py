from langchain_cohere import CohereEmbeddings
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

async def get_embedding():
    try:
        embeddings = CohereEmbeddings(
            cohere_api_key=os.environ['COHERE_API_KEY'], 
            model="embed-english-light-v3.0"
        )
        return embeddings
    except Exception as e:
        st.error(f"Error initializing embeddings: {e}")
        return None