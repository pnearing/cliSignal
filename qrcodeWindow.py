#!/usr/bin/env python3
"""
File: qrcodeWindow.py
Display a given qr-code.
"""
import logging
import time
from typing import Optional, Any
import curses
from common import ROW, HEIGHT, COL, WIDTH, STRINGS, Focus
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
        border_focus_chars: dict[str, str] = theme['qrcodeWinFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN_TITLE, theme['qrcodeWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.QRCODE_WIN_FOCUS_TITLE, theme['qrcodeWinFTitle'])
        title_chars: dict[str, str] = theme['qrcodeWinTitleChars']
        title_focus_chars: dict[str, str] = theme['qrcodeWinFTitleChars']

        # Setup qr_code:
        self.qrcode: list[str] = []

        width: int = 41
        height: int = 22
        top_left = calc_center_top_left(std_screen.getmaxyx(), (height, width))

        # Create the curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        super().__init__(std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                         border_chars, border_focus_chars, title_attrs, title_focus_attrs, title_chars,
                         title_focus_chars, bg_char, Focus.QR_CODE)

        # Set text attrs:
        self._text_attrs: int = calc_attributes(ThemeColours.QRCODE_TEXT, theme['qrcodeText'])

        # Store std_screen
        self._std_screen: curses.window = std_screen
        return

    def redraw(self) -> None:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.redraw.__name__)
        if not self.is_visible:
            return
        super().redraw()
        for i, line in enumerate(self.qrcode):
            for j, char in enumerate(self.qrcode[i]):
                if len(char) != 1:
                    logger.debug("Char = %s" % char)
                self._window.addch(1 + i, 1 + j, char, self._text_attrs)
        self._window.refresh()
        return

    def resize(self) -> None:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.resize.__name__)
        screen_size = self._std_screen.getmaxyx()
        top_left: tuple[int, int] = calc_center_top_left(self._std_screen.getmaxyx(), self.real_size)
        logger.debug("qr_window top_left=%s" % str(top_left))
        logger.debug("window size: %s" % str(self.real_size))
        logger.debug("screen size: %s" % str(screen_size))
        if screen_size[ROW] < self.real_size[ROW]:
            return
        if screen_size[COL] < self.real_size[COL]:
            return

        super().resize(self.real_size, top_left, True, True)
        return
# 22 row, 45 cols
# 9608 ord code. for full block.
