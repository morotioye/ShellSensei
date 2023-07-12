import argparse
from HyperParams.Context import Context
from Models.GPT3Config import GPT3Config

def parse_args():
    """
    Contains all the argparsers for handling command line interaction
    """
    parser = argparse.ArgumentParser(description='TermGPT')
    parser.add_argument('model', type=str, help='Model to use (GPT3 or GPT4)')
    return parser.parse_args()

def main():
    """
    Implements the main logic for executing the program.
    """
    args = parse_args()
    context = Context()
    if args.model.upper() == 'GPT3':
        gpt3_config = GPT3Config(model=args.model, history=context.get_history(), output_file='output.txt')
        gpt3_config.t_prompt()
    elif args.model.upper() == 'GPT4':
        print("GPT4 is not yet implemented.")
    else:
        print("Invalid model. Please choose either GPT3 or GPT4.")

if __name__ == "__main__":
    main()
