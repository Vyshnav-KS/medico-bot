from langchain.tools import BaseTool
import streamlit as st
from config.settings import settings

class ApplicationTool(BaseTool):
    name=settings.application_tool_settings.name
    description=settings.application_tool_settings.description
    def _run(self, query: str =""):
        print("Application tool")
        st.balloons()   


application_tool = ApplicationTool()