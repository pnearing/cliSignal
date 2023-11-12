#!/usr/bin/env python3
"""
File: quitWindow.py
Quit "are you sure?" message.
"""
from typing import Optional
import curses
from common import ROW, ROWS, COL, COLS, calc_attributes, STRINGS, center_string, add_accel_text, \
    KEYS_ENTER, KEY_ESC, KEY_BACKSPACE
from themes import ThemeColours
from window import Window


class QuitWindow(Window):
    """
    The quit "Are you sure?" message window.
    """
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the quit window.
        :param size: tuple[int, int]: The size of the window: (ROWS, COLS).
        :param top_left: tuple[int, int]: The top left corner of the window: (ROW, COL).
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Set title and background character.
        title: str = STRINGS['titles']['quit']
        bg_char: str = STRINGS['background']['quitWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.QUIT_WIN, theme['quitWin'])
        border_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_BORDER, theme['quitWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_FOCUS_BORDER, theme['quitWinFBorder'])
        border_chars: dict[str, str] = theme['quitWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_TITLE, theme['quitWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_FOCUS_TITLE, theme['quitWinFTitle'])
        title_chars: dict[str, str] = theme['quitWinTitleChars']

        # Window contents:
        self._window_contents: tuple[None, str, dict[str, str], None] = (
            None, STRINGS['messages']['quit'], STRINGS['other']['yesOrNo'], None
        )

        # Calculate window width:
        width: int = len(self._window_contents[1]) + 2
        # Calculate window height:
        height: int = len(self._window_contents) + 2
        # Make a curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, title_attrs, title_focus_attrs, title_chars, bg_char, False,
                        True)
        # Set this by default as invisible.
        self.is_visible = False
        # Set the text attributes:
        self._text_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_TEXT, theme['quitWinText'])
        """Quit window text attributes."""
        self._sel_text_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_SEL_TEXT, theme['quitWinSelText'])
        """Quit window selected text attributes."""
        self._sel_accel_text_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_SEL_ACCEL_TEXT,
                                                          theme['quitWinSelAccelText'])
        """Quit window accelerator text attributes."""
        self._unsel_text_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_UNSEL_TEXT, theme['quitWinUnselText'])
        """Quit window unselected text attributes."""
        self._unsel_accel_text_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_UNSEL_ACCEL_TEXT,
                                                            theme['quitWinUnselAccelText'])
        """Quit window unselected accelerator text attributes."""
        self._yes_selected: bool = True
        """If yes is selected."""
        return

    #####################################
    # Overrides:
    #####################################
    def redraw(self) -> None:
        """
        Redraw the window:
        :return: None
        """
        if not self.is_visible:
            return
        # Draw the border, title, and background:
        super().redraw()

        # Get yes / no characters:
        lead_chars: str = self._window_contents[2]['leadChars']
        yes_label: str = self._window_contents[2]['yes']
        mid_chars: str = self._window_contents[2]['midChars']
        no_label: str = self._window_contents[2]['no']
        tail_chars: str = self._window_contents[2]['tailChars']

        # Determine yes / no position:
        width = len(lead_chars) + (len('yes') - 2) + len(mid_chars) + (len('no') - 2) + len(tail_chars)
        col: int = int(self.size[COLS] // 2) - int(width // 2)
        row: int = 3

        # Add the message to the window:
        self._window.addstr(2, 1, self._window_contents[1], self._text_attrs)
        self._window.move(row, col)
        self._window.addstr(lead_chars, self._text_attrs)
        if self._yes_selected:
            add_accel_text(self._window, yes_label, self._sel_text_attrs, self._sel_accel_text_attrs)
        else:
            add_accel_text(self._window, yes_label, self._unsel_text_attrs, self._unsel_accel_text_attrs)
        self._window.addstr(mid_chars, self._text_attrs)
        if self._yes_selected:
            add_accel_text(self._window, no_label, self._unsel_text_attrs, self._unsel_accel_text_attrs)
        else:
            add_accel_text(self._window, no_label, self._sel_text_attrs, self._sel_accel_text_attrs)
        self._window.addstr(tail_chars, self._text_attrs)
        self._window.refresh()
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press given the character code.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True, the user wants to quit, False, the user doesn't want to quit, and None if not handled.
        """
        if char_code in KEYS_ENTER:
            return True
        elif char_code in (KEY_ESC, KEY_BACKSPACE):
            return False
        elif char_code in (curses.KEY_LEFT, curses.KEY_RIGHT):
            self._yes_selected = not self._yes_selected
        return None
