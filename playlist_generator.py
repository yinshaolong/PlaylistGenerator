import openai
import os
import dotenv
import argparse
import json

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

model = {3:"gpt-3.5-turbo", 4:"gpt-4-1106-preview"}

def parse_args():
    parser = argparse.ArgumentParser(description='Generate a playlist based on a prompt')
    parser.add_argument('-p', type=str, help='Prompt to generate playlist from')
    parser.add_argument('-m', default = 4, type=str, help='Model to use for generation')
    parser.add_argument('-l', default = 5, type=int, help='Length of playlist to generate')
    return parser.parse_args()



def get_reply():
    args = parse_args()
    model = args.m
    messages = get_prompt()
    messages[1].user = f'{messages[1].user}{args.p if args.p else get_user_input("prompt")}'

    for data in client.chat.completions.create(
    model=model,
    messages= messages,
    max_tokens = 200,
    stream=True,
    ):          
         #streams have a different format - have delta.content instead of message.content
        content = data.choices[0].delta.content
        if content is not None:
            yield content

def get_user_input(prompt:str)->str:
    valid_input = False
    while not valid_input:
        user_input = input(f"No {prompt} given. Please enter a {prompt}: ")
        valid_input = True if user_input else False
    return user_input

def get_prompt()->list[dict]:
    with open("prompt.json", "r") as f:
        return json.load(f)
    
def main():
    for data in get_reply():
        print(data)
if __name__ == "__main__":
    main()