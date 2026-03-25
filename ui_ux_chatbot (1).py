import tkinter as tk
from tkinter import scrolledtext
import re

# Simple keyword-based responses
RESPONSES = {
    r"\bcolor\b|\bpalette\b": "For mobile, stick to a simple color palette. Use the 60-30-10 rule: 60% dominant color, 30% secondary, 10% accent.",
    r"\bbutton\b|\btouch\b": "Touch targets should be at least 44x44 points (or 48x48 dp) to ensure they are easily tappable with a finger.",
    r"\bfont\b|\btypography\b|\btext\b": "Use legible fonts. Body text should typically be at least 16sp. Sans-serif fonts like Roboto (Android) or San Francisco (iOS) work best.",
    r"\bnavigation\b|\bmenu\b": "Keep navigation simple. Bottom navigation bars are great for 3-5 top-level destinations, while hamburger menus can hold secondary options.",
    r"\baccessibility\b|\ba11y\b": "Ensure high contrast between text and background. Support dynamic sizing so users can increase text size if needed.",
    r"\banimation\b|\btransition\b": "Keep animations subtle and purposeful. They should guide the user's attention (around 200-300ms is ideal for mobile).",
    r"\blayout\b|\bspacing\b|\bgrid\b": "Use an 8pt grid system. Consistent margins and padding make the UI feel structured and readable.",
    r"\bhello\b|\bhi\b|\bhey\b": "Hello! I'm your Mobile UI/UX Assistant. Ask me about colors, layouts, buttons, fonts, navigation, or accessibility!",
    r"\bbye\b|\bexit\b|\bquit\b": "Goodbye! Keep designing great mobile experiences!",
}

def get_bot_response(user_input):
    user_input = user_input.lower()
    for pattern, response in RESPONSES.items():
        if re.search(pattern, user_input):
            return response
    return "I'm a basic UI/UX assistant. Try asking me specifically about colors, buttons, fonts, layouts, navigation, or accessibility!"

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile UI/UX Assistant")
        self.root.geometry("400x500")
        
        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Arial", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure text colors for chat bubbles
        self.chat_area.tag_config('user', foreground='#0056b3')
        self.chat_area.tag_config('bot', foreground='#333333')
        
        # Input area frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Text entry field
        self.user_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_entry.bind("<Return>", self.send_message)
        
        # Send button
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message, bg="#007BFF", fg="white", font=("Arial", 10, "bold"))
        self.send_btn.pack(side=tk.RIGHT)
        
        # Welcome message
        self.display_message("Bot", "Hello! I'm your Mobile UI/UX Assistant. Ask me about colors, buttons, fonts, navigation, or accessibility!", 'bot')

    def send_message(self, event=None):
        msg = self.user_entry.get().strip()
        if not msg:
            return
            
        # Clear input field
        self.user_entry.delete(0, tk.END)
        
        # Display user message
        self.display_message("You", msg, 'user')
        
        # Check for quit
        if msg.lower() in ['exit', 'quit', 'bye']:
            self.display_message("Bot", "Goodbye!", 'bot')
            self.root.after(1500, self.root.destroy)
            return

        # Get and display bot response
        response = get_bot_response(msg)
        self.display_message("Bot", response, 'bot')

    def display_message(self, sender, message, tag):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
