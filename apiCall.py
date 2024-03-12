import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv("API_URL")

def post_message(api_uri, data):
    response = requests.post(f"{api_url}/{api_uri}", json=data)

    if response.status_code == 200:
        print("Successfully posted to API.")
        return response.status_code, response.json()
    else:
        print("Failed to post to API. Status code:", response.status_code)
        return response.status_code, None