import socket
import threading
from tkinter import *
from tkinter import scrolledtext
from cryptography.fernet import Fernet

# Client class to manage connection and encryption
class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("BAK-BAK MACHINE")
        self.master.geometry("500x500")
        self.master.config(bg='#FAFAFA')

        # Header bar (like Instagram chat header)
        self.header_frame = Frame(master, bg='#ffffff', height=50)
        self.header_frame.pack(fill=X)

        self.header_label = Label(self.header_frame, text="Encrypted Chat", bg='#ffffff', fg='#262626', font=("Helvetica", 14, "bold"))
        self.header_label.pack(pady=10)

        # Chat window (like Instagram's chat background, white with grey text)
        self.chat_window = scrolledtext.ScrolledText(master, wrap=WORD, width=50, height=20, bg='#FAFAFA', fg='#262626', font=('Helvetica', 12), bd=0)
        self.chat_window.pack(padx=10, pady=10)
        self.chat_window.config(state=DISABLED)

        # Bottom frame for message entry and send button
        self.bottom_frame = Frame(master, bg='#FAFAFA')
        self.bottom_frame.pack(side=BOTTOM, fill=X, pady=10)

        # Entry widget for typing messages (rounded and with border like Instagram)
        self.message_entry = Entry(self.bottom_frame, width=40, font=('Helvetica', 12), bg='#EFEFEF', fg='#262626', bd=0)
        self.message_entry.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=8)
        self.message_entry.config(highlightthickness=1, highlightbackground='#DBDBDB')
        self.message_entry.bind("<Return>", self.send_message)

        # Send button (round button similar to Instagram send)
        self.send_button = Button(self.bottom_frame, text="Send", bg='#0095F6', fg='white', font=("Helvetica", 10, "bold"), relief=FLAT, width=8, height=1, command=self.send_message, bd=0)
        self.send_button.grid(row=0, column=1, padx=7)

        # Initialize socket connection
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 12345))

        # Encryption key input
        encryption_key = input("Enter the encryption key: ").encode()
        self.cipher_suite = Fernet(encryption_key)

        # Start a thread for receiving messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
                    self.display_message(f"Server: {decrypted_message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_message(self, event=None):
    	message = self.message_entry.get()
    	if message:
        	encrypted_message = self.cipher_suite.encrypt(message.encode())
        	print(f"Message: {encrypted_message}")  # Show the encrypted version
        	self.client_socket.send(encrypted_message)
        	self.display_message(f"You: {message}")
        	self.message_entry.delete(0, END)



    def display_message(self, message):
        self.chat_window.config(state=NORMAL)
        self.chat_window.insert(END, message + "\n")
        self.chat_window.config(state=DISABLED)
        self.chat_window.yview(END)

if __name__ == "__main__":
    root = Tk()
    client = ChatClient(root)
    root.mainloop()
