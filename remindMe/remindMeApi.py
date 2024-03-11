from fastapi import APIRouter, Body, HTTPException
from subprocess import Popen, PIPE, STDOUT
import json

router = APIRouter()

@router.post("/execute-jxa/")
async def execute_jxa(task: str = Body(..., embed=True), date: str = Body(..., embed=True), category: str = Body(..., embed=True)):
    # Prepare the command to execute the JXA script with arguments
    command = f'osascript -l JavaScript "/Users/tahmidimran/CS Side Projects/automation-projects/second-brain/remindMe/createTodo.scpt" "{task}" "{category}" "{date}"'
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
