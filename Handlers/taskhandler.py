from discord.ext import tasks
from Handlers.logger import logger
class TaskHandler():
    def __init__(self):
        self._tasks = []

    def task_launcher(self, interval, time, name, function, function_before_loop=None):
        if interval:
            new_task = tasks.loop(seconds=interval)(function)
        elif time:
            new_task = tasks.loop(time=time)(function)

        if function_before_loop:
            new_task.before_loop(function_before_loop)

        new_task.start()
        self._tasks.append(new_task)
        logger.info(f"Task {name} was created and started")