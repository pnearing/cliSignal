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
        return

    def redraw(self) -> None:
        """
        Redraw this window.
        :return: None
        """
        self._window.clear()
        self._window.attron(curses.color_pair(1) | curses.A_BOLD)
        self._window.border()
        self._window.attroff(curses.color_pair(1) | curses.A_BOLD)
        add_title_to_win(self._window, self._title, (curses.color_pair(1) | curses.A_BOLD))
        return

