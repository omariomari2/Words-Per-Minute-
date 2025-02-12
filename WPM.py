import curses
from curses import wrapper
import time
import random

def draw_border(stdscr):
	# Get window dimensions
	height, width = stdscr.getmaxyx()
	
	# Draw top and bottom borders (subtract 1 from height to avoid bottom-right corner)
	stdscr.addstr(0, 0, "+" + "-" * (width-2) + "+")
	stdscr.addstr(height-2, 0, "+" + "-" * (width-2) + "+")  # Changed from height-1 to height-2
	
	# Draw side borders (adjust range to match new bottom border)
	for y in range(1, height-2):  # Changed from height-1 to height-2
		stdscr.addstr(y, 0, "|")
		stdscr.addstr(y, width-1, "|")

def center_text(stdscr, text, y_offset=0):
	height, width = stdscr.getmaxyx()
	x = width//2 - len(text)//2
	y = height//2 + y_offset
	stdscr.addstr(y, x, text)

def start_screen(stdscr):
	stdscr.clear()
	draw_border(stdscr)
	
	# Add title with a box around it
	title = "SPEED TYPING TEST"
	height, width = stdscr.getmaxyx()
	title_y = height//4
	title_x = width//2 - len(title)//2
	
	# Draw box around title
	stdscr.addstr(title_y-1, title_x-2, "+" + "-" * (len(title)+2) + "+")
	stdscr.addstr(title_y, title_x-2, "|" + " " * (len(title)+2) + "|")
	stdscr.addstr(title_y+1, title_x-2, "+" + "-" * (len(title)+2) + "+")
	
	# Add title in green
	stdscr.attron(curses.color_pair(1))
	stdscr.addstr(title_y, title_x, title)
	stdscr.attroff(curses.color_pair(1))
	
	# Add instructions
	center_text(stdscr, "Press any key to begin!", 2)
	center_text(stdscr, "ESC to exit", 4)
	
	stdscr.refresh()
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
	height, width = stdscr.getmaxyx()
	
	# Draw border
	draw_border(stdscr)
	
	# Display WPM in top-right corner
	stdscr.addstr(1, width-15, f"WPM: {wpm}")
	
	# Break target text into wrapped lines
	words = target.split()
	lines = []
	current_line = []
	current_length = 0
	max_width = width - 20  # Leave margin on both sides
	
	for word in words:
		if current_length + len(word) + 1 <= max_width:
			current_line.append(word)
			current_length += len(word) + 1
		else:
			lines.append(' '.join(current_line))
			current_line = [word]
			current_length = len(word) + 1
	if current_line:
		lines.append(' '.join(current_line))
	
	# Display wrapped text
	target_y = height//3
	for i, line in enumerate(lines):
		target_x = width//2 - len(line)//2
		stdscr.addstr(target_y + i, target_x, line)
	
	# Display current text with color coding
	current_string = "".join(current)
	pos = 0
	for i, char in enumerate(current_string):
		line_idx = 0
		while line_idx < len(lines):
			if pos < len(lines[line_idx]):
				correct_char = lines[line_idx][pos]
				x = width//2 - len(lines[line_idx])//2 + pos
				y = target_y + line_idx
				
				if char == correct_char:
					color = curses.color_pair(1)  # Green for correct
				else:
					color = curses.color_pair(2)  # Red for incorrect
					
				stdscr.attron(color)
				stdscr.addstr(y, x, char)
				stdscr.attroff(color)
				break
			pos -= len(lines[line_idx])
			line_idx += 1
		pos += 1
	
	# Add cursor at current position
	if len(current) < len(target):
		pos = len(current)
		line_idx = 0
		while line_idx < len(lines):
			if pos < len(lines[line_idx]):
				cursor_x = width//2 - len(lines[line_idx])//2 + pos
				cursor_y = target_y + line_idx
				stdscr.addstr(cursor_y, cursor_x, "_", curses.color_pair(3))
				break
			pos -= len(lines[line_idx])
			line_idx += 1

def load_text():
	try:
		with open("text.txt", "r") as f:
			paragraphs = f.read().split('\n\n')  # Split by double newline to get paragraphs
			if not paragraphs:
				return "Default text if file is empty."
			return random.choice(paragraphs).replace('\n', ' ').strip()
	except FileNotFoundError:
		return "Default text if file not found."
	except Exception as e:
		return f"Error occurred: {str(e)}"

def display_stats(stdscr, wpm_history):
	stdscr.clear()
	draw_border(stdscr)
	
	# Calculate statistics
	avg_wpm = sum(wpm_history) / len(wpm_history) if wpm_history else 0
	max_wpm = max(wpm_history) if wpm_history else 0
	
	# Display title
	title = "YOUR TYPING STATISTICS"
	height, width = stdscr.getmaxyx()
	title_y = height//4
	title_x = width//2 - len(title)//2
	
	# Draw box around stats
	stdscr.addstr(title_y-1, title_x-2, "+" + "-" * (len(title)+2) + "+")
	stdscr.addstr(title_y, title_x-2, "|" + " " * (len(title)+2) + "|")
	stdscr.addstr(title_y+1, title_x-2, "+" + "-" * (len(title)+2) + "+")
	
	# Display stats in green
	stdscr.attron(curses.color_pair(1))
	stdscr.addstr(title_y, title_x, title)
	stdscr.attroff(curses.color_pair(1))
	
	# Display detailed stats
	stats_y = title_y + 3
	center_text(stdscr, f"Tests completed: {len(wpm_history)}", stats_y - height//2)
	center_text(stdscr, f"Average WPM: {avg_wpm:.1f}", stats_y + 1 - height//2)
	center_text(stdscr, f"Maximum WPM: {max_wpm}", stats_y + 2 - height//2)
	
	# Show individual test results
	if wpm_history:
		center_text(stdscr, "Recent WPM scores:", stats_y + 4 - height//2)
		for i, wpm in enumerate(wpm_history[-5:]):  # Show last 5 scores
			center_text(stdscr, f"Test {len(wpm_history)-4+i}: {wpm} WPM", stats_y + 5 + i - height//2)
	
	center_text(stdscr, "Press ESC to exit or any other key to play again", stats_y + 11 - height//2)
	stdscr.refresh()

def main(stdscr):
	# Initialize color pairs
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
	
	# Hide the cursor
	curses.curs_set(0)
	
	# Keep track of WPM history
	wpm_history = []

	try:
		start_screen(stdscr)
		while True:
			final_wpm, accuracy = wpm_test(stdscr)
			if final_wpm:  # Only add to history if test was completed (not escaped)
				wpm_history.append(final_wpm)
			
			display_stats(stdscr, wpm_history)
			key = stdscr.getkey()
			
			if ord(key) == 27:  # ESC key
				center_text(stdscr, "Thanks for playing!", 3)
				stdscr.refresh()
				time.sleep(1)
				break
	except KeyboardInterrupt:
		pass
	finally:
		curses.endwin()

def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	total_keystrokes = 0
	correct_keystrokes = 0
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			accuracy = (correct_keystrokes / total_keystrokes * 100) if total_keystrokes > 0 else 0
			display_final_score(stdscr, wpm, accuracy)
			return wpm, accuracy

		try:
			key = stdscr.getkey()
		except curses.error:
			continue

		if ord(key) == 27:  # ESC key
			return None, None

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text) and len(key) == 1:
			total_keystrokes += 1
			if len(current_text) < len(target_text) and key == target_text[len(current_text)]:
				correct_keystrokes += 1
			current_text.append(key)

def display_final_score(stdscr, wpm, accuracy):
	stdscr.clear()
	draw_border(stdscr)
	
	title = "FINAL SCORE"
	height, width = stdscr.getmaxyx()
	title_y = height//4
	
	# Draw box around score
	center_text(stdscr, title, title_y - height//2)
	center_text(stdscr, f"Words Per Minute: {wpm}", title_y + 2 - height//2)
	center_text(stdscr, f"Accuracy: {accuracy:.1f}%", title_y + 4 - height//2)
	center_text(stdscr, "Press 'r' to replay or ESC to exit", title_y + 6 - height//2)
	
	stdscr.refresh()
	while True:
		key = stdscr.getkey()
		if key.lower() == 'r':
			return True
		elif ord(key) == 27:  # ESC
			return False

wrapper(main)