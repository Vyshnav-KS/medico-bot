import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from chain.lc_chain import get_response
import langchain
from database.vector_search import get_retriever
langchain.verbose = False
langchain.debug = False

load_dotenv()

st.set_page_config(page_title="Medico", page_icon="🤖")
st.title("Medico")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I'm Medico, your personal assistant for all your medical inquiries. How can I assist you today?"),
    ]


# conversation --------------
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input -------------------
user_query = st.chat_input("Type your message here...")
context = get_retriever(user_query)
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        try:
            output = get_response(user_query, st.session_state.chat_history, context)
            response = output.get("output")
            st.write(response)
        except Exception as e:
            response = st.write("Network Error")
            print(e)
        if response:
            st.session_state.chat_history.append(AIMessage(content=response))
    
