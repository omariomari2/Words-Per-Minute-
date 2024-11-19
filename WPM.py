import curses
from curses import wrapper
import time
import random


def start_screen(omr_scr):
	omr_scr.clear()
	omr_scr.addstr("Welcome to the Speed Typing Test!")
	omr_scr.addstr("\nPress any key to begin!")
	omr_scr.refresh()
	omr_scr.getkey()

def display_text(omr_scr, target, current, wpm=0):
	omr_scr.addstr(target)
	omr_scr.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		omr_scr.addstr(0, i, char, color)

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(omr_scr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	omr_scr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		omr_scr.clear()
		display_text(omr_scr, target_text, current_text, wpm)
		omr_scr.refresh()

		if "".join(current_text) == target_text:
			omr_scr.nodelay(False)
			break

		try:
			key = omr_scr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(omr_scr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(omr_scr)
	while True:
		wpm_test(omr_scr)
		omr_scr.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = omr_scr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)