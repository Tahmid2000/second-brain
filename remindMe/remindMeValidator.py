import json
from datetime import datetime
from remindMe.remindMeAssistant import create_task_object
from subprocess import Popen, PIPE, STDOUT

import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from FailedFunctionException import FailedFunctionException

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

def execute_script(task, date, category):
    command = f'osascript -l JavaScript "/Users/tahmidimran/CS Side Projects/automation-projects/second-brain/remindMe/remindMeCreate.scpt" "{task}" "{category}" "{date}"'
    try:
        process = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        stdout, stderr = process.communicate()
        return "Success"
    except Exception as e:
        raise FailedFunctionException(str(e))
    
def create_todo(message):
    task_object = create_task_object(message)
    print(f"Assistant's task object: {task_object}")

    task = validate_task(task_object)
    print(f"Validated task: {task}")

    try:
        task_created_status = execute_script(task=task['task'], date=task['date'], category=task['category'])
        return task
    except Exception as e:
        raise FailedFunctionException(str(e))

