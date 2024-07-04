import streamlit as st
from langchain.agents import Tool
from langchain.tools import BaseTool

def toggle_bot_name(input=""):
    if "app_title" not in st.session_state:
        st.session_state.app_title = "Medico"    
    st.session_state.app_title = "Medbuddy" if st.session_state.app_title == "Medico" else "Medico"
    st.title(st.session_state.app_title)
    return st.session_state.app_title

change_name_tool = Tool(
    name="Change Name",
    func=toggle_bot_name,
    description="Changes the name of the bot when the user requests."
)
