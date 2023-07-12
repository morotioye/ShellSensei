from textwrap import dedent
from sys import platform

'''
This class stores the context of the conversation, which is eventually transformed into a vector database

'''
class Context:
    def __init__(self, platform):
        self.history = []
        self.platform = platform # iterate on this to include 
        self.chain_of_thought = [
                # User
                # dedent(f"""\
                # Given text input from a user looking to do programming, help to build a series of console commands 
                # that will achieve the goals of the prompt. Your responses will be one command at a time, where each 
                # response is the command and nothing but the command. When ready for the next command, the user will say "--next" 
                # and you will respond with the next command. When we have reached the end of console commands, respond with 
                # "--done" and then you will do it again with some new input from the user. We are running on {platform}.
                # """),

                dedent(f"""\
                You are a command line assistant. Given text input from a user, help build a series of console commands
                that will achieve the goals of the prompt. 
                - We are running on {platform}.
                - Your responses will be one at a time, where each response is the command and nothing but the command.
                - When ready for the next command the user will say "--next" and you will respond with the next command.
                - When you reached the end of the terminal commands, respond with "--done".
                """),

                # Assistant
                "Understood! How can I assist you today with terminal commands?",

                # User    
                "Build a basic Flask app.",

                # Assistant
                "`pip install flask`",

                # User
                "--next",

                # Assistant
                "`mkdir basic_flask_app`",

                # User
                "--next",

                # Assistant
                dedent('''\
                `cat << 'EOF' > basic_flask_app/app.py
                from flask import Flask, render_template

                app = Flask(__name__)

                @app.route('/')
                def index():
                    return render_template('index.html')

                @app.route('/about')
                def about():
                    return render_template('about.html')

                if __name__ == '__main__':
                    app.run(debug=True)

                EOF`'''),

                # User
                "--next",

                dedent('''\
                `cat << EOF > basic_flask_app/templates/index.html
                <!DOCTYPE html>
                <html>
                <head>
                    <title>My Flask App</title>
                </head>
                <body>
                    <h1>Welcome to My Flask App</h1>
                    <p>This is the home page!</p>
                </body>
                </html>
                EOF`'''),

                "--next",

                dedent('''\
                `cat << 'EOF' > basic_flask_app/templates/about.html
                <!DOCTYPE html>
                <html>
                <head>
                    <title>About My Flask App</title>
                </head>
                <body>
                    <h1>About My Flask App</h1>
                    <p>This is a simple Flask app that demonstrates the use of templates!</p>
                </body>
                </html>
                EOF`'''),

                "--next",

                # Assistant
                "`python basic_flask_app/app.py`",

                # User
                "--next",

                # Assistant
                "--done",

                # User
                "List my current directory",

                # Assistant
                "`ls`",

                # User
                "--next",

                # Assistant
                "--done",

                # User
                "Create a basic React app",

                # Assistant
                "`npx create-react-app basic-app`"
            ]
        
        self.init_history()

    def init_history(self) -> list:
        roles: list = ["user", "assistant"]
        for i, content in enumerate(self.chain_of_thought):
            self.append(roles[i % 2], content, self.history)
    
    
    def get_history(self) -> list:
        return self.history
    
    def append(self, role: str, content: str, history) -> None:
        history.append({"role": role, "content": content})


