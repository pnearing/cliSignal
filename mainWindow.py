#!/usr/bin/env python3
"""
File: mainWindow.py
Class to store and manipulate the main window.
"""
import curses
from common import ROW, COL, calc_attributes
from themes import ThemeColours
from window import Window
from contactsWindow import ContactsWindow
from messagesWindow import MessagesWindow
from typingWindow import TypingWindow


class MainWindow(Window):
    """
    Class to store and manipulate the main curses window. (stdscr)
    """

    def __init__(self,
                 window: curses.window,
                 theme: dict[str, dict[str, int | bool]]
                 ) -> None:
        """
        Initialize the MainWindow object.
        :param window: curses.window: The curses window object.
        """
        # Define window attrs for the main window:
        window_attrs: int = calc_attributes(ThemeColours.MAIN_WIN, theme['mainWin'])
        border_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_BORDER, theme['mainWinBorder'])
        title_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_TITLE, theme['mainWinTitle'])
        # Run super.__init__:
        Window.__init__(self,
                        window,
                        "cliSignal",
                        (0, 0),
                        window_attrs,
                        border_attrs,
                        title_attrs,
                        theme,
                        True)
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
        self.recalculate_window_sizes()
        # Create window objects:
        self.contacts_window: ContactsWindow = ContactsWindow(self.contacts_size, self.contacts_top_left, theme)
        """The contacts window object."""
        self.messages_window: MessagesWindow = MessagesWindow(self.messages_size, self.messages_top_left, theme)
        """The messages window object."""
        self.typing_window: TypingWindow = TypingWindow(self.typing_size, self.typing_top_left, theme)
        """The typing area window object."""
        return

    def recalculate_window_sizes(self):
        self.contacts_size = (self.size[ROW], int(self.size[COL] * 0.33))
        self.contacts_top_left = (self.top_left[ROW], self.top_left[COL])
        self.messages_size = (int(self.size[ROW] * 0.75), self.size[COL] - self.contacts_size[COL])
        self.messages_top_left = (self.top_left[ROW], self.top_left[COL] + self.contacts_size[COL])
        self.typing_size = (self.size[ROW] - self.messages_size[ROW], self.size[COL] - self.contacts_size[COL])
        self.typing_top_left = (self.messages_top_left[ROW] + self.messages_size[ROW],
                                self.top_left[COL] + self.contacts_size[COL])
        return

    def redraw(self) -> None:
        super().redraw()
        self.contacts_window.redraw()
        self.messages_window.redraw()
        self.typing_window.redraw()
        return

    def resize(self) -> None:
        super().resize((-1, -1), (0, 0))
        self.recalculate_window_sizes()
        self.contacts_window.resize(self.contacts_size, self.contacts_top_left)
        self.messages_window.resize(self.messages_size, self.messages_top_left)
        self.typing_window.resize(self.typing_size, self.typing_top_left)
        return
