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

def send_message(client, message):
    """Send a message to a specific client."""
    try:
        client.send(message.encode())
    except:
        pass  # Ignore errors if client disconnects

def broadcast(message):
    """Send a message to all clients."""
    for client in clients:
        send_message(client, message)

def countdown_timer(duration, client):
    """Sends countdown updates to a client."""
    for remaining in range(duration, 0, -1):
        send_message(client, f"Time left: {remaining} seconds")
        time.sleep(1)

def handle_client(client):
    """Handle communication with a client."""
    username = client.recv(1024).decode()  # Receive username
    usernames.append(username)
    scores[username] = 0
    clients.append(client)

    # Wait for both players to join
    while len(clients) < 2:
        send_message(client, "Waiting for another player...")
        time.sleep(1)

    send_message(client, "Game starting!")

    # Send questions
    for q in questions:
        broadcast(f"Question: {q['question']}")
        
        start_time = time.time()  # Start timer
        answered = {}  # Track answers per player

        # Start countdown timer in a thread for each client
        timer_threads = []
        for c in clients:
            thread = threading.Thread(target=countdown_timer, args=(20, c), daemon=True)
            thread.start()
            timer_threads.append(thread)

        # Collect answers with timeout
        for c in clients:
            c.settimeout(20)  # Set 20-second timeout for response
            try:
                answer = c.recv(1024).decode()
                answered[c] = answer  # Store answer
            except socket.timeout:
                answered[c] = "No Answer"  # Mark as "No Answer"
        
        # Evaluate answers
        for c, answer in answered.items():
            player_index = clients.index(c)
            player_username = usernames[player_index]

            if answer == "No Answer":
                send_message(c, "No Answer")  # Show "No Answer" only to that user
            
            if answer.lower() == q["answer"].lower():
                scores[player_username] += 1

    # Find highest score
    max_score = max(scores.values())

    # Check for tie
    winners = [user for user, score in scores.items() if score == max_score]

    if len(winners) > 1:
        broadcast(f"It's a tie! Players {', '.join(winners)} all scored {max_score} points!")
    else:
        broadcast(f"The winner is {winners[0]} with {max_score} points!")

    # Close connections
    for client in clients:
        client.close()
    clients.clear()

def start_server():
    """Start the server and handle incoming clients."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Server started. Waiting for connections...")

    while len(clients) < 2:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_server()
