import subprocess

def handle_command(user_input):
    if user_input.startswith("/open"):
        program = user_input.replace("/open ", "")
        subprocess.Popen(program)
        return "Програму відкрито."

    if user_input == "/exit":
        exit()

    return None
