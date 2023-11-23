#!/usr/bin/env python3
"""
File: qrcodeWindow.py
Display a given qr-code.
"""
import time
from typing import Optional, Any
import curses
from common import ROW, HEIGHT, COL, WIDTH, STRINGS
from cursesFunctions import center_string, calc_center_top_left, calc_attributes
from themes import ThemeColours
from window import Window


class QRCodeWindow(Window):
    """
    Display a given QR Code.
    """
    def __init__(self,
                 std_screen: curses.window,
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the qr code window.
        :param std_screen: curses.window: The std_screen curses window object.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        title: str = STRINGS['titles']['qrcode']
        bg_char: str = theme['backgroundChars']['qrcodeWin']

        # Set theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN, theme['qrcodeWin'])
        border_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN_BORDER, theme['qrcodeWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN_FOCUS_BORDER, theme['qrcodeWinFBorder'])
        border_chars: dict[str, str] = theme['qrcodeWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN_TITLE, theme['qrcodeWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN_FOCUS_TITLE, theme['qrcodeWinFTitle'])
        title_chars: dict[str, str] = theme['qrcodeWinTitleChars']

        # Setup qr_code:
        self.qrcode: list[str] = []

        width: int = 41
        height: int = 22
        top_left = calc_center_top_left(std_screen.getmaxyx(), (height, width))

        # Create the curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        super().__init__(window, title, top_left, window_attrs, border_attrs, border_focus_attrs, border_chars,
                         title_attrs, title_focus_attrs, title_chars, bg_char)

        # Set as invisible by default:
        self.is_visible = False

        # Set text attrs:
        self._text_attrs: int = calc_attributes(ThemeColours.QRCODE_TEXT, theme['qrcodeText'])

        # Store std_screen
        self._std_screen: curses.window = std_screen
        return

    def redraw(self) -> None:
        if not self.is_visible:
            return
        super().redraw()
        for i, line in enumerate(self.qrcode):
            self._window.addstr(1 + i, 1, line, self._text_attrs)
        self._window.refresh()
        return

    def resize(self) -> None:
        top_left: tuple[int, int] = calc_center_top_left(self._std_screen.getmaxyx(), self.real_size)
        super().resize((-1, -1), top_left)
        return
# 22 row, 45 cols
# 9608 ord code. for full block.
