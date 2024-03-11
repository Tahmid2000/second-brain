from remindMe.remindMeAssistant import create_task_object, fix_task_object
from remindMe.remindMeApiCall import create_todo_with_api

def setup(bot):
    def process_string(input_string):
        return f"remind me to {input_string}"
    
    @bot.command()
    async def remindme(ctx, *, arg):
        def authorize(m):
            return m.author == ctx.author and m.channel == ctx.channel
        def check(m):
            return authorize(m)

        # try:
        processed_string = process_string(arg)
        task_object = create_task_object(processed_string)
        print(f"Assistant's task object: {task_object}")
        [response_status_code,actual_task_object] = create_todo_with_api(task_object)
        if 200 <= response_status_code < 300:
            await ctx.send(f"Created this task for you:```{actual_task_object}```")
        else:
            await ctx.send(f"Failed to create task.")
        # except:
        #     await ctx.send(f"Failed to create task. except")

