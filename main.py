from brain import Brain

def main():
    brain = Brain()
    print("AI Assistant started. Type /exit to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["/exit", "exit"]:
            break
        response = brain.process(user_input)
        print("AI:", response)

if __name__ == "__main__":
    main()
