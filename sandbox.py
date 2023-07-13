# testing LangChain implementation
import subprocess
import json
from sys import platform
import os 
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.agents import AgentType
from HyperParams.Context import Context
from dotenv import load_dotenv, find_dotenv
from HyperParams.Context import Context
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent


# Load env variables
load_dotenv(find_dotenv())
openai_api_key = os.getenv("OPENAI_API_KEY")
context = Context("HyperParams/history.json")

# Init ChatModel
term_gpt = ChatOpenAI(model="gpt-4", temperature=0.5)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False) # will return history




def run_command(text: str):
    try:
        command_output = subprocess.check_output(text, shell=True, stderr=subprocess.STDOUT)
        return command_output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"



command_executor = Tool(
        name="command-executor",
        func=run_command,
        description="This method is used to run a command in the terminal. It takes in one str param which is the command to be run, runs it, and returns output if no error occurs,\
            else, it returns the error message."
    )

tools = [command_executor]

# Init prompt template
'''
Template Schema:
> System Message

> Chat History

> Human: {human_input}

'''

template = context.system_message + "\n\nYou are running on {platform}. \n\nHuman: {human_input}\nChatbot:"

prompt = PromptTemplate(
    input_variables=["human_input", "platform"],
    template=template
)


term_gpt_agent = initialize_agent(
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=term_gpt,
    verbose=True,
    max_iterations=5,
    memory=memory
)

while True:
    query = input("You: ")
    print(term_gpt_agent(prompt.format(human_input=query, platform=platform))["output"])