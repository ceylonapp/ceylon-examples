class PlayerCoordinatorAgent:
    def __init__(self, config=None):
        pass

    async def accept_message(self, message):
        pass

    async def run_agent(self, request):
        print(request)
        await self.send_message(data={
            "status": "accept",
            "command": "command"
        })
