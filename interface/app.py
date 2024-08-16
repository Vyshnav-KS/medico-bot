import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from chain.response_generator import get_response
import langchain

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
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        try:
            # response = get_response(user_query, st.session_state.chat_history)
            response = st.write_stream(get_response(user_query, st.session_state.chat_history))
            content = response["output"]
            st.write(content)
            st.session_state.chat_history.append(AIMessage(content))
        except Exception as e:
            # content = st.write("Network Error")
            print(e)
    
