from langchain.tools import BaseTool
from langsmith import traceable
from config.settings import settings

class GeneralTool(BaseTool):
    name=settings.general_tool_settings.name
    description=settings.general_tool_settings.description

    return_direct = False

    @traceable
    def _run(self, query: str):
        print("Running general tool")
        return  query


general_tool = GeneralTool()