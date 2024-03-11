import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
api_url = os.getenv("API_URL")

def validate_task(data):
    try:
        data_dict = json.loads(data)

        valid_categories = ["To-Do List", "Work", "Other"]
        if data_dict.get("category") not in valid_categories:
            data_dict["category"] = "To-Do List"
        if data_dict.get("category") == "Work":
            data_dict["category"] = "Microsoft"

        try:
            datetime.strptime(data_dict.get("date"), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            data_dict["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        return data_dict
    
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"})

def post_task(api_url, data):
    # Construct the JSON body of the POST request
    # data = {
    #     "task": task,
    #     "category": category,
    #     "date": date
    # }

    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        print("Successfully posted to API.")
        return response.status_code, response.json()
    else:
        print("Failed to post to API. Status code:", response.status_code)
        return response.status_code, None

def create_todo_with_api(data):
    task = validate_task(data)
    print(f"Validated task: {task}")
    response_status_code, response = post_task(f"{api_url}/remind_me/execute-jxa", task)
    return [response_status_code,task]

