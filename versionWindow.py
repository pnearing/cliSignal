#!/usr/bin/env python3
"""
File: versionWindow.py
    Store and display the versions.
"""
import curses
from typing import Optional

from window import Window
from common import ROW, COL, WIDTH, HEIGHT, STRINGS, KEYS_ENTER, Focus
from common import APP_VERSION as CLISIGNAL_VERSION
from SignalCliApi.signalCommon import VERSION as SIGNAL_API_VERSION
from themes import ThemeColours
from cursesFunctions import calc_attributes, calc_center_top_left, center_string


class VersionWindow(Window):
    """
    Store and display the current versions.
    """
    def __init__(self,
                 std_screen: curses.window,
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize the version window.
        :param std_screen: curses.window: The std_screen window object.
        :param theme: dist[str, dict[str, int | bool | str]]: The current theme.
        """
        # Get title and background character:
        title: str = STRINGS['titles']['version']
        bg_char: str = theme['backgroundChars']['versionWin']

        # Set the window attrs from the theme:
        window_attrs: int = calc_attributes(ThemeColours.VERSION_WIN, theme['verWin'])
        border_attrs: int = calc_attributes(ThemeColours.VERSION_WIN_BORDER, theme['verWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.VERSION_WIN_FOCUS_BORDER, theme['verWinFBorder'])
        border_chars: dict[str, str] = theme['verWinBorderChars']
        border_focus_chars: dict[str, str] = theme['verWinFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.VERSION_WIN_TITLE, theme['verWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.VERSION_WIN_FOCUS_TITLE, theme['verWinFTitle'])
        title_chars: dict[str, str] = theme['verWinTitleChars']
        title_focus_chars: dict[str, str] = theme['verWinFTitleChars']

        self._app_version_string: str = "cliSignal: V%s" % CLISIGNAL_VERSION
        self._api_version_string: str = "SignalCliApi: V%s" % SIGNAL_API_VERSION
        self._continue_string: str = "Press enter to continue."
        # Calculate size, add 4 extra spaces for border and spaces in width:
        width: int = max(len(self._app_version_string), len(self._app_version_string), len(self._continue_string)) + 4
        height: int = 7
        top_left: tuple[int, int] = calc_center_top_left(std_screen.getmaxyx(), (height, width))

        # Make a curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        super().__init__(std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                         border_chars, border_focus_chars, title_attrs, title_focus_attrs, title_chars,
                         title_focus_chars, bg_char, Focus.VERSION)

        # Set text attrs:
        self._text_attrs: int = calc_attributes(ThemeColours.VERSION_TEXT, theme['verWinText'])
        return

    def resize(self) -> None:
        """
        Resize the version window.
        :return: None
        """
        top_left: tuple[int, int] = calc_center_top_left(self._std_screen.getmaxyx(), self.real_size)
        super().resize((-1, -1), top_left, False, True)
        return

    def redraw(self) -> None:
        """
        Redraw the version window.
        :return: None
        """
        # If not visible return:
        if not self.is_visible:
            return
        # Draw the border and title:
        super().redraw()

        # Draw the window text:
        center_string(self._window, 2, self._app_version_string, self._text_attrs)
        center_string(self._window, 3, self._api_version_string, self._text_attrs)
        center_string(self._window, 4, self._continue_string, self._text_attrs)
        self._window.noutrefresh()
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code of the pressed key.
        :return: Optional[bool]: Return None: Char was not handled, and processing should continue.
            Return True: Char was handled, and processing should not continue.
            Return False: Close the window.
        """
        if char_code in KEYS_ENTER:
            return False
        return None
