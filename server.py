import socket
import threading

# Server settings
HOST = "127.0.0.1"
PORT = 12345
clients = []
usernames = []
scores = {}

# Questions and answers
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the capital city of Japan?", "answer": "Tokyo"},
    {"question": "How many continents are there in the world?", "answer": "7"},
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "What is the largest planet?", "answer": "Jupiter"},
]
current_question = 0

def broadcast(message):
    """Send a message to all clients."""
    for client in clients:
        client.send(message.encode())

def handle_client(client, addr):
    """Handle communication with a client."""
    global current_question
    username = client.recv(1024).decode()
    usernames.append(username)
    scores[username] = 0

    # Wait until both players join
    if len(clients) < 2:
        client.send("Waiting for another player...".encode())
    else:
        broadcast("Game starting!")

        # Send questions
        for q in questions:
            broadcast(f"Question: {q['question']}")
            answers = []
            for c in clients:
                answer = c.recv(1024).decode()
                answers.append(answer)

            # Evaluate answers
            for i, answer in enumerate(answers):
                if answer.lower() == q["answer"].lower():
                    scores[usernames[i]] += 1

        # Announce winner
        winner = max(scores, key=scores.get)
        broadcast(f"The winner is {winner} with {scores[winner]} points!")
        for client in clients:
            client.close()

def start_server():
    """Start the server and handle incoming clients."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Server started. Waiting for connections...")

    while len(clients) < 2:
        client, addr = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()
