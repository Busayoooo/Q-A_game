import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Client settings
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
client = None  # Initialize the client globally

def connect_to_server(username, text_area, connect_button):
    """Connects to the server and starts listening for messages."""
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    client.connect((SERVER_HOST, SERVER_PORT))  # Connect to the server

    # Send the username to the server
    client.send(username.encode())

    # Disable the connect button and change its background color to blend in
    connect_button.config(state=tk.DISABLED, bg="pink", fg="pink")  

    def listen_to_server():
        """Listens to messages from the server and updates the GUI."""
        while True:
            try:
                message = client.recv(1024).decode()  # Receive message from server
                text_area.insert(tk.END, message + "\n")  # Insert message into the text area
            except:
                break  # Stop if there's an error (e.g., server disconnects)

    # Start a new thread to listen for messages
    threading.Thread(target=listen_to_server, daemon=True).start()

def send_answer(answer_entry):
    """Sends the user's answer to the server."""
    if client:  # Check if the client is connected
        answer = answer_entry.get()  # Get the text from the answer entry field
        if answer:
            client.send(answer.encode())  # Send the answer to the server
            answer_entry.delete(0, tk.END)  # Clear the input field after sending

# GUI for the client
def client_gui():
    """Creates the graphical user interface (GUI) for the client."""
    root = tk.Tk()  # Initialize the main window
    root.title("General Questions Quiz Game")  # Set window title

    # Set the entire window background to pink
    root.configure(bg='pink')

    # Username label
    username_label = tk.Label(root, text="Enter your username:", bg='pink', fg='black')
    username_label.pack(pady=5)

    # Username entry field
    username_entry = tk.Entry(root, bg='white', fg='black')
    username_entry.pack(pady=5)

    # Text area to display messages
    text_area = tk.Text(root, height=15, width=50, bg='white', fg='black')
    text_area.pack(pady=10)

    # Answer entry field
    answer_entry = tk.Entry(root, bg='white', fg='black')
    answer_entry.pack(pady=5)

    # Button to connect to the server
    connect_button = tk.Button(
        root, text="Connect", bg='white', fg='pink',  # Button color settings
        command=lambda: connect_to_server(username_entry.get(), text_area, connect_button)  # Call connect function
    )
    connect_button.pack(pady=5)

    # Button to send an answer
    send_button = tk.Button(
        root, text="Send Answer", bg='turquoise', fg='white',  # Button color settings
        command=lambda: send_answer(answer_entry)  # Call send function
    )
    send_button.pack(pady=5)

    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    client_gui()
