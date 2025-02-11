import socket
import threading
import time

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

def broadcast(message):
    """Send a message to all clients."""
    for client in clients:
        client.send(message.encode())

def handle_client(client, addr):
    """Handle communication with a client."""
    username = client.recv(1024).decode()  # Receive username
    usernames.append(username)
    scores[username] = 0

    # Wait for both players to join
    if len(clients) < 2:
        client.send("Waiting for another player...".encode())
        return

    broadcast("Game starting!")

    # Send questions
    for q in questions:
        broadcast(f"Question: {q['question']}")
        
        answers = {}
        start_time = time.time()  # Start timer

        # Collect answers with a timeout
        for c in clients:
            c.settimeout(20)  # Set 20-second timeout for response
            try:
                answer = c.recv(1024).decode()
                answers[c] = answer  # Store the answer
            except socket.timeout:
                answers[c] = "No Answer"  # If the player didn't answer, mark as "No Answer"
        
        # Evaluate answers
        for c, answer in answers.items():
            player_index = clients.index(c)
            player_username = usernames[player_index]
            if answer.lower() == q["answer"].lower():
                scores[player_username] += 1

    # Announce winner
    winner = max(scores, key=scores.get)
    broadcast(f"The winner is {winner} with {scores[winner]} points!")

    # Close all client connections
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
