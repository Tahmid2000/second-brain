import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from notion_client import Client

load_dotenv()
notion_integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
notion_page_id = os.getenv("NOTION_PAGE_ID")
notion_second_brain_notes_db = os.getenv("NOTION_SECOND_BRAIN_NOTES_DB")

notion = Client(auth=notion_integration_token)

def get_pages():
    subpages = []
    url = f"https://api.notion.com/v1/blocks/{notion_page_id}/children"
    headers = {
        "Authorization": f"Bearer {notion_integration_token}",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(url, headers=headers)
    with open('db.json', 'w', encoding='utf8') as f:
       json.dump(response.json(), f, ensure_ascii=False, indent=4)

    if response.status_code == 200:
        blocks = response.json().get('results', [])
        for block in blocks:
            if block['type'] == 'child_page':
                subpages.append(block)
        return subpages
    else:
        print(f"Failed to fetch subpages. Status code: {response.status_code}")
        return []
    
# function to add a note to any page
def add_to_page():
    pass

def markdown_to_notion(markdown_text):
    """
    Convert simple Markdown text to a Notion block structure.
    Currently supports basic text as a demonstration.
    """
    notion_blocks = []
    if markdown_text:
        # Adjusted for the correct structure with 'rich_text'
        notion_blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": markdown_text,
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                }],
            },
        })
    return notion_blocks

def to_none_if_empty_or_null(input_string):
    # Check if the string is None or empty (after stripping whitespace)
    if input_string is None or input_string.strip() == "":
        return None
    else:
        return input_string
    
# function to add to "other" notes
def add_to_notes_db(name, tags, actual_note, url=None, page_content=None):
    current_datetime = datetime.now().isoformat()
    new_row_properties = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": name
                    }
                }
            ]
        },
        "Tags": {
            "multi_select": [{"name": tag} for tag in tags]
        },
        "Actual Note": {
            "rich_text": [
                {
                    "text": {
                        "content": actual_note
                    }
                }
            ]
        },
        "Date Added": {
            "date": {
                "start": current_datetime,
                "time_zone": "America/Chicago"
            }
        }
    }
    if url:
        new_row_properties["URL"] = {
            "url": url
        }
    try:
        new_page = notion.pages.create(
            parent={"database_id": notion_second_brain_notes_db},
            properties=new_row_properties,
            # Add content to the page if page_content is provided
            children=markdown_to_notion(page_content) if page_content else []
        )
        print("Row (with detailed page) added successfully to the database.")
        return new_page
    except Exception as e:
        print(f"An error occurred: {e}")
    
# add_to_notes_db("Sample Item 22", ["Tag1", "Tag2"], "sample item", "", "")
