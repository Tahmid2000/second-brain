from fastapi import APIRouter, HTTPException, Body
from typing import Optional, List
from pydantic import BaseModel
from note.noteCreate import add_to_notes_db
from note.noteValidator import create_note
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
async def process_user_message(message: str = Body(..., embed=True)):
    try:
        note = create_note(message)
        return note
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))