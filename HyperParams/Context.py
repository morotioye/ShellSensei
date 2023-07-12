import json
from sys import platform

class Context:
    def __init__(self, history_path):
        # test empty history
        self.history = json.load(open(history_path, 'r'))
        self.system_message = open("HyperParams/system_message.txt", "r").read() + f"\nWe are running on \"{platform}\""
        
        self.init_history()
        
    def init_history(self):
        if len(self.history) == 0:
            with open('HyperParams/sample_conversation.json', 'r') as f:
                self.history = json.load(f)

    def log(self, history_path):
        json.dump(self.history, open(history_path, 'w'), indent=4)


    
# Test system message
if __name__ == "__main__":
    context = Context("HyperParams/history.json")
    print(context.history)

 

