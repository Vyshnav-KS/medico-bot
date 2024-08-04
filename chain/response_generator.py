from dotenv import load_dotenv
from chain.prompts.system_prompt import system_instruction
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from chain.tools.medical_tool import medical_tool
from chain.tools.general_tool import general_tool
from chain.tools.application_tool import application_tool
from langchain_community.cache import InMemoryCache
from langchain_openai import AzureChatOpenAI
from langchain.globals import set_llm_cache
from langsmith import traceable
from config.settings import settings
from langchain import hub

# set_llm_cache(InMemoryCache())

@traceable
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
        # prompt = system_prompt

        instructions = system_instruction
        base_prompt = hub.pull("langchain-ai/react-agent-template")
        prompt = base_prompt.partial(instructions=instructions)


        model = AzureChatOpenAI(model=settings.azure_openai_settings.model, openai_api_type=settings.azure_openai_settings.openai_api_type)

        agent = create_react_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            handle_parsing_errors=True, 
            memory=memory,
            max_iterations=3,
            verbose=True,
            )
        
        print(f"User query: {user_query}")
        return agent_executor.stream({
            "input": f"User question: {user_query}",
            "chat_history": chat_history,
        })
    except Exception as e:
        print(e)
        return None


    