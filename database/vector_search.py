from langchain_pinecone import PineconeVectorStore
from chain.embeddings import get_embedding
from dotenv import load_dotenv


# Retrieve relevant documents based on the query
def get_retriever(query):
    load_dotenv()
    index_name = 'medulla'

    try:
        # cohere embedding
        embeddings = get_embedding()
        docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        
        # similarity search
        print("Similarity search initiated...")
        vdb_results = docsearch.similarity_search(query, k=4)
        
        return vdb_results

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return "Error retrieving documents."

