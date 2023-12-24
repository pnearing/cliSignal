#!/usr/bin/env python3
"""
File: typingWindow.py
Message typing area window.
"""
import logging
from typing import Optional
import curses
from curses.textpad import Textbox

import common
from SignalCliApi.signalMessages import SignalMessages
from common import ROW, COL, STRINGS, Focus, HEIGHT, WIDTH, TOP, LEFT
from cursesFunctions import calc_attributes, add_ch
from themes import ThemeColours
from window import Window


class TypingWindow(Window):
    """
    Message typing window. You know, where you type your message. I didn't know what else to call it.
    """
    def __init__(self,
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | Optional[str]]]
                 ) -> None:
        """
        Initialize the typing window.
        :param size: tuple[int, int]: The size of the window.
        :param top_left: tuple[int, int]: The top left corner of the window.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        """
        # Set title and background char:
        title: str = STRINGS['titles']['typing']
        bg_char: str = theme['backgroundChars']['typingWin']

        # Set window attributes:
        window_attrs: int = calc_attributes(ThemeColours.TYPING_WIN, theme['typeWin'])
        border_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_BORDER, theme['typeWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_FOCUS_BORDER, theme['typeWinFBorder'])
        border_chars: dict[str, str] = theme['typeWinBorderChars']
        border_focus_chars: dict[str, str] = theme['typeWinFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_TITLE, theme['typeWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_FOCUS_TITLE, theme['typeWinFTitle'])
        title_chars: dict[str, str] = theme['typeWinTitleChars']
        title_focus_chars: dict[str, str] = theme['typeWinFTitleChars']

        # Create the curses window:
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, border_focus_chars, title_attrs, title_focus_attrs, title_chars,
                        title_focus_chars, bg_char, Focus.TYPING)
        # Set this window as always visible, and static size:
        self.always_visible = True
        self.is_static_size = False

        self._text_box_top_left = (self.real_top + 1, self.real_left + 1)
        self._text_box_size = (self.height, self.width - 11)
        self._text_box_window = curses.newwin(self._text_box_size[HEIGHT], self._text_box_size[WIDTH],
                                              self._text_box_top_left[TOP], self._text_box_top_left[LEFT])
        self._text_box = Textbox(self._text_box_window)
        return

################################
# External method overrides:
################################
    def resize(self,
               size: Optional[tuple[int, int]],
               real_top_left: Optional[tuple[int, int]],
               do_resize: bool = True,
               do_move: bool = True,
               ) -> None:
        super().resize(size, real_top_left, do_resize, do_move)
        self._text_box_top_left = (self.real_top + 1, self.real_left + 1)
        self._text_box_size = (self.height, self.width - 11)
        self._text_box_window = curses.newwin(self._text_box_size[HEIGHT], self._text_box_size[WIDTH],
                                              self._text_box_top_left[TOP], self._text_box_top_left[LEFT])
        self._text_box = Textbox(self._text_box_window)
        return

    def redraw(self) -> None:
        super().redraw()
        add_ch(self._window, '\u2566', self.border_attrs, 0, self.right - 10)
        for row in range(1, self.bottom + 1):
            add_ch(self._window, '\u2551', self.border_attrs, row, self.right - 10)
        add_ch(self._window, '\u2569', self.border_attrs, self.bottom + 1, self.right - 10)
        self._window.noutrefresh()
        self._text_box_window.noutrefresh()
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.process_key.__name__)
        if self.is_focused:
            if common.CURRENT_RECIPIENT is not None and char_code in common.KEYS_ENTER:
                self._text_box_window.clear()
                self._text_box.edit()
                message = self._text_box.gather().strip()
                if message == '':
                    return False
                messages: SignalMessages = common.CURRENT_ACCOUNT.messages
                response = messages.send_message(
                    recipients=common.CURRENT_RECIPIENT,
                    body=message
                )
                logger.debug("Sent message: %s" % message)
                # TODO: Check response.
                return True
        return
