from fastapi import APIRouter, HTTPException, Body
from typing import Optional, List
from pydantic import BaseModel
from note.createNoteNotion import add_to_notes_db
from note.noteApiCall import create_note_with_api
from note.noteAssistant import create_note_object
router = APIRouter()

class NotionRow(BaseModel):
    name: str
    tags: List[str]
    actual_note: str
    url: Optional[str] = None
    page_content: Optional[str] = None

@router.post("/execute-add-notion-db/")
async def add_row(row: NotionRow):
    try:
        response = add_to_notes_db(
            name=row.name,
            tags=row.tags,
            actual_note=row.actual_note,
            url=row.url,
            page_content=row.page_content
        )
        return {"message": "Row added successfully.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/process-user-message/")
async def process_user_message(message: str):
    try:
        note_object = create_note_object(message)
        print(f"Assistant's note object: {note_object}")
        [response_status_code,actual_note_object] = create_note_with_api(note_object, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))