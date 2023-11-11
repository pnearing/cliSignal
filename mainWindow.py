#!/usr/bin/env python3
"""
File: mainWindow.py
Class to store and manipulate the main window.
"""
from typing import Optional, Callable, Any
import curses
from common import ROW, COL, calc_attributes, STRINGS
from themes import ThemeColours
from window import Window
from contactsWindow import ContactsWindow
from messagesWindow import MessagesWindow
from typingWindow import TypingWindow
from menuBar import MenuBar
from statusBar import StatusBar


class MainWindow(Window):
    """
    Class to store and manipulate the main curses window. (stdscr)
    """

    def __init__(self,
                 window: curses.window,
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]],
                 ) -> None:
        """
        Initialize the MainWindow object.
        :param window: curses.window: The curses window object.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param callbacks: dict[str, dict[str, Optional[Callable]]: The callbacks to call for activations.
        """
        # Set title and background character:
        title: str = STRINGS['titles']['main']
        bg_char: str = STRINGS['background']['mainWin']

        # Define window attrs for the main window:
        window_attrs: int = calc_attributes(ThemeColours.MAIN_WIN, theme['mainWin'])
        border_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_BORDER, theme['mainWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_FOCUS_BORDER, theme['mainWinFBorder'])
        border_chars: dict[str, str] = theme['mainBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_TITLE, theme['mainWinTitle'])
        title_focus_attr: int = calc_attributes(ThemeColours.MAIN_WIN_FOCUS_TITLE, theme['mainWinFTitle'])
        title_chars: dict[str, str] = theme['mainWinTitleChars']

        # Run super.__init__:
        Window.__init__(self,
                        window=window,
                        title=title,
                        top_left=(0, 0),
                        window_attrs=window_attrs,
                        border_attrs=border_attrs,
                        border_focus_attrs=border_focus_attrs,
                        border_chars=border_chars,
                        title_attrs=title_attrs,
                        title_focus_attrs=title_focus_attr,
                        title_chars=title_chars,
                        bg_char=bg_char,
                        is_main_window=True
                        )

        # Set the sub window vars:
        self.contacts_size: tuple[int, int] = (-1, -1)
        """The size of the contacts window."""
        self.contacts_top_left: tuple[int, int] = (-1, -1)
        """The top left corner of the contacts window."""
        self.messages_size: tuple[int, int] = (-1, -1)
        """The size of the messages window."""
        self.messages_top_left: tuple[int, int] = (-1, -1)
        """The top left corner of the messages window."""
        self.typing_size: tuple[int, int] = (-1, -1)
        """The size of the typing window."""
        self.typing_top_left: tuple[int, int] = (-1, -1)
        """The top left of the typing window."""
        self.menu_width: int = -1
        """The width of the menu bar."""
        self.menu_top_left: tuple[int, int] = (-1, -1)
        """The top left corner of the menu bar."""
        self.status_width: int = -1
        """The width of the status bar."""
        self.status_top_left: tuple[int, int] = (-1, -1)
        """The top let of the status bar."""
        self.recalculate_window_sizes()
        # Create window objects:
        self.contacts_window: ContactsWindow = ContactsWindow(self.contacts_size, self.contacts_top_left, theme)
        """The contacts Window object."""
        self.messages_window: MessagesWindow = MessagesWindow(self.messages_size, self.messages_top_left, theme)
        """The messages Window object."""
        self.typing_window: TypingWindow = TypingWindow(self.typing_size, self.typing_top_left, theme)
        """The typing area Window object."""
        self.menu_bar: MenuBar = MenuBar(self._window, self.menu_width, self.menu_top_left, theme, callbacks)
        """The menu bar Bar object."""
        self.status_bar: StatusBar = StatusBar(self._window, self.status_width, self.status_top_left, theme)
        """The status bar Bar object."""
        return

    def recalculate_window_sizes(self):
        self.contacts_size = (self.size[ROW] - 2, int(self.size[COL] * 0.33))
        self.contacts_top_left = (self.top_left[ROW] + 1, self.top_left[COL])
        self.messages_size = (int(self.size[ROW] * 0.75) - 1, self.size[COL] - self.contacts_size[COL])
        self.messages_top_left = (self.top_left[ROW] + 1, self.top_left[COL] + self.contacts_size[COL])
        self.typing_size = (self.size[ROW] - self.messages_size[ROW] - 2, self.size[COL] - self.contacts_size[COL])
        self.typing_top_left = (self.messages_top_left[ROW] + self.messages_size[ROW],
                                self.top_left[COL] + self.contacts_size[COL])
        self.menu_width = self.size[COL]
        self.menu_top_left = (self.top_left[ROW], self.top_left[COL])
        self.status_width = self.size[COL]
        self.status_top_left = (self.size[ROW], self.top_left[COL])
        return

    def redraw(self) -> None:
        super().redraw()
        self.contacts_window.redraw()
        self.messages_window.redraw()
        self.typing_window.redraw()
        self.menu_bar.redraw()
        self.status_bar.redraw()
        curses.doupdate()
        return

    def resize(self) -> None:
        super().resize((-1, -1), (0, 0))
        self.recalculate_window_sizes()
        self.contacts_window.resize(self.contacts_size, self.contacts_top_left)
        self.messages_window.resize(self.messages_size, self.messages_top_left)
        self.typing_window.resize(self.typing_size, self.typing_top_left)
        self.menu_bar.resize(self.menu_width, self.menu_top_left)
        self.status_bar.resize(self.status_width, self.status_top_left)
        return
