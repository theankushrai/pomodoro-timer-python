# 🍅 Pomodoro Timer – Your Focus and Productivity Booster

Tired of losing focus during work sessions? This Python-based Pomodoro timer helps you maintain productivity with structured work and break intervals. Featuring multi-desktop support, your break reminders will follow you across all virtual desktops, ensuring you never miss a well-deserved break! ⏱️

## 💡 Why I Built This

As someone who values deep work and regular breaks, I needed a solution that:

- Enforces the Pomodoro technique with customizable intervals
- Ensures breaks are taken seriously with full-screen, multi-desktop notifications
- Prevents skipping breaks with password protection
- Provides clear visual and audio cues for session transitions
- Works seamlessly across virtual desktops

## 🚀 Key Features

- **Customizable Timer Settings** - Set your preferred work/break durations
- **Multi-Desktop Support** - Break windows appear on all virtual desktops
- **Password Protection** - Prevents skipping breaks without proper authorization
- **Visual & Audio Alerts** - Clear notifications for session transitions
- **Session Tracking** - Tracks your work sessions and long breaks
- **Responsive UI** - Clean, distraction-free interface

## 🧰 Tech Stack

- **Frontend**: Tkinter (Python's standard GUI library)
- **System Integration**: Windows API (win32gui, ctypes)
- **Dependencies**: 
  - `pywin32` - Windows API bindings
  - `ctypes` - Low-level Windows API access

## 🛠️ Installation

### Prerequisites
- Python 3.6 or higher
- Windows OS (for virtual desktop support)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pomodoro-timer-python.git
   cd pomodoro-timer-python
   ```

2. **Install dependencies**
   ```bash
   pip install pywin32
   ```

3. **Run the application**
   ```bash
   python pomodoro_timer.py
   ```

## 🖥️ Usage

1. **Set Your Preferences**
   - Work duration (default: 25 minutes)
   - Short break (default: 5 minutes)
   - Long break (default: 15 minutes)
   - Number of sessions before long break (default: 4)

2. **Start Working**
   - Click "Start Pomodoro" to begin your first work session
   - The timer will automatically transition between work and break sessions

3. **Taking Breaks**
   - When break time comes, full-screen windows will appear on all desktops
   - To end break early, enter the password (default: "iamdesparatetowork")
   - After completing all sessions, you'll be notified that your Pomodoro sequence is complete

## 🎛️ Customization

You can modify the following in the code:
- Default timer settings in the `PomodoroTimer` class
- Break window appearance in the `BreakManager` class
- Password protection in the `BreakManager.__init__` method

## 🎥 Tutorial & Media

### 📹 Video Tutorial
🚧 Coming Soon - A step-by-step video guide will be available shortly!

### 🖼️ Screenshots

#### Main Interface
🚧 Coming Soon - Screenshot of the main timer interface

#### Break Screen
🚧 Coming Soon - Screenshot of the full-screen break window

#### Settings
🚧 Coming Soon - Screenshot of the settings/preferences dialog

## 🔗 Find Me Online

For more of my projects, tutorials, and social links, visit my Linktree:

→ [https://linktr.ee/theankushrai](https://linktr.ee/theankushrai)

Linktree contains:
- GitHub
- Twitter
- LinkedIn
- Portfolio