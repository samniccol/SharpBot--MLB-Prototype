import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime, timedelta



WATCHLIST_FILE = "watchlist.json"

# Example hardcoded games for now
AVAILABLE_GAMES = fetch_live_odds = [
    {"game_id": "yankees-vs-redsox-20250628", "start_time": "2025-06-28T19:05:00"},
    {"game_id": "dodgers-vs-giants-20250628", "start_time": "2025-06-28T21:10:00"}
]

def load_watchlist():
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f, indent=2)

def add_game(game):
    watchlist = load_watchlist()
    if not any(g["game_id"] == game["game_id"] for g in watchlist):
        watchlist.append(game)
        save_watchlist(watchlist)
        messagebox.showinfo("✅ Added", f"{game['game_id']} added to watchlist!")
    else:
        messagebox.showwarning("⚠️ Already Exists", "Game is already in the watchlist.")

def remove_game(game_id):
    watchlist = load_watchlist()
    watchlist = [g for g in watchlist if g["game_id"] != game_id]
    save_watchlist(watchlist)
    messagebox.showinfo("❌ Removed", f"{game_id} removed from watchlist.")

def build_gui():
    root = tk.Tk()
    root.title("Watchlist Manager")

    tk.Label(root, text="Available Games").pack()

    for game in AVAILABLE_GAMES:
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text=game["game_id"]).pack(side="left")
        tk.Button(frame, text="Add", command=lambda g=game: add_game(g)).pack(side="left")

    tk.Label(root, text="Remove Game (type exact ID):").pack(pady=10)
    entry = tk.Entry(root)
    entry.pack()

    def remove_action():
        gid = entry.get().strip()
        if gid:
            remove_game(gid)

    tk.Button(root, text="Remove", command=remove_action).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
