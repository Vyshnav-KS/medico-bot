from langchain.tools import BaseTool
import streamlit as st

class GeneralTool(BaseTool):
    name="General Tool"
    description="Give response for generic questions."

    return_direct = False
    def _run(self, query: str =""):
        return 


general_tool = GeneralTool()