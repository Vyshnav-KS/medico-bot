from pinecone import Pinecone
from openai import OpenAI
# import streamlit as st
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from chain.embeddings import get_embedding
from dotenv import load_dotenv
import asyncio
from langchain_cohere import CohereEmbeddings

load_dotenv()


# Initialize Pinecone client
# def client_init():
#     try:
#         pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

#         index_name = "medulla"

#         # Check if the index already exists
#         if index_name not in pc.list_indexes().names():
#             pc.create_index(
#                 name=index_name,
#                 dimension=384, 
#                 metric="cosine", 
#                 spec=ServerlessSpec(
#                     cloud="aws", 
#                     region="us-east-1"
#                 )
#             )

#         index = pc.Index(index_name)
#         return index_name
#     except Exception as e:
#         st.error(f"Error initializing Pinecone client: {e}")
#         return None

# Retrieve relevant documents based on the query
def get_retriever(query):
    final_content = ""
    # index_name = client_init()
    index_name = 'medulla'

    if not index_name:
        return "Error initializing Pinecone client."

    try:
        # cohere embedding
        embeddings = get_embedding()
        docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        
        # similarity search
        print("Similarity search initiated...")
        vdb_results = docsearch.similarity_search(query, k=4)
        
        if vdb_results:
            for content in vdb_results:
                final_content += content.page_content
        
        print(f"Final content: {final_content[:20]}")
        
        return final_content

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return "Error retrieving documents."

# asyncio.run(get_retriever("Is there any association between smoking and GERD ?"))
