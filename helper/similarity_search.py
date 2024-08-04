from langchain_pinecone import PineconeVectorStore
from helper.embeddings import get_embedding
from dotenv import load_dotenv
from langsmith import traceable
from config.settings import settings


# Retrieve relevant documents based on the query
@traceable(run_type="retriever")
def get_retriever(query):
    load_dotenv()
    index_name = settings.similarity_search_settings.index_name

    try:
        # cohere embedding
        embeddings = get_embedding()
        docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        
        # similarity search
        print("Similarity search initiated...")
        vdb_results = docsearch.similarity_search(query, k=settings.similarity_search_settings.no_of_samples)
        
        return vdb_results

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return "Error retrieving documents."

