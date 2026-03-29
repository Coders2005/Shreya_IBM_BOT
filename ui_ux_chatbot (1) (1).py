import tkinter as tk
from datetime import datetime

MENU = None

# Purple / neutrals (mobile-style chat)
PURPLE = "#6D28D9"
PURPLE_DARK = "#5B21B6"
BOT_BUBBLE = "#EDEBF5"
USER_BUBBLE = "#6D28D9"
BG_CHAT = "#FFFFFF"
TEXT_MUTED = "#6B7280"

KB = [
    {
        "kw": ("font", "typography", "typeface"),
        "q": "On mobile, typography means readable type at arm’s length: use few sizes, body near 16–17pt/sp, "
        "good contrast, line height ~1.35–1.5×.",
        "f": {
            "1": ("Font Types", "Sans-serif (SF Pro, Roboto) fits most UI. Serif fits editorial, not dense UI. "
            "One UI family + optional display brand font is plenty."),
            "2": ("Font Sizes", "Try caption ~12, body ~16–17, titles ~20–24. Avoid tiny text for important info; "
            "test large accessibility sizes."),
            "3": ("Font Pairing", "At most two families; match mood and x-height. When unsure, one family + weight/size is safest."),
        },
    },
    {
        "kw": ("color", "palette", "contrast"),
        "q": "Color sets hierarchy: neutrals for surfaces, a primary for main actions, semantic greens/reds for status. "
        "Check contrast in light and dark mode.",
        "f": {
            "1": ("Primary & Accent", "One strong primary; accents for promos. Too many bright colors fight—neutrals should dominate."),
            "2": ("Light vs Dark Mode", "Tune fills and borders; don’t only invert. Primaries may need a lighter tint on dark."),
            "3": ("Accessibility", "Never use color alone for meaning. Aim for WCAG text contrast; try color-blind checks."),
        },
    },
    {
        "kw": ("layout", "spacing", "grid", "margin"),
        "q": "Use a simple column layout, 8-point spacing rhythm, group related items, add space between sections. "
        "Respect notch and home-indicator safe areas.",
        "f": {
            "1": ("8-Point Grid", "Pad and gap in 8s (4 inside tight components). Makes handoff faster and screens calmer."),
            "2": ("Visual Hierarchy", "Size, weight, and contrast show what matters first—one main focus per screen helps."),
            "3": ("Scroll & Fold", "Key actions up top when possible; long flows need progress and a clear primary action."),
        },
    },
    {
        "kw": ("button", "touch", "tap", "target"),
        "q": "Touch targets ~44×44 pt (iOS) or 48×48 dp (Material). Small icons OK if padding grows the hit box; "
        "space out competing taps.",
        "f": {
            "1": ("Hit Area vs Visual Size", "Glyphs can be small; tappable region must be big—note min sizes for developers."),
            "2": ("States", "Show default, pressed, disabled, loading. Disabled must not look clickable; block double submit."),
            "3": ("Thumb Reach", "Bottom zones are easier on big phones—place key actions where thumbs naturally reach."),
        },
    },
]


def find_topic(text):
    t = text.lower()
    for item in KB:
        if any(k in t for k in item["kw"]):
            return item
    return None


def format_menu(followups):
    lines = []
    for key in sorted(followups.keys(), key=int):
        lines.append(f"{key}. {followups[key][0]}")
    return "\n".join(lines)


def pick_number(msg):
    s = msg.strip()
    if s.isdigit() and len(s) <= 2:
        return s
    if len(s) == 2 and s[0].isdigit() and s[1] in ").":
        return s[0]
    return None


def now_time():
    return datetime.now().strftime("%H:%M")


# —— UI refs (set in main) ——
root = chat_inner = chat_canvas = None
entry = None
PLACEHOLDER = "Ask me anything about mobile UI or UX…"


def scroll_chat_bottom():
    if not chat_canvas:
        return
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)


def add_bubble(text, is_user):
    row = tk.Frame(chat_inner, bg=BG_CHAT)
    row.pack(fill=tk.X, padx=10, pady=6)

    side = tk.RIGHT if is_user else tk.LEFT
    inner = tk.Frame(row, bg=BG_CHAT)
    inner.pack(side=side)

    av = "🙂" if is_user else "🤖"
    bubble_bg = USER_BUBBLE if is_user else BOT_BUBBLE
    fg = "#FFFFFF" if is_user else "#1F2937"

    if is_user:
        col = tk.Frame(inner, bg=BG_CHAT)
        col.pack(side=tk.RIGHT)
        tk.Label(col, text=av, font=("Segoe UI", 16), bg=BG_CHAT).pack(side=tk.RIGHT, anchor="s", padx=(4, 0))
        bcol = tk.Frame(col, bg=BG_CHAT)
        bcol.pack(side=tk.RIGHT)
        tk.Label(
            bcol,
            text=text,
            font=("Segoe UI", 10),
            bg=bubble_bg,
            fg=fg,
            wraplength=300,
            justify=tk.LEFT,
            padx=14,
            pady=10,
        ).pack(anchor="e")
        tk.Label(bcol, text=now_time(), font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CHAT).pack(anchor="e", pady=(2, 0))
    else:
        col = tk.Frame(inner, bg=BG_CHAT)
        col.pack(side=tk.LEFT)
        tk.Label(col, text=av, font=("Segoe UI", 16), bg=BG_CHAT).pack(side=tk.LEFT, anchor="s", padx=(0, 4))
        bcol = tk.Frame(col, bg=BG_CHAT)
        bcol.pack(side=tk.LEFT)
        tk.Label(
            bcol,
            text=text,
            font=("Segoe UI", 10),
            bg=bubble_bg,
            fg=fg,
            wraplength=300,
            justify=tk.LEFT,
            padx=14,
            pady=10,
        ).pack(anchor="w")
        tk.Label(bcol, text=now_time(), font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CHAT).pack(anchor="w", pady=(2, 0))

    chat_inner.update_idletasks()
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
    scroll_chat_bottom()


def on_send(event=None):
    global MENU
    raw = entry.get("1.0", "end-1c").strip()
    if raw == PLACEHOLDER or not raw:
        return
    entry.delete("1.0", tk.END)
    add_bubble(raw, True)

    n = pick_number(raw)
    if MENU and n in MENU:
        add_bubble(MENU[n][1], False)
        MENU = None
        return

    topic = find_topic(raw)
    if topic:
        MENU = dict(topic["f"])
        body = topic["q"] + "\n\n" + format_menu(topic["f"])
        add_bubble(body, False)
        return

    add_bubble("I focus on mobile UI and UX—things like fonts, colors, layout, and touch-friendly controls. Ask me about one of those!", False)
    MENU = None


def chip(text_to_send):
    entry.delete("1.0", tk.END)
    entry.insert("1.0", text_to_send)
    on_send()


def entry_focus_in(_):
    if entry.get("1.0", "end-1c") == PLACEHOLDER:
        entry.delete("1.0", tk.END)
        entry.config(fg="#111827")


def entry_focus_out(_):
    if not entry.get("1.0", "end-1c").strip():
        entry.insert("1.0", PLACEHOLDER)
        entry.config(fg=TEXT_MUTED)


def on_return_key(event):
    if event.state & 0x0001:
        return None
    on_send()
    return "break"


def build_ui():
    global root, chat_inner, chat_canvas, entry

    root = tk.Tk()
    root.title("Design Assistant")
    root.geometry("420x640")
    root.minsize(360, 480)
    root.configure(bg=BG_CHAT)

    chat_wrap = tk.Frame(root, bg=BG_CHAT)
    chat_wrap.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

    chat_canvas = tk.Canvas(chat_wrap, bg=BG_CHAT, highlightthickness=0)
    sb = tk.Scrollbar(chat_wrap, orient=tk.VERTICAL, command=chat_canvas.yview)
    chat_canvas.configure(yscrollcommand=sb.set)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    chat_inner = tk.Frame(chat_canvas, bg=BG_CHAT)
    win = chat_canvas.create_window((0, 0), window=chat_inner, anchor="nw")

    def on_inner_cfg(_):
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))

    def on_canvas_cfg(e):
        chat_canvas.itemconfig(win, width=e.width)

    chat_inner.bind("<Configure>", on_inner_cfg)
    chat_canvas.bind("<Configure>", on_canvas_cfg)

    def wheel_scroll(e):
        w = e.widget
        while w:
            if w == chat_wrap:
                chat_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
                return
            w = w.master

    root.bind_all("<MouseWheel>", wheel_scroll)

    chips_f = tk.Frame(root, bg="#F3F4F6")
    chips_f.pack(fill=tk.X, padx=10, pady=(8, 4))
    for label, q in (
        ("Fonts & type", "Tell me about fonts for mobile apps"),
        ("Color & contrast", "How should I use color on mobile?"),
        ("Layout & spacing", "Tips for layout and spacing"),
        ("Touch & buttons", "Touch targets and buttons"),
    ):
        tk.Button(
            chips_f,
            text=label,
            font=("Segoe UI", 9),
            bg="white",
            fg=PURPLE,
            activeforeground=PURPLE_DARK,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#DDD6FE",
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda t=q: chip(t),
        ).pack(side=tk.LEFT, padx=4, pady=6)

    bottom = tk.Frame(root, bg=BG_CHAT)
    bottom.pack(fill=tk.X, padx=10, pady=(4, 8))

    inp_row = tk.Frame(bottom, bg=BG_CHAT)
    inp_row.pack(fill=tk.X)
    inp_row.columnconfigure(0, weight=1)

    entry = tk.Text(
        inp_row,
        height=2,
        font=("Segoe UI", 10),
        wrap=tk.WORD,
        bg="white",
        fg=TEXT_MUTED,
        insertbackground="#111827",
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground="#E5E7EB",
        highlightcolor=PURPLE,
        padx=12,
        pady=8,
    )
    entry.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    entry.insert("1.0", PLACEHOLDER)
    entry.bind("<FocusIn>", entry_focus_in)
    entry.bind("<FocusOut>", entry_focus_out)
    entry.bind("<Return>", on_return_key)

    send_btn = tk.Button(
        inp_row,
        text="Send",
        font=("Segoe UI", 10, "bold"),
        bg=PURPLE,
        fg="white",
        activebackground=PURPLE_DARK,
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        command=on_send,
        padx=18,
        pady=10,
        width=6,
    )
    send_btn.grid(row=0, column=1, sticky="ns")

    tk.Label(
        bottom,
        text="Press Enter to send  ·  Shift+Enter for a new line",
        font=("Segoe UI", 8),
        fg=TEXT_MUTED,
        bg=BG_CHAT,
    ).pack(pady=(6, 0))

    add_bubble(
        "Hi — I’m here for mobile UI and UX: typography, color, layout, and touch-friendly patterns. "
        "Use a quick prompt below or type your own question.",
        False,
    )
    entry.focus_set()


if __name__ == "__main__":
    build_ui()
    root.mainloop()
