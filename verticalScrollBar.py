#!/usr/bin/env python3
"""
File: verticalScrollBar.py
    Handle a vertical scroll bar.
"""
import curses
from scrollBar import ScrollBar, MIN_HEIGHT


class VerticalScrollBar(ScrollBar):
    """
    Class to store and handle a curses scroll bar.
    """
    def __init__(self,
                 height: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize a Vertical scroll bar.
        :param height: int: The height of the scroll bar.
        :param top_left: tuple[int, int]: The top left corner of the scrollbar.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        super().__init__((height, 1), top_left, theme)
        return

    def resize(self, height: int, top_left: tuple[int, int]) -> None:
        """
        Resize the scroll bar.
        :param height: The new height of the scroll bar.
        :param top_left: The new top left corner of the scroll bar.
        :return: None.
        """
        super().resize((height, 1), top_left)
        return

    def redraw(self) -> None:
        """
        Redraw the vertical scroll bar.
        :return: None
        """
        # Draw the background:
        super().redraw()
        # Don't draw if we're not visible or too small:
        if not self._is_visible or self.height < MIN_HEIGHT:
            return
        # Place the pg up button:
        self._window.addstr(0, 0, self._pg_up_button_char, self.button_attrs)
        # Place the up button:
        self._window.addstr(1, 0, self._up_button_char, self.button_attrs)
        # Place the down button:
        self._window.addstr(self.height - 2, 0, self._down_button_char, self.button_attrs)
        # Place the pg down button:
        try:
            self._window.addstr(self.height - 1, 0, self._pg_down_button_char, self.button_attrs)
        except curses.error:
            pass
        # Place the handle:
        if self.position is not None:
            row = int((self.height - 5) * self.position) + 2
            self._window.addstr(row, 0, self._vertical_handle_char, self.handle_attrs)
        self._window.noutrefresh()
        return


