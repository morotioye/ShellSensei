import os
import subprocess
from sys import platform
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


class ShellSensei:
    def __init__(self, model="gpt-4", temperature=0.5):
        load_dotenv(find_dotenv())
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.term_gpt = ChatOpenAI(model=model, temperature=temperature)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)
        self.system_message = open("HyperParams/system_message.txt", "r").read()
        self.command_executor = self._init_command_executor()
        self.tools = [self.command_executor]
        self.template = self._init_template()
        self.agent = self._init_agent()

    def _run_command(self, text):
        try:
            command_output = subprocess.check_output(text, shell=True, stderr=subprocess.STDOUT)
            return command_output
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode('utf-8')}"

    def _init_command_executor(self):
        description = (
            "This method is used to run a command in the terminal. "
            "It takes in one str param which is the command to be run, "
            "runs it, and returns output if no error occurs, else, it returns the error message."
        )
        return Tool(name="command-executor", func=self._run_command, description=description)

    def _init_template(self):
        template = (
            f"{self.system_message}\n\nYou are running on {{platform}}. "
            "\n\nHuman: {human_input}\nChatbot:"
        )
        return PromptTemplate(input_variables=["human_input", "platform"], template=template)

    def _init_agent(self):
        return initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=self.tools,
            llm=self.term_gpt,
            verbose=True,
            max_iterations=5,
            memory=self.memory
        )

    def interact(self):
        while True:
            query = input("You: ")
            print(self.agent(self.template.format(human_input=query, platform=platform))["output"])
