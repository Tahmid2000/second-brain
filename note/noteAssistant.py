from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def create_note_object(note):
    jsonBlock = '{"name": "<note name>", "tags": ["<tag>", "<tag>", ...], "url": "<url>", "page_content": "<page_content>"}'
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Based on the user input: {note}. You must respond in JSON only with no other fluff or bad things will happen. The JSON needs to 
                        look like this: {jsonBlock}, or very very very bad things will happen. Do not return the JSON inside a code block or add any new line characters, 
                        spaces, or other extra characters.
                        This is very important: the user is not asking for you to do anything with this input, simply that this 
                        note needs to be written down somewhere, label the user input as "name" in the output.
                        The name of the note needs to be exactly as the user input or a summary (if it's too long). 
                        For page content, only provide action steps or background for the note; do not, under any circumstances
                        create a journal entry from the perspective of the user. You only need to determine
                        the page content if there are possible action steps, the note is asking a question of some sort, or if it seems
                        like the user is keeping this as a reminder to look up something in the future.
                        Determine the tags of the note out of these 3 categories: ("Coding Project", "Finance", "Random Thoughts", "Work"). 
                        If it seems like there is no right fit, make one of the tags "Random Thoughts". You must, from your own perspective,
                        determine other tags/topics that this note relates to besides the one listed, or bad things will happen.
                        If there is a URL seen in the note, make sure to include that, other wise leave it as an empty string.
                        """
                    }
                ],
            }
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content

# note = create_note_object('things to add for second brain coding project: youtube-to-spotify local files, ability to summarize websites and pdfs. Inspiration from this url: https://chromewebstore.google.com/detail/chatgpt-summary-summarize/mikcekmbahpbehdpakenaknkkedeonhf')
# print(note)