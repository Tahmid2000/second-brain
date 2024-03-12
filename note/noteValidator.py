import json
from datetime import datetime
from note.noteAssistant import create_note_object
from note.noteCreate import add_to_notes_db

import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from FailedFunctionException import FailedFunctionException

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

def create_note(message):
    note_object = create_note_object(message)
    print(f"Assistant's note object: {note_object}")

    note = validate_note(note_object, message)
    print(f"Validated note: {note}")

    try:
        created_noted = add_to_notes_db(
            name=note['name'],
            tags=note['tags'],
            actual_note=note['actual_note'],
            url=note['url'],
            page_content=note['page_content']
        )
        return note
    except Exception as e:
        raise FailedFunctionException(str(e))

# create_note_with_api("error", "errorasdfasdffasdf")