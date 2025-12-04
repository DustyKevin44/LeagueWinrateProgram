import tkinter as tk
from tkinter import font as tkfont

class WinRateOverlay:
    """Transparent overlay window displaying win probability"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure transparent, always-on-top window"""
        self.root.title("Win Rate")
        
        # Make window transparent and always on top
        self.root.attributes('-alpha', 0.85)  # 85% opacity
        self.root.attributes('-topmost', True)
        
        # CRITICAL: Set to toolwindow to stay on top of fullscreen games
        self.root.attributes('-toolwindow', True)
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Set size and position (top-right corner)
        width = 150
        height = 80
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Dark background
        self.root.configure(bg='#1a1a1a')
        
        # Make window draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.do_move)
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        """Create UI elements"""
        # Title label
        self.title_label = tk.Label(
            self.root,
            text="Win Probability",
            font=tkfont.Font(family="Segoe UI", size=9),
            bg='#1a1a1a',
            fg='#cccccc'
        )
        self.title_label.pack(pady=(5, 0))
        
        # Win rate label (large)
        self.win_rate_label = tk.Label(
            self.root,
            text="---%",
            font=tkfont.Font(family="Segoe UI", size=24, weight="bold"),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        self.win_rate_label.pack(pady=(0, 5))
        
        # Status label (small)
        self.status_label = tk.Label(
            self.root,
            text="Waiting...",
            font=tkfont.Font(family="Segoe UI", size=8),
            bg='#1a1a1a',
            fg='#888888'
        )
        self.status_label.pack()
        
    def update_win_rate(self, win_probability):
        """
        Update displayed win rate.
        
        Args:
            win_probability: Float between 0 and 1
        """
        percentage = win_probability * 100
        self.win_rate_label.config(text=f"{percentage:.1f}%")
        
        # Color code based on win rate
        if percentage >= 60:
            color = '#4ade80'  # Green
        elif percentage >= 55:
            color = '#a3e635'  # Light green
        elif percentage >= 50:
            color = '#fbbf24'  # Yellow
        elif percentage >= 45:
            color = '#fb923c'  # Orange
        else:
            color = '#f87171'  # Red
            
        self.win_rate_label.config(fg=color)
        
    def update_status(self, status_text):
        """Update status message"""
        self.status_label.config(text=status_text)
        
    def run(self):
        """Start the overlay"""
        self.root.mainloop()
        
    def destroy(self):
        """Close the overlay"""
        self.root.destroy()


if __name__ == "__main__":
    # Test the overlay
    overlay = WinRateOverlay()
    
    # Simulate some updates
    import time
    import threading
    
    def test_updates():
        time.sleep(1)
        overlay.update_win_rate(0.65)
        overlay.update_status("Updated 1s ago")
        
        time.sleep(2)
        overlay.update_win_rate(0.52)
        overlay.update_status("Updated 3s ago")
        
        time.sleep(2)
        overlay.update_win_rate(0.38)
        overlay.update_status("Updated 5s ago")
    
    threading.Thread(target=test_updates, daemon=True).start()
    overlay.run()
