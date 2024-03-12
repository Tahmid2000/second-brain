import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from apiCall import post_message

def setup(bot):
    def process_string(input_string):
        return f"remind me to {input_string}"
    
    @bot.command()
    async def remindme(ctx, *, arg):
        def authorize(m):
            return m.author == ctx.author and m.channel == ctx.channel
        def check(m):
            return authorize(m)

        try:
            processed_string = process_string(arg)
            data = {"message": processed_string}
            [response_status_code,actual_task_object] = post_message("remind-me/process-user-message", data)
            if 200 <= response_status_code < 300:
                await ctx.send(f"Created this task for you:```{actual_task_object}```")
            else:
                await ctx.send(f"Failed to create task.")
        except:
            await ctx.send(f"Failed to create task due to an exception.")

