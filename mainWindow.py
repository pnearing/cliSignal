#!/usr/bin/env python3

import curses
from common import add_title_to_win
from window import Window


class MainWindow(Window):
    """
    Class to store and manipulate the main curses window. (stdscr)
    """
    def __init__(self, window: curses.window) -> None:
        """
        Initialize the MainWindow object.
        :param window: The curses window object.
        """
        Window.__init__(self, window, "cliSignal")
        return

    def redraw(self) -> None:
        """
        Redraw the window.
        :return: None
        """
        super().redraw()
        self._window.refresh()
        return
