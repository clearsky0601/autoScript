#!/usr/bin/env python3
import os
import datetime
import curses
import re

LOG_FILE = os.path.expanduser("~/.useful_commands.log")
HISTORY_FILE = os.path.expanduser("~/.zsh_history")

def get_last_update_time():
    if os.path.exists(LOG_FILE):
        return datetime.datetime.fromtimestamp(os.path.getmtime(LOG_FILE))
    return None

def get_new_history(last_update):
    if not os.path.exists(HISTORY_FILE):
        print(f"Error: Zsh history file not found at {HISTORY_FILE}")
        return []

    with open(HISTORY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        history = f.readlines()

    commands = []
    for line in history:
        match = re.match(r': (\d+):\d+;(.+)$', line)
        if match:
            timestamp, command = match.groups()
            command_time = datetime.datetime.fromtimestamp(int(timestamp))
            if last_update is None or command_time > last_update:
                commands.append(command.strip())

    return list(dict.fromkeys(commands))[-1000:]

def select_commands(stdscr, commands):
    curses.curs_set(0)
    current_row = 0
    selected = [False] * len(commands)
    offset = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for i in range(offset, min(offset + h - 2, len(commands))):
            cmd = commands[i]
            x = 2
            y = i - offset + 1
            if i == current_row:
                stdscr.attron(curses.A_REVERSE)
            if selected[i]:
                stdscr.attron(curses.A_BOLD)
            stdscr.addstr(y, x, cmd[:w-3])
            stdscr.attroff(curses.A_REVERSE)
            stdscr.attroff(curses.A_BOLD)

        # 添加进度指示器
        progress = f"[{current_row + 1}/{len(commands)}]"
        stdscr.addstr(h-1, w - len(progress) - 1, progress)

        if offset + h - 2 < len(commands):
            stdscr.addstr(h-1, 0, "MORE")
        else:
            stdscr.addstr(h-1, 0, "END")

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            return None
        elif key == ord('j'):
            if current_row < len(commands) - 1:
                current_row += 1
                if current_row >= offset + h - 2:
                    offset += 1
        elif key == ord('k'):
            if current_row > 0:
                current_row -= 1
                if current_row < offset:
                    offset -= 1
        elif key == ord(' '):
            selected[current_row] = not selected[current_row]
        elif key == 10:  # Enter key
            confirm = stdscr.subwin(3, 30, h//2-1, w//2-15)
            confirm.box()
            confirm.addstr(1, 2, "Save? (y/n)")
            confirm.refresh()
            if confirm.getch() == ord('y'):
                return [cmd for cmd, sel in zip(commands, selected) if sel]

def main():
    last_update = get_last_update_time()
    if last_update:
        print(f"Last update: {last_update}")
    else:
        print("No previous records found.")

    new_history = get_new_history(last_update)
    if not new_history:
        print("No new commands since last update.")
        return

    selected_commands = curses.wrapper(select_commands, new_history)

    if selected_commands is None:
        print("Operation cancelled. No commands were recorded.")
    elif selected_commands:
        with open(LOG_FILE, "a") as f:
            for cmd in selected_commands:
                f.write(f"{datetime.datetime.now()} {cmd}\n")
        print(f"Selected commands have been saved to {LOG_FILE}")
    else:
        print("No commands were selected.")

if __name__ == "__main__":
    main()