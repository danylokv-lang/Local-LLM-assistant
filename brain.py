from config import SYSTEM_PROMPT
from model import AIModel
from memory import Memory
from commands import handle_command

class Brain:
    def __init__(self):
        self.model = AIModel()
        self.memory = Memory()

    def process(self, user_input):
        command_response = handle_command(user_input)
        if command_response:
            return command_response

        self.memory.add("User", user_input)

        full_prompt = SYSTEM_PROMPT + "\n"
        full_prompt += self.memory.get_context()

        response = self.model.generate(full_prompt)

        self.memory.add("Assistant", response)

        return response
