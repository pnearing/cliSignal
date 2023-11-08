#!/usr/bin/env python3
"""
File: bar.py
Base functions of the menu / status bar.
"""
from typing import Optional
from enum import IntEnum
import curses
from themes import ThemeColours
from common import ROW, COL, STRINGS


class Bar(object):
    """
    Base class for the status and menu bars.
    """

    def __init__(self,
                 window: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 empty_attrs: int,
                 theme: dict[str, dict[str, int | bool | Optional[str]]],
                 bg_char: str,
                 ) -> None:
        """
        Initialize the status bar.
        :param window: curses.window: The window to draw on (Main window)
        :param width: int: The width of the status bar.
        :param top_left: tuple[int, int]: The top left corner of the status bar.
        :param empty_attrs: int: The attributes to use for empty spaces on the status bar.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        :param bg_char: str: The character to use for the background.
        """
        # Set internal vars:
        self._window: curses.window = window
        """The curses window object"""
        self._theme: dict[str, dict[str, int | bool | Optional[str]]] = theme
        """Store a copy of theme for the bar."""
        self._empty_attrs: int = empty_attrs
        """The attributes to use for empty spaces on the bar."""
        self._bg_char: str = bg_char
        """The character to use for drawing the background. Usually space."""

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
            self._window.addstr(self.top_left[ROW], col, self._bg_char, self._empty_attrs)
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
        self.top_left = top_left
        self.width = width
        return

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this bar?
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :return: bool: True if the mouse is over this bar, False if not.
        """
        if mouse_pos[ROW] == self.top_left[ROW]:
            if self.top_left[COL] <= mouse_pos[COL] <= (self.top_left[COL] + self.width):
                return True
        return False
