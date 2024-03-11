import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
api_url = os.getenv("API_URL")

def validate_note(data, initial_note):
    try:
        data_dict = json.loads(data)
        data_dict['actual_note'] = initial_note

        # valid_categories = ["To-Do List", "Work", "Other"]
        # if data_dict.get("category") not in valid_categories:
        #     data_dict["category"] = "To-Do List"
        # if data_dict.get("category") == "Work":
        #     data_dict["category"] = "Microsoft"

        # try:
        #     datetime.strptime(data_dict.get("date"), "%Y-%m-%dT%H:%M:%S")
        # except ValueError:
        #     data_dict["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        return data_dict
    
    except json.JSONDecodeError:
        return {'name': initial_note, 'tags': ['Random Thoughts'], 'actual_note': initial_note}

def post_note(api_url, data):
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        print("Successfully posted to API.")
        return response.status_code, response.json()
    else:
        print("Failed to post to API. Status code:", response.status_code)
        return response.status_code, None

def create_note_with_api(data, initial_note):
    note = validate_note(data, initial_note)
    print(f"Validated note: {note}")
    response_status_code, response = post_note(f"{api_url}/note/execute-add-notion-db", note)
    return [response_status_code,note]

# create_note_with_api("error", "errorasdfasdffasdf")