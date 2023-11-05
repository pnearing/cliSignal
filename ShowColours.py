#!/usr/bin/env python3

import curses


def main(std_sreen: curses.window):
    for i in range(0, curses.COLORS):
        string = f'{i:03d}'
        curses.init_pair(i+1, curses.COLOR_WHITE, i)
        std_sreen.addstr(string, curses.color_pair(i + 1))
    std_sreen.refresh()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    return


if __name__ == '__main__':
    curses.wrapper(main)
    exit()