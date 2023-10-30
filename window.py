#!/usr/bin/env python3
"""
    File: window.py
    Basic curses window operations.
"""
import curses
from common import add_title_to_win


class Window(object):
    """
    Base window class.
    """
    def __init__(self, window: curses.window, title: str) -> None:
        """
        Initialize the window.
        :param window: curses.window: The curses window object.
        :param title: The title of the window.
        """
        object.__init__(self)
        self._window: curses.window = window
        self._title: str = title
        num_rows, num_cols = window.getmaxyx()
        self.min_row = 1
        self.min_col = 1
        self.max_row = num_rows - 2
        self.max_col = num_cols - 2
        return

    def redraw(self) -> None:
        """
        Redraw this window.
        :return: None
        """
        # Clear the window:
        self._window.clear()
        # Draw a blue and white border:
        self._window.attron(curses.color_pair(1) | curses.A_BOLD)
        self._window.border()
        self._window.attroff(curses.color_pair(1) | curses.A_BOLD)
        # Add the title:
        add_title_to_win(self._window, self._title, (curses.color_pair(1) | curses.A_BOLD))
        # Fill the rest of the screen with a blue background.
        for row in range(self.min_row, self.max_row + 1):
            for col in range(self.min_col, self.max_col + 1):
                self._window.addch(row, col, ' ', curses.color_pair(1))
        return

