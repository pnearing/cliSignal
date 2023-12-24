#!/usr/bin/env python3
"""
File: messagesWindow.py
Messages list window handling.
"""
from typing import Optional
import curses

import common
from SignalCliApi import SignalReceivedMessage, SignalSentMessage
from SignalCliApi.signalCommon import RecipientTypes
from SignalCliApi.signalMessage import SignalMessage
from SignalCliApi.signalMessages import SignalMessages
from common import ROW, COL, TOP, LEFT, BOTTOM, RIGHT, STRINGS, Focus
from cursesFunctions import calc_attributes, add_title_to_win, add_ch, center_string, terminal_bell
from messageItem import MessageItem
from themes import ThemeColours
from typeError import __type_error__
from verticalScrollBar import VerticalScrollBar
from window import Window


class MessagesWindow(Window):
    """
    Class to store the messages' window.
    """
    def __init__(self,
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the messages window.
        :param size: tuple[int, int]: The size of the window: (ROWS, COLS).
        :param top_left: tuple[int, int]: The top left corner of the window: (ROW, COL).
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Set title theme, and background character:
        title: str = STRINGS['titles']['messages']
        self._theme: dict[str, dict[str, int | bool | str]] = theme
        """Store the theme for future use."""
        self._bg_char: str = theme['backgroundChars']['messagesWin']
        """Store the background character."""

        # Set theme attrs and strings:
        window_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN, theme['msgsWin'])
        border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_BORDER, theme['msgsWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_FOCUS_BORDER, theme['msgsWinFBorder'])
        border_chars: dict[str, str] = theme['msgsWinBorderChars']
        border_focus_chars: dict[str, str] = theme['msgsWinFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_TITLE, theme['msgsWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_FOCUS_TITLE, theme['msgsWinFTitle'])
        title_chars: dict[str, str] = theme['msgsWinTitleChars']
        title_focus_chars: dict[str, str] = theme['msgsWinFTitleChars']

        # Create the curses window:
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])

        # Run Super:
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, border_focus_chars, title_attrs, title_focus_attrs, title_chars,
                        title_focus_chars, self._bg_char, Focus.MESSAGES, 'left')

        # Set this window as always visible:
        self.always_visible = True
        self.is_static_size = False

        # Create the vertical scroll bar:
        self._v_scrollbar: VerticalScrollBar = VerticalScrollBar(
            height=self.height,
            top_left=(self.real_top_left[common.TOP] + 1, self.real_bottom_right[common.RIGHT] - 1),
            theme=theme
        )
        """The vertical scroll bar object."""
        self._v_scrollbar.is_visible = True

        # Create the conversation var:
        self._conversation: list[SignalSentMessage | SignalReceivedMessage] = []
        """The conversation we build the pad from."""
        self.__update_conversation__()

        # Create the message items for the messages in the conversation:
        self._message_item_list: list[MessageItem] = []
        """The message item list for the conversation."""
        self._selection: Optional[int] = None
        self.__update_message_items__()
        if len(self._message_item_list) > 0:
            self._message_item_list[-1].is_selected = True
            self._selection = len(self._message_item_list) - 1

        # Create the pad:
        self._pad: Optional[curses.window] = None
        """The pad we draw on."""
        self._pad_out_top_left: tuple[int, int] = (0, 0)
        """The top left of the pad to start the output from."""
        self.__create_pad__()

        return

    def __update_conversation__(self) -> None:
        if common.CURRENT_RECIPIENT is None:
            self._conversation = []
            return

        def _sort_(item: SignalMessage) -> int:
            return item.timestamp.timestamp

        messages: SignalMessages = common.CURRENT_ACCOUNT.messages
        self._conversation = messages.get_conversation(common.CURRENT_RECIPIENT)
        self._conversation.sort(key=_sort_, reverse=False)
        return

    def __update_message_items__(self) -> None:
        self.selection = None
        self._message_item_list = []
        for message in self._conversation:
            message_item = MessageItem(message=message,
                                       pad_width=self.pad_width,
                                       theme=self._theme
                                       )
            self._message_item_list.append(message_item)
        if len(self._message_item_list) > 0:
            self._message_item_list[-1].is_selected = True
            self.selection = len(self._message_item_list) - 1
        return

    def __clear_pad__(self) -> None:
        for row in range(0, self.pad_height):
            for col in range(0, self.pad_width):
                add_ch(self._pad, self._bg_char, self._bg_attrs, row, col)
        return

    def __create_pad__(self):
        self._pad = curses.newpad(self.pad_height, self.pad_width)
        self.__clear_pad__()
        item_top = 1  # One extra line for end of history.
        for message_item in self._message_item_list:
            message_item.pad = self._pad
            message_item.top = item_top
            item_top += message_item.height
        self.pad_out_bottom = self.pad_bottom
        return

    def __inc_selection__(self, step: int = 1) -> None:
        new_selection = self.selection + step
        if new_selection >= len(self._message_item_list):
            new_selection = len(self._message_item_list) - 1
            terminal_bell()
        self.selection = new_selection
        return

    def __dec_selection__(self, step: int = 1) -> None:
        new_selection = self.selection - step
        if new_selection < 0:
            new_selection = 0
            terminal_bell()
        self.selection = new_selection
        return

    #############################################
    # External methods:
    #############################################
    def recipient_changed(self) -> None:
        self.__update_conversation__()
        self.__update_message_items__()
        self.__create_pad__()
        return

    def message_received(self) -> None:
        return self.recipient_changed()

    def update(self) -> None:
        return self.recipient_changed()

    #############################################
    # External overrides:
    #############################################
    def resize(self,
               size: Optional[tuple[int, int]],
               real_top_left: Optional[tuple[int, int]],
               do_resize: bool = True,
               do_move: bool = True,
               ) -> None:
        super().resize(size, real_top_left, do_resize, do_move)
        self._v_scrollbar.resize(self.height, (self.real_top_left[TOP] + 1, self.real_bottom_right[RIGHT] - 1))
        self.__update_message_items__()
        self.__create_pad__()
        return

    def redraw(self) -> None:
        super().redraw()
        if common.CURRENT_RECIPIENT is None:
            recipient_text = 'None'
        else:
            if common.CURRENT_RECIPIENT.recipient_type == RecipientTypes.CONTACT:
                recipient_text = common.CURRENT_RECIPIENT.get_display_name(proper_self=False)
            else:
                recipient_text = common.CURRENT_RECIPIENT.get_display_name()
        recipient_text = "Thread: " + recipient_text
        add_title_to_win(self._window, recipient_text, self.border_attrs, self.title_attrs, self.title_chars['lead'],
                         self.title_chars['tail'], 'right')
        if self.pad_height > self.display_height:
            self._v_scrollbar.is_enabled = True
        else:
            self._v_scrollbar.is_enabled = False
        self._v_scrollbar.redraw()

        # Redraw the pad:
        self.__clear_pad__()
        if common.CURRENT_RECIPIENT is not None:
            center_string(self._pad, 0, STRINGS['msgsWin']['endOfHist'], self._bg_attrs)
        for message_item in self._message_item_list:
            message_item.redraw()

        if self.selected_message is not None:
            self.pad_out_bottom = self.selected_message.bottom

        self._window.noutrefresh()
        self._pad.noutrefresh(self.pad_out_top, self.pad_out_left,
                              self.display_top, self.display_left,
                              self.display_bottom, self.display_right)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        if self.is_focused:
            if char_code == curses.KEY_UP:
                self.__dec_selection__()
                return True
            elif char_code == curses.KEY_DOWN:
                self.__inc_selection__()
                return True
            elif char_code == curses.KEY_PPAGE:
                self.__dec_selection__(5)
                return True
            elif char_code == curses.KEY_NPAGE:
                self.__inc_selection__(5)
                return True
        return None

##################################
# Properties:
##################################
    ##################
    # Selections:
    @property
    def selection(self) -> int:
        return self._selection

    @selection.setter
    def selection(self, value: Optional[int]):
        if value is not None and not isinstance(value, int):
            __type_error__('value', 'Optional[int]', value)
        last_selection = self._selection
        self._selection = value
        if last_selection is not None:
            self._message_item_list[last_selection].is_selected = False
        if value is not None:
            self._message_item_list[value].is_selected = True
        return

    @property
    def selected_message(self) -> Optional[MessageItem]:
        if self._selection is not None:
            return self._message_item_list[self._selection]
        return None

    #############
    # Display output:
    @property
    def display_top_left(self):
        return self.real_top + 1, self.real_left + 1

    @property
    def display_top(self):
        return self.real_top + 1

    @property
    def display_left(self):
        return self.real_left + 1

    @property
    def display_width(self):
        return self.width - 1

    @property
    def display_height(self):
        return self.height

    @property
    def display_bottom_right(self):
        return self.display_top + self.display_height - 1, self.display_left + self.display_width - 1

    @property
    def display_bottom(self):
        return self.display_top + self.display_height - 1

    @property
    def display_right(self):
        return self.display_left + self.display_width - 1

    ##############
    # Pad properties:
    @property
    def pad_top_left(self):
        return 0, 0

    @property
    def pad_top(self):
        return 0

    @property
    def pad_left(self):
        return 0

    @property
    def pad_width(self):
        return self.display_width

    @property
    def pad_height(self):
        pad_height = 1  # One extra line for end of history.
        for message_item in self._message_item_list:
            pad_height += message_item.height
        if pad_height < self.display_height:
            pad_height = self.display_height
        return pad_height

    @property
    def pad_bottom_right(self):
        return self.pad_top + self.pad_height - 1, self.pad_left + self.pad_width - 1

    @property
    def pad_bottom(self):
        return self.pad_top + self.pad_height - 1

    @property
    def pad_right(self):
        return self.pad_left + self.pad_width - 1

    ##############
    # pad output size, top_left, etc:
    @property
    def pad_out_size(self):
        return self.display_height, self.display_width

    @property
    def pad_out_height(self):
        return self.display_height

    @property
    def pad_out_width(self):
        return self.display_width

    @property
    def pad_out_top_left(self):
        return self._pad_out_top_left

    @pad_out_top_left.setter
    def pad_out_top_left(self, value):
        if not common.__type_check_position_or_size__(value):
            __type_error__("value", 'tuple[int, int]', value)
        self._pad_out_top_left = value

    @property
    def pad_out_top(self):
        return self._pad_out_top_left[TOP]

    @pad_out_top.setter
    def pad_out_top(self, value):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_out_top_left = (value, self._pad_out_top_left[LEFT])
        return

    @property
    def pad_out_left(self):
        return self._pad_out_top_left[LEFT]

    @pad_out_left.setter
    def pad_out_left(self, value: int):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_out_top_left = (self.pad_out_top_left[TOP], value)
        return

    @property
    def pad_out_bottom_right(self) -> tuple[int, int]:
        return self.pad_out_top + self.pad_out_height - 1, self.pad_out_left + self.pad_out_width - 1

    @pad_out_bottom_right.setter
    def pad_out_bottom_right(self, value: tuple[int, int]) -> None:
        if not common.__type_check_position_or_size__(value):
            __type_error__('value', 'tuple[int, int]', value)
        top = value[BOTTOM] - self.pad_out_height + 1
        if top < 0:
            top = 0
        left = value[RIGHT] - self.pad_out_width + 1
        if left < 0:
            left = 0
        self._pad_out_top_left = (top, left)

    @property
    def pad_out_bottom(self):
        return self.pad_out_top + self.pad_out_height - 1

    @pad_out_bottom.setter
    def pad_out_bottom(self, value):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        top = value - self.pad_out_height + 1
        if top < 0:
            top = 0
        self._pad_out_top_left = (top, self._pad_out_top_left[LEFT])
        return

    @property
    def pad_out_right(self):
        return self.pad_out_left + self.pad_out_width - 1

    @pad_out_right.setter
    def pad_out_right(self, value):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        left = value - self.pad_out_width + 1
        if left < 0:
            left = 0
        self._pad_out_top_left = (self._pad_out_top_left[TOP], left)
        return

#############################################
# Property hooks:
#############################################
    def __is_focused_hook__(self, is_get: bool, value: bool) -> Optional[bool]:
        if not is_get and value:
            should_save: bool = False
            for message in self._conversation:
                self_contact = common.CURRENT_ACCOUNT.contacts.get_self()
                if message.sender != self_contact:
                    message.mark_read()
                    should_save = True
                elif message.sender == self_contact and message.recipient == self_contact:
                    message.mark_read()
                    should_save = True
            if should_save:
                common.CURRENT_ACCOUNT.messages.__save__()
        return None
