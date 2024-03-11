from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def create_task_object(task):
    jsonBlock = '{"task": "<task>", "date": "YYYY-MM-DDTHH:MM:SS", "category": "<category>"}'
    todayDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Based on the user input {task}. Determine the task the user wants to be reminded of. 
                        Determine the date of the task in the format "YYYY-MM-DDTHH:MM:SS" given that today is {todayDate}. 
                        If the user doesn’t explicitly mention a date, set the date to {todayDate} and the time to 10 minutes from 
                        right now, given that the time right now is: {datetime.now().strftime("%H:%M:%S")}. 
                        If the user mentions "morning" time, set the time to "10:00:00".
                        If the user mentions "afternoon" time, set the time to "15:00:00".
                        If the user mentions "evening" or "night" time, set the time to "21:00:00".
                        If the user mentions a date, but not a time, set the time to "11:00:00".
                        Determine the category of the task out of these 
                        3 categories: (Work, To-Do List, Other). If the user doesn’t explicitly mention a category the task to be sorted to, 
                        make your best guess you have to make a choice out of (Work, To-Do List, Other) or bad things will happen;
                        default to To-Do List as a last case scenario. 
                        You must respond in JSON only with no other fluff or bad things will happen. The JSON needs to 
                        look like this: {jsonBlock}. Do not return the JSON inside a code block or add any new line characters, 
                        spaces, or other extra characters."""
                    }
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content

def fix_task_object(task, input):
    jsonBlockTask = "{'task': '<task>', 'date': 'mm-dd-yyyy', 'category': '<category>'}"
    jsonBlockClarify = "{'aiResponse': '<response>'}"
    jsonBlockCorrect = "{'aiResponse': '<clarifyingQuestion>'}"
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You gave the user this task: {task}, and the user responed with this: {input}.
                        If the user says something is wrong, then determine what is wrong and update the appropriate key,value in the task. If you update the date, it must be in the
                        format mm-dd-yyyy given that today is {datetime.now()}. If you update the category, you have to make a choice out of (Work, Personal, Other) or bad things will happen. 
                        If the user doesn't mention what value a key should be changed to ask a clarifying 
                        question in this format: {jsonBlockClarify}. If the user says nothing is wrong, respond with an empty string in this format: {jsonBlockClarify}.
                        You must respond in JSON only with no other fluff or bad things will happen. Do not return the JSON inside a code block or add any 
                        new line characters, spaces, or other extra characters."""
                    }
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content

# task = create_task_object('figure out why the jobs are failing tomorrow at work')
# print(task)
# task = "{'task': 'read the day trading instructions pdf', 'date': '03-04-2024', 'category': 'Work'}"
# fixed = fix_task_object(task, "category is wrong")
# print(fixed)