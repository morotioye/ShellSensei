import os
import subprocess
import openai
from Stats.OpenAIAPIStats import OpenAIAPIStats
from dotenv import load_dotenv


class GPT3Config:
    def __init__(self, model, history, output_file):
        self.model = model
        self.history = history
        self.output_file = output_file
        self.usage = OpenAIAPIStats()
        load_dotenv()

    def _print_history(self):
        """Prints the history of the conversation to console, then --- Resuming Session ---"""
        print('\n'.join(self.history))
        print('--- Resuming Session ---')

    def append(self, user_or_model, message):
        """
        Adds the last message from either User or Assistant to history.
        user_or_model: 0 if user, 1 if assistant
        """
        role = 'user' if user_or_model == 0 else 'assistant'
        self.history.append({'role': role, 'content': message})


    def get_completion(self, prompt):
        """
        Retrieves the completion from GPT-3 API
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.history,
        )

        return response.choices[0].message.content

    def t_prompt(self):
        """
        Method responsible for bringing together all functionalities. 
        Runs loop in terminal, prompting user, appending content, calculating usage, and executing commands
        """
        while True:
            user_input = input("You: ")
            if user_input == "--next":
                self.append(0, user_input)
                print("Assistant: ", self.get_completion(self.history))
            elif user_input == "--done":
                break
            else:
                self.append(0, user_input)
                print("Assistant: ", self.get_completion(self.history))

    def execute(self, command):
        """
        Given a command, executes it in terminal
        """
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print('Output: ', output)
        print('Error: ', error)


