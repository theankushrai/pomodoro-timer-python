#!/usr/bin/env python3
"""
Pomodoro Timer

A customizable Pomodoro timer that helps you stay focused and productive.
Displays break windows on all virtual desktops when a break starts.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import sys
import ctypes
from ctypes import wintypes
import win32gui
import win32con
import win32api
import pythoncom
import pywintypes
import win32process
import os

class BreakManager:
    """Manages break windows across all virtual desktops"""
    
    def __init__(self, break_time, is_long_break, on_break_end):
        self.break_time = break_time
        self.is_long_break = is_long_break
        self.on_break_end = on_break_end
        self.windows = []
        self.running = True
        self.end_time = time.time() + break_time
        self.password = "iamdesparatetowork"
        self.timer_finished = False  # Track if timer has finished
        self.create_windows()
        self.update_timer()
    
    def create_windows(self):
        """Create break windows that should appear on all desktops"""
        # Create a single window that we'll try to make visible on all desktops
        self.create_break_window()
    
    def create_break_window(self):
        """Create a break window that should appear on all desktops"""
        try:
            # Create a new Tkinter window
            window = tk.Tk()
            
            # Set window properties
            window.title("Break Time!")
            window.configure(bg='#222')
            
            # Add content first (we'll make it fullscreen after)
            break_label = tk.Label(
                window,
                text="Take a break!",
                font=("Arial", 48, "bold"),
                bg="#222",
                fg="white"
            )
            break_label.pack(pady=(60, 20))
            
            # Add timer label
            time_left = max(0, int(self.end_time - time.time()))
            mins, secs = divmod(time_left, 60)
            timer_label = tk.Label(
                window,
                text=f"Break time: {mins:02d}:{secs:02d}",
                font=("Arial", 36),
                bg="#222",
                fg="white"
            )
            timer_label.pack(pady=10)
            window.timer_label = timer_label
            
            # Add wellness message
            wellness_msg = tk.Label(
                window,
                text="Relax! Look away from the screen, stretch your body, and rest your eyes.",
                font=("Arial", 18, "italic"),
                bg="#222",
                fg="#FFD700",
                wraplength=700,
                justify="center"
            )
            wellness_msg.pack(pady=(0, 30))
            
            # Only add password entry to the first window
            if not self.windows:
                password_frame = tk.Frame(window, bg="#222")
                password_frame.pack(pady=(10, 40))
                
                password_label = tk.Label(
                    password_frame,
                    text="Enter password to end break early:",
                    font=("Arial", 16),
                    bg="#222",
                    fg="white"
                )
                password_label.pack(side=tk.LEFT, padx=(0, 10))
                
                password_entry = tk.Entry(password_frame, show="*", font=("Arial", 16), width=20)
                password_entry.pack(side=tk.LEFT)
                password_entry.focus_set()
                
                def try_end_break(event=None):
                    if password_entry.get() == self.password:
                        self.end_break()
                    else:
                        password_entry.delete(0, tk.END)
                        password_label.config(text="Incorrect password. Try again:", fg="red")
                        window.after(1000, lambda: password_label.config(
                            text="Enter password to end break early:", 
                            fg="white"
                        ))
                
                submit_btn = tk.Button(
                    password_frame, 
                    text="Submit", 
                    font=("Arial", 14), 
                    command=try_end_break
                )
                submit_btn.pack(side=tk.LEFT, padx=(10, 0))
                password_entry.bind('<Return>', try_end_break)
                
                # Add resume button that will appear when break time is up
                resume_btn = tk.Button(
                    window,
                    text="Resume Working",
                    font=("Arial", 20, "bold"),
                    bg="#4CAF50",
                    fg="white",
                    activebackground="#357a38",
                    activeforeground="white",
                    command=self.end_break
                )
                resume_btn.pack(pady=40)
                window.resume_btn = resume_btn
                resume_btn.pack_forget()  # Hide initially
            
            # Now make the window fullscreen and topmost
            window.attributes('-fullscreen', True)
            window.attributes('-topmost', True)
            window.overrideredirect(True)  # Remove window decorations
            
            # Get window handle for Windows-specific operations
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            
            # Try to make window visible on all virtual desktops
            try:
                # This is the GUID for the virtual desktop manager
                IID_IVirtualDesktopManager = "{a5cd92ff-29be-454c-8d04-d82879fb3f1b}"
                CLSID_VirtualDesktopManager = "{aa509086-5ca9-4c25-8f95-589d3c07b48a}"
                
                # Try to get the virtual desktop manager
                shell32 = ctypes.windll.shell32
                shell32.CoInitialize(0)
                
                # Try to make the window visible on all desktops
                try:
                    # This is a best-effort approach
                    ctypes.windll.user32.SetWindowLongW(
                        hwnd,
                        -20,  # GWL_EXSTYLE
                        0x00080000  # WS_EX_APPWINDOW
                    )
                except Exception as e:
                    print(f"Could not set window style: {e}")
                
                # Make sure window is visible
                ctypes.windll.user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                
            except Exception as e:
                print(f"Error setting window properties: {e}")
            
            # Store the window
            self.windows.append(window)
            
            # Handle window close - prevent default closing
            def on_closing():
                # Don't allow window to be closed by clicking X
                pass
                
            window.protocol("WM_DELETE_WINDOW", on_closing)
            
            return window
            
        except Exception as e:
            print(f"Error creating break window: {e}")
            return None
    
    def update_timer(self):
        """Update the timer on all break windows"""
        if not self.running:
            return
            
        time_left = max(0, int(self.end_time - time.time()))
        
        # When timer reaches zero, show resume button but DON'T auto-close
        if time_left <= 0 and not self.timer_finished:
            self.timer_finished = True
            # Show the resume button when timer is finished
            for window in self.windows:
                try:
                    if window.winfo_exists() and hasattr(window, 'resume_btn'):
                        window.resume_btn.pack(pady=40)
                        # Update timer text to show it's finished
                        if hasattr(window, 'timer_label'):
                            window.timer_label.config(
                                text="Break time complete! Click Resume or enter password.",
                                fg="#4CAF50"  # Green color to indicate completion
                            )
                        window.update()
                except Exception as e:
                    print(f"Error showing resume button: {e}")
            
            # Don't call self.end_break() here - let user decide when to end
            # Just continue updating to keep the window alive
        
        # Update timer display if still counting down
        if time_left > 0:
            mins, secs = divmod(time_left, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            
            windows_to_remove = []
            for window in self.windows:
                try:
                    if window.winfo_exists():
                        if hasattr(window, 'timer_label'):
                            window.timer_label.config(text=f"Break time: {time_str}")
                            window.update()
                    else:
                        windows_to_remove.append(window)
                except Exception as e:
                    print(f"Error updating window: {e}")
                    windows_to_remove.append(window)
            
            # Remove any dead windows
            for window in windows_to_remove:
                if window in self.windows:
                    self.windows.remove(window)
        
        # Schedule the next update if we still have windows and timer is running
        if self.running and self.windows:
            self.windows[0].after(200, self.update_timer)
    
    def end_break(self):
        """End the break and close all windows - only called by user action"""
        if not self.running:
            return
            
        self.running = False
        
        # Close all windows
        for window in self.windows[:]:
            try:
                if window.winfo_exists():
                    window.destroy()
            except:
                pass
        
        self.windows = []
        
        # Notify the main application
        if self.on_break_end:
            self.on_break_end()


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

    def on_break_end(self):
        """Callback when break ends, either by timeout or user action"""
        self.is_break = False
        self.break_manager = None
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

    def start_break(self):
        """
        Start a break session. Creates break windows on all virtual desktops.
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
            
        # Calculate break time
        is_long_break = (self.current_session % 4 == 0)
        break_time = (self.long_break_min if is_long_break else self.short_break_min) * 60
        
        # Create break manager to handle windows on all desktops
        self.is_break = True
        self.break_manager = BreakManager(
            break_time=break_time,
            is_long_break=is_long_break,
            on_break_end=self.on_break_end
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()