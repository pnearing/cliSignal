#!/usr/bin/env python3
"""
File: mainWindow.py
Class to store and manipulate the main window.
"""
from typing import Optional, Callable, Any
import curses
from common import ROW, COL, HEIGHT, WIDTH, STRINGS, MIN_SIZE, Focus
from cursesFunctions import calc_attributes, center_string
from themes import ThemeColours
from window import Window
from contactsWindow import ContactsWindow
from messagesWindow import MessagesWindow
from typingWindow import TypingWindow
from menuBar import MenuBar
from statusBar import StatusBar
from quitWindow import QuitWindow
from linkWindow import LinkWindow
from qrcodeWindow import QRCodeWindow
from versionWindow import VersionWindow


class MainWindow(Window):
    """
    Class to store and manipulate the main curses window. (stdscr)
    """

    def __init__(self,
                 std_screen: curses.window,
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]],
                 ) -> None:
        """
        Initialize the MainWindow object.
        :param std_screen: curses.window: The curses window object.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param callbacks: dict[str, dict[str, Optional[Callable]]: The callbacks to call for activations.
        """
        # Set title and background character:
        title: str = STRINGS['titles']['main']
        bg_char: str = theme['backgroundChars']['mainWin']

        # Define window attrs for the main window:
        window_attrs: int = calc_attributes(ThemeColours.MAIN_WIN, theme['mainWin'])
        border_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_BORDER, theme['mainWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_FOCUS_BORDER, theme['mainWinFBorder'])
        border_chars: dict[str, str] = theme['mainBorderChars']
        border_focus_chars: dict[str, str] = theme['mainFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_TITLE, theme['mainWinTitle'])
        title_focus_attr: int = calc_attributes(ThemeColours.MAIN_WIN_FOCUS_TITLE, theme['mainWinFTitle'])
        title_chars: dict[str, str] = theme['mainWinTitleChars']
        title_focus_chars: dict[str, str] = theme['mainWinFTitleChars']

        # Run super.__init__:
        Window.__init__(self,
                        std_screen=std_screen,
                        window=std_screen,
                        title=title,
                        top_left=(0, 0),
                        window_attrs=window_attrs,
                        border_attrs=border_attrs,
                        border_focus_attrs=border_focus_attrs,
                        border_chars=border_chars,
                        border_focus_chars=border_focus_chars,
                        title_attrs=title_attrs,
                        title_focus_attrs=title_focus_attr,
                        title_chars=title_chars,
                        title_focus_chars=title_focus_chars,
                        bg_char=bg_char,
                        focus_id=Focus.MAIN
                        )

        self.always_visible = True
        # Store the std_screen:
        self._std_screen: curses.window = std_screen
        """The standard curses screen."""

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
        self.__recalculate_window_sizes__()

        # Create primary window objects:
        self.contacts_window: ContactsWindow = ContactsWindow(std_screen, self.contacts_size, self.contacts_top_left,
                                                              theme)
        """The contacts Window object."""
        self.messages_window: MessagesWindow = MessagesWindow(std_screen, self.messages_size, self.messages_top_left,
                                                              theme)
        """The messages Window object."""
        self.typing_window: TypingWindow = TypingWindow(std_screen, self.typing_size, self.typing_top_left, theme)
        """The typing area Window object."""
        self.primary_windows: tuple[Window, ...] = (self.contacts_window, self.messages_window, self.typing_window)
        """A list of the primary windows."""

        # Create the menu and status bars:
        self.menu_bar: MenuBar = MenuBar(self._window, self.menu_top_left, theme, callbacks)
        """The menu bar Bar object."""
        self.status_bar: StatusBar = StatusBar(self._window, self.status_top_left, theme)
        """The status bar Bar object."""
        self.bars: tuple[MenuBar, StatusBar] = (self.menu_bar, self.status_bar)
        """The menu and status bars."""

        # Create sub-windows:
        self.quit_window: QuitWindow = QuitWindow(std_screen, theme)
        """The quit window object."""
        self.link_window: LinkWindow = LinkWindow(std_screen, theme)
        """The link window object."""
        self.qr_window: QRCodeWindow = QRCodeWindow(std_screen, theme)
        """The QR-Code window."""
        self.ver_window: VersionWindow = VersionWindow(std_screen, theme)
        """The version window."""
        self.sub_windows: tuple[Window, ...] = (self.quit_window, self.link_window, self.qr_window, self.ver_window)
        """The sub windows."""

        # The size error message:
        self._error_message: str = STRINGS['messages']['sizeError'].format(rows=MIN_SIZE[HEIGHT], cols=MIN_SIZE[WIDTH])
        self._error_attrs: int = calc_attributes(ThemeColours.MAIN_WIN_ERROR_TEXT, theme['mainWinErrorText'])
        return

###############################################
# Internal Methods:
###############################################
    def __recalculate_window_sizes__(self):
        """
        Recalculate the window sizes.
        :return: None
        """
        # Contacts Window
        self.contacts_size = (self.size[HEIGHT] - 2,
                              int(self.size[WIDTH] * 0.33))
        self.contacts_top_left = (self.top_left[ROW] + 1,
                                  self.top_left[COL])
        # Messages window:
        self.messages_size = (int(self.size[HEIGHT] * 0.75) - 1,
                              self.size[WIDTH] - self.contacts_size[WIDTH])
        self.messages_top_left = (self.top_left[ROW] + 1,
                                  self.top_left[COL] + self.contacts_size[WIDTH])
        # Typing window:
        self.typing_size = (self.size[HEIGHT] - self.messages_size[HEIGHT] - 2,
                            self.size[WIDTH] - self.contacts_size[WIDTH])
        self.typing_top_left = (self.messages_top_left[ROW] + self.messages_size[HEIGHT],
                                self.top_left[COL] + self.contacts_size[WIDTH])
        # menu bar:
        self.menu_top_left = (self.top_left[ROW],
                              self.top_left[COL])
        # Status bar:
        self.status_top_left = (self.bottom_right[ROW],
                                self.top_left[COL])
        return

    def __draw_size_error__(self) -> None:
        self._std_screen.clear()
        row: int = int(self.size[HEIGHT] / 2)
        try:
            center_string(self._std_screen, row, self._error_message, self._error_attrs)
        except curses.error:
            pass
        curses.doupdate()
        return

#######################################
# External method overrides:
#######################################
    def resize(self) -> None:
        size: tuple[int, int] = self._std_screen.getmaxyx()
        top_left: tuple[int, int] = (0, 0)
        super().resize(size, top_left, False, False)
        if self.real_size[HEIGHT] < MIN_SIZE[HEIGHT] or self.real_size[WIDTH] < MIN_SIZE[WIDTH]:
            return

        self.__recalculate_window_sizes__()
        self.contacts_window.resize(self.contacts_size, self.contacts_top_left)
        self.messages_window.resize(self.messages_size, self.messages_top_left)
        self.typing_window.resize(self.typing_size, self.typing_top_left)
        self.menu_bar.resize(self.menu_top_left)
        self.status_bar.resize(self.status_top_left)
        self.quit_window.resize()
        self.link_window.resize()
        self.qr_window.resize()
        self.ver_window.resize()
        return

    def should_resize(self) -> bool:
        num_rows, num_cols = self._std_screen.getmaxyx()
        if num_rows != self.real_size[HEIGHT]:
            return True
        if num_cols != self.real_size[WIDTH]:
            return True
        return False

    def redraw(self) -> None:
        if self.should_resize():
            self.resize()
        # If the terminal is too small, draw an error message:
        if self.real_size[HEIGHT] < MIN_SIZE[HEIGHT] or self.real_size[WIDTH] < MIN_SIZE[WIDTH]:
            self.__draw_size_error__()
            return

        # Draw main border and title:
        super().redraw()

        # Draw the main windows:
        self.contacts_window.redraw()
        self.messages_window.redraw()
        self.typing_window.redraw()
        # Draw the menu and status bars:
        self.menu_bar.redraw()
        self.status_bar.redraw()
        # Draw the sub-windows last, only one should be visible at a time.
        self.link_window.redraw()
        self.qr_window.redraw()
        self.ver_window.redraw()
        self.quit_window.redraw()
        curses.doupdate()
        return

############################################
# External methods:
############################################
    def get_visible_sub_window(self) -> Optional[Window]:
        """
        Get the sub-window that is visible.
        :return: Window: The visible sub-window, or None if none visible.
        """
        for window in self.sub_windows:
            if window.is_visible:
                return window
        return None

    def hide_sub_windows(self) -> None:
        """
        Make all the sub-windows invisible.
        :return: None
        """
        for window in self.sub_windows:
            window.is_visible = False
        return

############################################
# Properties:
############################################
    @property
    def is_sub_window_visible(self) -> bool:
        """
        Is a sub window visible?
        :return:
        """
        for window in self.sub_windows:
            if window.is_visible:
                return True
        return False
