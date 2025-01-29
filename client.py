import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Client settings
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
client = None  # Initialize the client globally

def connect_to_server(username, text_area):
    """Connect to the server and handle communication."""
    global client  # Use the global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    client.send(username.encode())

    def listen_to_server():
        """Listen to messages from the server."""
        while True:
            try:
                message = client.recv(1024).decode()
                text_area.insert(tk.END, message + "\n")
            except:
                break

    threading.Thread(target=listen_to_server, daemon=True).start()

def send_answer(answer_entry):
    """Send the answer to the server."""
    if client:
        answer = answer_entry.get()
        if answer:
            client.send(answer.encode())
            answer_entry.delete(0, tk.END)

# GUI for the client
def client_gui():
    root = tk.Tk()
    root.title("General questions quiz game")

    # Set the entire window background to pink
    root.configure(bg='pink')

    # Username label with black text on white background
    username_label = tk.Label(root, text="Enter your username:", bg='pink', fg='gray')
    username_label.pack(pady=5)

    # Username entry with white background
    username_entry = tk.Entry(root, bg='white', fg='black')
    username_entry.pack(pady=5)

    # Text area for messages with white background
    text_area = tk.Text(root, height=15, width=50, bg='white', fg='black')
    text_area.pack(pady=10)

    # Answer entry with white background
    answer_entry = tk.Entry(root, bg='white', fg='black')
    answer_entry.pack(pady=5)

    # Connect button with black background and white text
    connect_button = tk.Button(
        root, text="Connect", bg='white', fg='pink',  # Black background, white text
        command=lambda: connect_to_server(username_entry.get(), text_area)
    )
    connect_button.pack(pady=5)

    # Send button with black background and white text
    send_button = tk.Button(
        root, text="Send Answer", bg='turquoise', fg='white',  # Black background, white text
        command=lambda: send_answer(answer_entry)
    )
    send_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    client_gui()
