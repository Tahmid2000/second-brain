# main_api.py
from fastapi import FastAPI
from note.noteApi import router as router_note
from remindMe.remindMeApi import router as router_remindMe
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #TODO: change
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_remindMe, prefix="/remind_me")
app.include_router(router_note, prefix="/note")
