import asyncio
import uvicorn
from main_bot import run_bot

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.create_task(uvicorn.run("main_api:app", host="127.0.0.1", port=8000))