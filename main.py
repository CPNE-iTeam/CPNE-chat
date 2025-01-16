from flask import Flask, request
import requests
import threading
from rich.console import Console
from rich.prompt import Prompt
import time
import logging
import random

app = Flask(__name__)
console = Console()
DEBUG = False

WELCOME_MESSAGE = """
 ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░        ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓████████▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
 ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░                                                                                                         
"""

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$?!@#%&*()_+-=[]{}|;:,.<>"

def send(dest, message, senderUsername):
    data = {
        "message": message,
        "sender": senderUsername
    }
    r = requests.post(f"http://{dest}:5000", json=data)




def chat():
    time.sleep(1)
    for i in range(10):print()      
    console.print(f"[bold blue]{WELCOME_MESSAGE}[/bold blue]")
    print()
    username = Prompt.ask("Entrez votre nom d'utilisateur")
    dest = Prompt.ask("Entrez le destinataire")

    message = ""
    while message != "/exit":
        message = Prompt.ask(">")
        send(dest, message, username)
        console.print(f"[bold]{username}:[/bold] {message}")
        if message == "/matrix":
            print_matrix()
            


def print_matrix():
    for i in range(50):
        console.print(f"[bold green]{''.join([LETTERS[random.randint(0, len(LETTERS)-1)] for i in range(200)])}[/bold green]")
        time.sleep(0.01)
    

@app.route("/", methods=["POST"])
def receive():
    data = request.json
    message = data["message"]
    sender = data["sender"]
    console.print(f"[bold blue]{sender}:[/bold blue] {message}")
    if message == "/matrix":
        print_matrix()
    return "OK"



if __name__ == "__main__":
    # Disable flask logs
    if not DEBUG:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    chatThread = threading.Thread(target=chat)
    chatThread.start()
    app.run(debug=DEBUG, host="0.0.0.0", port=5000)
