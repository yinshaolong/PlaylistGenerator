import openai
import os
import dotenv
import argparse
import json

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

model = {3:"gpt-3.5-turbo", 4:"gpt-4-1106-preview"}

example_json = """[
  {"song": "Eye of the Tiger", "artist": "Survivor"},
  {"song": "Stronger", "artist": "Kanye West"},
  {"song": "Don't Stop Believin'", "artist": "Journey"},
  {"song": "Harder, Better, Faster, Stronger", "artist": "Daft Punk"},
  {"song": "Can't Hold Us", "artist": "Macklemore & Ryan Lewis"}
]"""
def parse_args():
    parser = argparse.ArgumentParser(description="Generate a playlist based on a prompt")
    parser.add_argument("-p", default = "motivation to do homework last minute", type=str, help="Prompt to generate playlist from")
    parser.add_argument("-m", default = 3, type=str, help="Model to use for generation")
    parser.add_argument("-l", default = 5, type=int, help="Length of playlist to generate")
    return parser.parse_args()



def get_reply():
    args = parse_args()
    gpt_model = args.m

    messages = get_prompt()
    count = args.l if args.l else get_user_input("length of playlist")
    playlist_gen_prompt = f"Generate a playlist of {count} songs based on this prompt:"

    messages[1]["content"] = f"{messages[1]['content']}{'motivation to do homework last minute'}"
    messages[2]["content"] = f"{example_json}"
    messages[3]["content"] = f"{playlist_gen_prompt}{args.p if args.p else get_user_input('prompt')}"
    print("messages: ",messages)
    for data in client.chat.completions.create(
    model=model[gpt_model],
     messages=messages,
    # max_tokens = 200,
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

def get_playlist()->list[dict]:
    playlist_tokens = []
    for data in get_reply():
        playlist_tokens.append(data)
        print(data, end="", flush=True)
    playlist = "".join(playlist_tokens)
    playlist = json.loads(playlist)
    return playlist

def main():
    playlist = get_playlist()
    print("\n\n\nplaylist: ",playlist, "type: ",type(playlist))
if __name__ == "__main__":
    main()