#!/usr/bin/env python3
"""
File: bar.py
Base functions of the menu / status bar.
"""
from typing import Optional
import curses
from themes import ThemeColours
from common import ROW, COL


class Bar(object):
    """
    Base class for the status and menu bars.
    """
    def __init__(self,
                 window: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 empty_attrs: int,
                 theme: dict[str, dict[str, int | bool | Optional[str]]]
                 ) -> None:
        """
        Initialize the status bar.
        :param window: curses.window: The window to draw on (Main window)
        :param width: int: The width of the status bar.
        :param top_left: tuple[int, int]: The top left corner of the status bar.
        :param empty_attrs: int: The attributes to use for empty spaces on the status bar.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        """
        # Set internal vars:
        self._window: curses.window = window
        """The curses window object"""
        self._theme: dict[str, dict[str, int | bool | Optional[str]]] = theme
        """Store a copy of theme for the bar."""
        self._empty_attrs: int = empty_attrs
        """The attributes to use for empty spaces on the bar."""

        # Set external properties:
        self.top_left: tuple[int, int] = top_left
        """Top Left corner of the window."""
        self.width: int = width
        """The size of the window."""
        self.is_visible: bool = True
        """If this bar is visible."""
        return

    def redraw(self) -> None:
        """
        Redraw the status bar.
        :return: None
        """
        # Draw a background:
        for col in range(self.top_left[COL], (self.top_left[COL] + self.width)):
            self._window.addstr(self.top_left[ROW], col, 'X', self._empty_attrs)
        # try:
        #     self._window.addstr(self.top_left[ROW], self.width, ' ', self._empty_attrs)
        # except curses.error:
        #     pass  # Always get an error at the end of the window.
        return

    def resize(self,
               width: int,
               top_left: tuple[int, int],
               ) -> None:
        """
        Resize the status bar.
        :param width: The new width.
        :param top_left: The new top_left corner.
        :return: None
        """
        self._window.resize(1, width)
        self._window.mvwin(top_left[ROW], top_left[COL])
        self.top_left = top_left
        self.width = width
        return
