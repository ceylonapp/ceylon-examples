

class TaskCreatorAgent:
    def __init__(self, config=None):
        print("Task Creator", config)

    async def accept_message(self, agent, message):
        pass

    async def run_agent(self, request):
        while True:
            await self.send_message(data={
                "payload": payload,
                "gen_time": time.time_ns()
            })
