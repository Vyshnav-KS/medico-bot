from langchain.tools import BaseTool
import streamlit as st

class ApplicationTool(BaseTool):
    name="Celebrations"
    description="Give response to the user for only on special occasions like birthdays, anniversery etc."

    def _run(self, query: str =""):
        st.balloons()   


application_tool = ApplicationTool()