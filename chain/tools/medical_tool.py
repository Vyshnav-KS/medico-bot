from langchain.tools import BaseTool
from database.vector_search import get_retriever

class MedicalTool(BaseTool):
    name= "Medical Tool"
    description="Returns answer for medical queries, medical-related questions."

    def _run(self, query: str):
        try:
            final_content = ""   

            # Similarity search function from vector database
            vdb_results = get_retriever(query)        
            if vdb_results:
                for content in vdb_results:
                    final_content += content.page_content
                
                print(f"Final content: {final_content[:20]}")
                return final_content

        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return "Error retrieving documents."
        
medical_tool = MedicalTool()