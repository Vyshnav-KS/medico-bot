from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from chain.prompts.system_prompt import system_prompt
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from chain.tools.medical_tool import medical_tool
from chain.tools.general_tool import general_tool
from chain.tools.application_tool import application_tool

def get_response(user_query, chat_history):

    load_dotenv()
    tools = [application_tool, medical_tool, general_tool]

    memory = ConversationBufferWindowMemory(
        memory_key='chat_history', 
        k=5, 
        return_messages=True
        )
    
    try:
        # Prompt template
        prompt = system_prompt
        model = ChatOpenAI(model='gpt-3.5-turbo')

        agent = create_react_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            handle_parsing_errors=True, 
            memory=memory
            )
        
        print(f"User query: {user_query}")
        return agent_executor.invoke({
            "input": f"User question: {user_query}",
            "chat_history": chat_history,
        })
    except Exception as e:
        print(e)
        return None


    