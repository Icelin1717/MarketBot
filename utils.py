import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
import gspread

# load config
with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

load_dotenv()
env_var = os.environ

scopes = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_info({
        "type": env_var["SERVICE_ACCOUNT_TYPE"],
        "project_id": env_var["SERVICE_ACCOUNT_PROJECT_ID"],
        "private_key_id": env_var["SERVICE_ACCOUNT_PRIVATE_KEY_ID"],
        "private_key": env_var["SERVICE_ACCOUNT_PRIVATE_KEY"],
        "client_email": env_var["SERVICE_ACCOUNT_CLIENT_EMAIL"],
        "client_id": env_var["SERVICE_ACCOUNT_CLIENT_ID"],
        "auth_uri": env_var["SERVICE_ACCOUNT_AUTH_URI"],
        "token_uri": env_var["SERVICE_ACCOUNT_TOKEN_URI"],
        "auth_provider_x509_cert_url": env_var["SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": env_var["SERVICE_ACCOUNT_CLIENT_X509_CERT_URL"],
        "universe_domain": env_var["SERVICE_ACCOUNT_UNIVERSE_DOMAIN"]
    },
    scopes=scopes)
client = gspread.authorize(credentials)
db = client.open_by_key(config["googleSheetKey"])

# get discord bot token from environment variables
def get_bot_token():
    if 'TOKEN' not in env_var:
        print(f"Error: environment variable TOKEN is missing")
        quit()
    return env_var["TOKEN"]
