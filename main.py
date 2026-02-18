from brain import Brain

def main():
    brain = Brain()
    print("\n" + "="*50)
    print("AI Assistant is running!")
    print("="*50)
    print("Commands: /help - help, /exit - exit")
    print("Or just speak in natural language!")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["/exit", "exit", "вийти", "вийди"]:
                print("Goodbye!")
                break
            
            if user_input.lower() == "/clear":
                print(brain.clear_history())
                continue
                
            response = brain.process(user_input)
            print(f"AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

