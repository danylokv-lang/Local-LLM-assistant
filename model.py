from llama_cpp import Llama

class AIModel:
    def __init__(self):
        print("Loading model on GPU with llama.cpp...")
        self.model = Llama(
            model_path="models/meta-llama-3-8b-instruct-q4_0.gguf",
            n_ctx=2048,
            n_gpu_layers=40,
            verbose=False
        )
        print("Model loaded!")

    def generate(self, user_input, history=None):
        system_prompt = "You are a helpful and friendly assistant."

        full_prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>\n\n"
            f"{system_prompt}<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_input}<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n\n"
        )

        output = self.model(
            full_prompt,
            max_tokens=200,
            stop=["<|eot_id|>"],
        )
        text = output["choices"][0]["text"].strip()
        return text

