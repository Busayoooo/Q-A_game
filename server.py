import socket
import threading

# Server settings
HOST = "127.0.0.1"  # Localhost IP address
PORT = 12345  # Port number for the server
clients = []  # List to store connected client sockets
usernames = []  # List to store usernames of players
scores = {}  # Dictionary to keep track of player scores

# Questions and answers for the quiz game
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the capital city of Japan?", "answer": "Tokyo"},
    {"question": "How many continents are there in the world?", "answer": "7"},
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "What is the largest planet?", "answer": "Jupiter"},
]
current_question = 0  # Index to track the current question

def broadcast(message):
    """Send a message to all connected clients."""
    for client in clients:
        client.send(message.encode())

def handle_client(client, addr):
    """Handle communication with an individual client."""
    global current_question
    username = client.recv(1024).decode()  # Receive username from client
    usernames.append(username)  # Store username
    scores[username] = 0  # Initialize score for the player

    # If only one player has joined, wait for the second player
    if len(clients) < 2:
        client.send("Waiting for another player...".encode())
    else:
        broadcast("Game starting!")  # Notify all players that the game is starting

        # Iterate through the quiz questions
        for q in questions:
            broadcast(f"Question: {q['question']}")  # Send the question to all clients
            answers = []  # List to store answers from players

            # Collect answers from all players
            for c in clients:
                answer = c.recv(1024).decode()
                answers.append(answer)

            # Evaluate answers and update scores
            for i, answer in enumerate(answers):
                if answer.lower() == q["answer"].lower():  # Check if answer is correct
                    scores[usernames[i]] += 1  # Increment the player's score

        # Determine the winner based on the highest score
        winner = max(scores, key=scores.get)
        broadcast(f"The winner is {winner} with {scores[winner]} points!")  # Announce the winner

        # Close connections for all clients
        for client in clients:
            client.close()

def start_server():
    """Start the server and handle incoming client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    server.bind((HOST, PORT))  # Bind the socket to the host and port
    server.listen(2)  # Listen for up to 2 connections
    print("Server started. Waiting for connections...")

    # Accept connections until 2 players have joined
    while len(clients) < 2:
        client, addr = server.accept()  # Accept a new connection
        clients.append(client)  # Add client to the list
        threading.Thread(target=handle_client, args=(client, addr)).start()  # Start a thread for the client

if __name__ == "__main__":
    start_server()  # Run the server
