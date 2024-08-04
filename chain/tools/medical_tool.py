from langchain.tools import BaseTool
from helper.similarity_search import get_retriever
from langsmith import traceable
from config.settings import settings

class MedicalTool(BaseTool):
    name= settings.medical_tool_settings.name
    description=settings.medical_tool_settings.description

    @traceable
    def _run(self, query: str):
        print("Running medical tool")
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