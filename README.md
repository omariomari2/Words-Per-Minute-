# Speed Typing Test
A terminal-based typing speed test application built with Python and curses. 
Test and improve your typing speed with real-time WPM (Words Per Minute) tracking and accuracy measurements.

## Demo
[Speed Typing Test Demo](./demo.gif)

## Features
- Real-time WPM calculation
- Accuracy tracking
- Color-coded feedback (green for correct, red for incorrect)
- Text wrapping for longer passages
- Statistics tracking (average WPM, maximum WPM, recent scores)
- Custom text support through external file
- Clean terminal UI with borders

## Prerequisites
- Python 3.6 or higher
- Windows users will need to install windows-curses:
  ```bash
  pip install windows-curses
  ```

## Installation
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/speed-typing-test.git
   cd speed-typing-test
   ```
2. (Optional) Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies (Windows users only)
   ```bash
   pip install windows-curses  # Only for Windows users
   ```

## Usage
1. (Optional) Create a `text.txt` file in the same directory with custom typing passages:
   ```bash
   echo "Your custom typing text here." > text.txt
   ```
2. Run the program:
   ```bash
   python WPM.py
   ```
3. Controls:
   - Type the displayed text
   - Backspace to correct mistakes
   - ESC to exit
   - Any key to start a new test
   - 'r' to replay after completing a test

## Custom Text Format
Create a `text.txt` file with your own typing passages. Separate different passages with blank lines:
