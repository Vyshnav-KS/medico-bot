import streamlit as st
from langchain.agents import Tool
from langchain.tools import BaseTool

def toggle_bot_name():
    if "bot_name" not in st.session_state:
        st.session_state.bot_name = "Medico"    
    st.session_state.bot_name = "Medbuddy" if st.session_state.bot_name == "Medico" else "Medico"
    return st.session_state.bot_name

change_name_tool = Tool(
    name="Change Name",
    func=toggle_bot_name,
    description="Changes the name of the bot when the user requests."
)