from pydantic_settings import BaseSettings

class AzureOpenAISettings(BaseSettings):
    model: str = "gpt-4-1106-preview"
    openai_api_type: str = "azure"

class CohereEmbeddingSettings(BaseSettings):
    model: str = "embed-english-light-v3.0"

class SimilaritySeachSettings(BaseSettings):
    index_name: str = "medulla"
    no_of_samples: int = 5

class GeneralToolSettings(BaseSettings):
    name: str = "GeneralTool"
    description: str = "Give response for generic questions."

class ApplicationToolSettings(BaseSettings):
    name: str = "Celebrations"
    description: str = "Give response to the user for only on special occasions like birthdays, anniversary etc."

class MedicalToolSettings(BaseSettings):
    name: str = "MedicalTool"
    description: str = "Returns answer for medical queries, medical-related questions."

class Settings():
    azure_openai_settings: AzureOpenAISettings = AzureOpenAISettings()
    cohere_embedding_settings: CohereEmbeddingSettings = CohereEmbeddingSettings()
    similarity_search_settings: SimilaritySeachSettings = SimilaritySeachSettings()
    general_tool_settings: GeneralToolSettings = GeneralToolSettings()
    application_tool_settings: ApplicationToolSettings = ApplicationToolSettings()
    medical_tool_settings: MedicalToolSettings = MedicalToolSettings()

settings = Settings()

