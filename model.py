from llama_cpp import Llama
from config import SYSTEM_PROMPT

class AIModel:
    def __init__(self):
        print("Loading model on GPU with llama.cpp...")
        # path до твоєї quantized моделі
        self.model = Llama(
            model_path="models/mistral-7b-openorca.Q4_K_M.gguf",
            n_gpu_layers=40,  # скільки шарів запускати на GPU, налаштувати можна
            verbose=False
        )
        print("Model loaded!")

    def generate(self, prompt):
        # повний prompt з системою + історією
        full_prompt = SYSTEM_PROMPT + "\n" + prompt

        output = self.model(
            full_prompt,
            max_tokens=150,
            stop=["User:", "Assistant:"]
        )

        # обрізаємо зайве
        text = output.get("text", "")
        if "User:" in text:
            text = text.split("User:")[0]
        return text.strip()

    