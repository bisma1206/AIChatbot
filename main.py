import requests
import tkinter as tk
from tkinter import scrolledtext, Frame, Label, filedialog
from PIL import Image, ImageTk
import io
import time

# OpenRouter API Key
API_KEY = "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"

# Function to call the API
def chat_with_gpt(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI chatbot."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle sending messages
def send_message(event=None):
    user_input = user_entry.get()
    if not user_input.strip():
        return
    
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "\nYou: ", "user")
    chat_display.insert(tk.END, user_input + "\n")
    
    chat_display.insert(tk.END, "Chatbot is typing...\n", "typing")
    chat_display.config(state=tk.DISABLED)
    root.update()
    
    time.sleep(1)  # Simulate chatbot typing delay
    chat_display.config(state=tk.NORMAL)
    chat_display.delete("end-2l", "end-1l")  # Remove typing indicator
    
    response = chat_with_gpt(user_input)
    chat_display.insert(tk.END, "Chatbot: ", "bot")
    chat_display.insert(tk.END, response + "\n\n")
    
    chat_display.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)
    root.update()

# Create main chat window
root = tk.Tk()
root.title("GreenHeaven AI Chatbot")
root.geometry("320x500")  # Adjusted size for a sleek look
root.resizable(False, False)
root.configure(bg="#E3F2FD")  # Light blue background for a modern feel

# Header Frame
header_frame = Frame(root, bg="#1B5E20", height=50)
header_frame.pack(fill=tk.X)
Label(header_frame, text=" 🌿 GreenHeaven AI Chatbot", fg="white", bg="#1B5E20", font=("Arial", 14, "bold"), padx=10).pack(side=tk.LEFT, pady=10)

# Load chatbot icon
icon_url = "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"
response = requests.get(icon_url)
icon_data = Image.open(io.BytesIO(response.content))
icon_data = icon_data.resize((50, 50), Image.LANCZOS)
chatbot_icon = ImageTk.PhotoImage(icon_data)

# Icon Display
icon_label = Label(root, image=chatbot_icon, bg="#E3F2FD")
icon_label.pack(pady=5)

# Chat Display Box
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=38, height=14, font=("Arial", 11), bg="#FFFFFF", fg="#000000", bd=3, relief=tk.FLAT)
chat_display.pack(padx=10, pady=5)
chat_display.config(state=tk.DISABLED)

# Styling chat display
chat_display.tag_config("user", foreground="#FFFFFF", background="#4CAF50", font=("Arial", 11, "bold"))  # User text in green
chat_display.tag_config("bot", foreground="#000000", background="#D3D3D3", font=("Arial", 11, "italic"))  # Bot text in gray
chat_display.tag_config("typing", foreground="#2E7D32", font=("Arial", 11, "italic"))

# Input Frame
input_frame = Frame(root, bg="#E3F2FD")
input_frame.pack(pady=5)

# Input Field
user_entry = tk.Entry(input_frame, font=("Arial", 12), width=22, bg="#FFFFFF", fg="#000000", bd=2, relief=tk.GROOVE)
user_entry.pack(side=tk.LEFT, padx=5, ipady=4)
user_entry.bind("<Return>", send_message)

# Load send button icon
send_icon_url = "https://cdn-icons-png.flaticon.com/512/786/786205.png"
response = requests.get(send_icon_url)
send_icon_data = Image.open(io.BytesIO(response.content))
send_icon_data = send_icon_data.resize((28, 28), Image.LANCZOS)
send_icon = ImageTk.PhotoImage(send_icon_data)

# Send Button
send_button = tk.Button(input_frame, image=send_icon, bg="#1B5E20", bd=0, command=send_message, relief=tk.FLAT, activebackground="#1B5E20")
send_button.pack(side=tk.RIGHT)

# Run the chatbot GUI
root.mainloop()
