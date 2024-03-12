import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from apiCall import post_message

def setup(bot):
    def process_string(input_string):
        return f"{input_string}"

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif']):
                print(attachment.url)

        await bot.process_commands(message)  

    @bot.command()
    async def note(ctx, *, arg):
        def authorize(m):
            return m.author == ctx.author and m.channel == ctx.channel
        def check(m):
            return authorize(m)

        try: 
            processed_string = process_string(arg)
            data = {"message": processed_string}
            [response_status_code,actual_note_object] = post_message("note/process-user-message", data)
            if 200 <= response_status_code < 300:
                await ctx.send(f"Created this note for you:```{actual_note_object}```")
            else:
                await ctx.send(f"Failed to create note.")
        except:
            await ctx.send(f"Failed to create note due to an exception.")


# fix: dont let chatgpt create too much of its own thing