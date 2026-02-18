from config import MAX_HISTORY

class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > MAX_HISTORY:
            self.history.pop(0)

    def get_context(self):
        context = ""
        for message in self.history:
            context += f"{message['role']}: {message['content']}\n"
        return context
