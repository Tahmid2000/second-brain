from fastapi import APIRouter, Body, HTTPException
from subprocess import Popen, PIPE, STDOUT
import json
from remindMe.remindMeValidator import create_todo

router = APIRouter()

@router.post("/execute-jxa/")
async def execute_jxa(task: str = Body(..., embed=True), date: str = Body(..., embed=True), category: str = Body(..., embed=True)):
    command = f'osascript -l JavaScript "/Users/tahmidimran/CS Side Projects/automation-projects/second-brain/remindMe/remindMeCreate.scpt" "{task}" "{category}" "{date}"'
    # Execute the JXA script
    try:
        process = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Script execution failed: {stderr}")

        return {"response": "success"}

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/process-user-message/")
async def process_user_message(message: str = Body(..., embed=True)):
    try:
        task = create_todo(message)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
