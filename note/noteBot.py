from note.noteAssistant import create_note_object
from note.noteApiCall import create_note_with_api

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

        processed_string = process_string(arg)
        try: 
            note_object = create_note_object(processed_string)
            print(f"Assistant's note object: {note_object}")
            [response_status_code,actual_note_object] = create_note_with_api(note_object, processed_string)
            if 200 <= response_status_code < 300:
                await ctx.send(f"Created this note for you:```{actual_note_object}```")
            else:
                await ctx.send(f"Failed to create note.")
        except:
            await ctx.send(f"Failed to create note. Exception caused.")


# fix: dont let chatgpt create too much of its own thing