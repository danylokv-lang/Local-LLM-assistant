from model import AIModel

class Brain:
    def __init__(self):
        self.model = AIModel()
        self.history = []

    def process(self, user_input):
        response = self.model.generate(user_input, history=self.history)
        self.history.append({"user": user_input, "assistant": response})
        return response
