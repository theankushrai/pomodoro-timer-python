#!/usr/bin/env python3
"""
Pomodoro Timer

A customizable Pomodoro timer that helps you stay focused and productive.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import sys

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer Setup")
        # Increased window size to ensure all widgets, including the Start button, are visible
        self.root.geometry("500x400")
        # Optionally, make window non-resizable to avoid accidental hiding
        self.root.resizable(False, False)
        
        # Initialize variables
        self.work_time = tk.StringVar(value="25")  # Default 25 minutes
        self.short_break = tk.StringVar(value="5")  # Default 5 minutes
        self.long_break = tk.StringVar(value="15")  # Default 15 minutes
        self.sessions = tk.StringVar(value="4")  # Default 4 sessions
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Set up the initial user interface for inputting Pomodoro parameters.
        """
        # Create main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text="Pomodoro Timer Setup", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Work time input
        ttk.Label(main_frame, text="Work Time (minutes):").pack(anchor='w', pady=(5, 0))
        work_entry = ttk.Entry(main_frame, textvariable=self.work_time, width=10)
        work_entry.pack(anchor='w', pady=(0, 10))
        
        # Short break input
        ttk.Label(main_frame, text="Short Break (minutes):").pack(anchor='w', pady=(5, 0))
        short_break_entry = ttk.Entry(main_frame, textvariable=self.short_break, width=10)
        short_break_entry.pack(anchor='w', pady=(0, 10))
        
        # Long break input
        ttk.Label(main_frame, text="Long Break (minutes - after 4 sessions):").pack(anchor='w', pady=(5, 0))
        long_break_entry = ttk.Entry(main_frame, textvariable=self.long_break, width=10)
        long_break_entry.pack(anchor='w', pady=(0, 10))
        
        # Number of sessions input
        ttk.Label(main_frame, text="Number of Work Sessions:").pack(anchor='w', pady=(5, 0))
        sessions_entry = ttk.Entry(main_frame, textvariable=self.sessions, width=10)
        sessions_entry.pack(anchor='w', pady=(0, 20))
        
        # Start button
        start_button = ttk.Button(main_frame, text="Start Pomodoro", command=self.start_timer)
        start_button.pack(pady=10)

    def start_timer(self):
        """
        Called when the user clicks the Start Pomodoro button. Validates user input and starts the timer sequence.
        """
        try:
            # Validate and parse user inputs
            self.work_min = int(self.work_time.get())
            self.short_break_min = int(self.short_break.get())
            self.long_break_min = int(self.long_break.get())
            self.total_sessions = int(self.sessions.get())
            # Ensure all values are positive
            if (self.work_min <= 0 or self.short_break_min <= 0 or 
                self.long_break_min <= 0 or self.total_sessions <= 0):
                raise ValueError("All values must be positive numbers")
            # Close setup window and start the timer
            self.root.destroy()
            self.run_pomodoro()
        except ValueError as e:
            # Show error if input is invalid
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers for all fields")

    def run_pomodoro(self):
        """
        Start the Pomodoro timer sequence. Initializes session tracking and begins the first work session.
        """
        self.current_session = 1    # Track current session number
        self.is_break = False       # Flag to track if in break mode
        self.running = True         # Control flag for the timer loop
        self.break_window = None    # Reference to break window (if any)
        # Start the first work session
        self.start_work_session()

    def start_work_session(self):
        """
        Start a work session. Displays a countdown in the terminal and waits for the session to complete.
        Plays a short beep at the start.
        """
        # Play a short beep to indicate work session start
        try:
            import winsound
            winsound.Beep(1000, 300)  # 1000 Hz for 300 ms
        except Exception:
            pass  # Ignore if sound fails
        print(f"Starting work session {self.current_session}...")
        for i in range(self.work_min * 60, 0, -1):
            if not self.running:
                break
            mins, secs = divmod(i, 60)
            print(f"{mins:02d}:{secs:02d}", end='\r')
            time.sleep(1)
        print("\nWork session complete!")
        self.start_break()

    def start_break(self):
        """
        Start a break session. Displays a fullscreen overlay with the break time and waits for the break to complete.
        Plays a double beep at the start.
        """
        # Play a double beep to indicate break start
        try:
            import winsound
            winsound.Beep(600, 200)  # 600 Hz for 200 ms
            time.sleep(0.1)
            winsound.Beep(800, 200)  # 800 Hz for 200 ms
        except Exception:
            pass  # Ignore if sound fails
        if self.current_session % 4 == 0:
            break_time = self.long_break_min * 60
        else:
            break_time = self.short_break_min * 60
        self.is_break = True
        self.break_window = tk.Tk()
        self.break_window.title("Break Time!")
        # Make the break overlay truly fullscreen
        self.break_window.attributes('-fullscreen', True)
        # Optionally, keep it always on top
        self.break_window.attributes('-topmost', True)
        # Set background color for better visibility
        self.break_window.configure(bg="#222")
        break_label = tk.Label(
            self.break_window,
            text="Take a break!",
            font=("Arial", 48, "bold"),
            bg="#222",
            fg="white"
        )
        break_label.pack(pady=(60, 20))  # Space above for aesthetics

        # --- Wellness Message Section ---
        # Add a motivational wellness message below the timer
        wellness_msg = tk.Label(
            self.break_window,
            text="Relax! Look away from the screen, stretch your body, and rest your eyes.",
            font=("Arial", 18, "italic"),
            bg="#222",
            fg="#FFD700",  # Gold color for emphasis
            wraplength=700,
            justify="center"
        )
        wellness_msg.pack(pady=(0, 30))

        # --- Password Entry Section ---
        # Frame to hold password entry and label
        password_frame = tk.Frame(self.break_window, bg="#222")
        password_frame.pack(pady=(10, 40))

        # Label for password prompt
        password_label = tk.Label(
            password_frame,
            text="Enter password to end break early:",
            font=("Arial", 16),
            bg="#222",
            fg="white"
        )
        password_label.pack(side=tk.LEFT, padx=(0, 10))

        # Entry field for password
        password_entry = tk.Entry(password_frame, show="*", font=("Arial", 16), width=20)
        password_entry.pack(side=tk.LEFT)
        password_entry.focus_set()

        # Function to check password and end break if correct
        def try_end_break(event=None):
            if password_entry.get() == "iamdesparatetowork":
                # If password is correct, destroy the break window and end break
                self.break_window.destroy()
                self.is_break = False
                self.running = True  # Ensure running is True for next session
                self.current_session += 1
                if self.current_session <= self.total_sessions:
                    self.start_work_session()
                else:
                    print("Pomodoro sequence complete!")
            else:
                # If password is wrong, show error and clear entry
                password_entry.delete(0, tk.END)
                password_label.config(text="Incorrect password. Try again:", fg="red")
                self.break_window.after(1000, lambda: password_label.config(text="Enter password to end break early:", fg="white"))

        # Button to submit password
        submit_btn = tk.Button(password_frame, text="Submit", font=("Arial", 14), command=try_end_break)
        submit_btn.pack(side=tk.LEFT, padx=(10, 0))
        # Bind Enter key to password check
        password_entry.bind('<Return>', try_end_break)

        # --- Timer Update Section ---
        for i in range(break_time, 0, -1):
            if not self.running or not self.break_window.winfo_exists():
                break
            mins, secs = divmod(i, 60)
            break_label.config(text=f"Break time: {mins:02d}:{secs:02d}")
            self.break_window.update()
            time.sleep(1)

        # --- Resume Working Button Section ---
        if self.break_window.winfo_exists():
            # After break ends, show the Resume Working button
            resume_btn = tk.Button(
                self.break_window,
                text="Resume Working",
                font=("Arial", 20, "bold"),
                bg="#4CAF50",
                fg="white",
                activebackground="#357a38",
                activeforeground="white",
                command=lambda: on_resume_click()
            )
            resume_btn.pack(pady=40)

            # Function to handle Resume Working button click
            def on_resume_click():
                self.break_window.destroy()
                self.is_break = False
                self.current_session += 1
                if self.current_session <= self.total_sessions:
                    self.start_work_session()
                else:
                    # Play a long beep to indicate all sessions are complete
                    try:
                        import winsound
                        winsound.Beep(1200, 700)  # 1200 Hz for 700 ms
                    except Exception:
                        pass
                    print("Pomodoro sequence complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()