import os
from dotenv import load_dotenv

load_dotenv()

# get discord bot token from environment variables
def get_bot_token():
    env_var = os.environ
    if 'TOKEN' not in env_var:
        print(f"Error: environment variable TOKEN is missing")
        quit()
    return env_var["TOKEN"]
