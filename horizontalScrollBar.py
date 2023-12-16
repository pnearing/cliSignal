#!/usr/bin/env python3
"""
File: horizontalScrollBar.py
    Store and handle a horizontal scoll bar.
"""
import curses
from scrollBar import ScrollBar, MIN_WIDTH


class HorizontalScrollBar(ScrollBar):
    """
    Horizontal scroll bar.
    """
    def __init__(self,
                 width: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the scroll bar.
        :param width: int: The width of the scroll bar.
        :param top_left: tuple[int, int]: The top left corner of the scroll bar.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        super().__init__((1, width), top_left, theme)
        return

    def resize(self, width: int, top_left: tuple[int, int]) -> None:
        """
        Resize the scroll bar.
        :param width: int: The new width of the scroll bar.
        :param top_left: tuple[int, int]: The new top left corner of the scroll bar.
        :return: None.
        """
        super().resize((1, width), top_left)
        return

    def redraw(self) -> None:
        """
        Redraw the scroll bar.
        :return: None
        """
        # Draw the background:
        super().redraw()
        # Don't draw if we not visible or too small:
        if not self.is_visible or self.width < MIN_WIDTH:
            return
        # Place the pg left button:
        self._window.addstr(0, 0, self._pg_left_button_char, self.button_attrs)
        # Place the left button:
        self._window.addstr(0, 1, self._left_button_char, self.button_attrs)
        # Place the right button:
        self._window.addstr(0, self.width - 2, self._right_button_char, self.button_attrs)
        # Place the page right button:
        try:
            self._window.addstr(0, self.width - 1, self._pg_right_button_char, self.button_attrs)
        except curses.error:
            pass
        # Place the handle:
        if self.position is not None:
            col = int((self.width - 5) * self.position) + 2
            self._window.addstr(0, col, self._horizontal_handle_char, self.handle_attrs)
        self._window.noutrefresh()
        return
