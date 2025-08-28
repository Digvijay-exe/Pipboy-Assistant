import tkinter as tk
from tkinter import scrolledtext
import requests
import threading



# Groq API key
GROQ_API_KEY = "YOUR_GROQ_API"

# Function to ask Pipboy (Groq API)
def ask_scan(question):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are Pipboy, an intelligent, witty, and efficient assistant. Always address the user as 'Captain' in every"},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Run GUI
def run_gui():
    root = tk.Tk()
    root.title("Pipboy")
    root.geometry("700x550")

    # Initial settings
    dark_mode_enabled = False
    voice_enabled = True

    # Colors
    default_bg = "#000000"
    default_fg = "#00ffff"
    dark_bg = "#121212"
    neon_blue = "#00ffff"

    # Apply theme
    def apply_theme():
        if dark_mode_enabled:
            root.configure(bg=dark_bg)
            input_box.configure(bg=dark_bg, fg=neon_blue, insertbackground=neon_blue)
            output_box.configure(bg=dark_bg, fg=neon_blue, insertbackground=neon_blue)
        else:
            root.configure(bg=default_bg)
            input_box.configure(bg=default_bg, fg=default_fg, insertbackground=default_fg)
            output_box.configure(bg=default_bg, fg=default_fg, insertbackground=default_fg)

    # GUI elements
    tk.Label(root, text="Ask Pipboy anything:", font=("Helvetica", 12)).pack(pady=10)

    input_box = tk.Entry(root, width=80)
    input_box.pack(pady=5)

    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    output_box.pack(pady=10)


    # Ask and display
    def on_submit():
        question = input_box.get()
        if question.strip():
            output_box.insert(tk.END, f"You: {question}\n", "bold")
            input_box.delete(0, tk.END)

            def handle_response():
                answer = ask_scan(question)
                output_box.insert(tk.END, f"Pipboy: {answer}\n\n")
                output_box.see(tk.END)

            threading.Thread(target=handle_response).start()

    # Submit button
    submit_btn = tk.Button(root, text="Ask Pipboy", command=on_submit)
    submit_btn.pack(pady=5)


    apply_theme()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
