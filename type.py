import curses
from curses import wrapper  # terminal manipulation
import time
import random

"""
Start screen function manipulates the terminal with "stdscr" functions. clear() clears the terminal, addstr() adds text to the terminal
refresh() continual refreshes the terminal and getkey() waits for the user to type something in the terminal. 
"""


def start_screen(stdscr):
    stdscr.clear()  # clears terminal
    stdscr.addstr(
        "Welcome to the speed typing test"
    )  # Row, Column (1,0) Adds text to terminal
    stdscr.addstr("\nPress any key to begin")  # Row, Column (1,0)
    stdscr.refresh()
    stdscr.getkey()


"""
prints the wpm variable to the terminal and if the char typed matches the text from the .txt
the color will change green/red depending on right or wrong text. 
"""


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


"""
Reads the .txt file and splits every individual line and returns them randomly
"""


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


"""
calls the .txt files and sets the time to manipulate the wpm time with exceptions
"""


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elasped = max(time.time() - start_time, 1)
        wpm = round(
            (len(current_text) / (time_elasped / 60)) / 5
        )  # rounds wpm so that 0 isnt a value if its too small

        stdscr.clear()  # clears screen
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:  # Done with all the text
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # esc key
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):  # handles delete key
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


"""
main function to call static variables and keep the while loop manipulation the terminal 
"""


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
