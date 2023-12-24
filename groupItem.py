#!/usr/bin/env python3
"""
File: groupItem.py
    Store and display a single group.
"""
import curses
from typing import Optional

import common
import terminal
from SignalCliApi import SignalReceivedMessage
from SignalCliApi.signalCommon import MessageFilter
from SignalCliApi.signalGroup import SignalGroup
from SignalCliApi.signalMessages import SignalMessages
from common import ROW, COL, TOP, LEFT
from cursesFunctions import calc_attributes, add_ch, add_str
from themes import ThemeColours
from typeError import __type_error__


class GroupItem(object):
    """
    Store and display a single group.
    :param pad: curses.window: The pad to draw on.
    :param pad_top_left: tuple[int, int]: The top left corner of this group on the pad: (ROW, COL).
    :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
    :param group: SignalCliApi.SignalGroup: The signal group.
    """
    def __init__(self,
                 pad_top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 group: SignalGroup,
                 ) -> None:
        """
        Initialize a group.
        :param pad_top_left: tuple[int, int]: The top left corner of this group on the pad: (ROW, COL).
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param group: SignalCliApi.SignalGroup: The signal group.
        """
        # Run super:
        super().__init__()

        # Set internal properties from parameters::
        self._pad: Optional[curses.window] = None
        """The window to draw on."""
        self._group: SignalGroup = group
        """The SignalCliApi SignalGroup object."""
        self._pad_top_left: tuple[int, int] = pad_top_left
        """The top left corner of the group item."""

        # Set internal properties:
        self._is_selected: bool = False
        """Is this group selected?"""
        self._is_expanded: bool = False
        """is this group expanded?"""
        self._bg_char: str = theme['backgroundChars']['contactsWin']
        """The background character."""
        self._selected_char: str = theme['groupSubWinChars']['selected']
        """Character to display when selected."""
        self._unselected_char: str = theme['groupSubWinChars']['unselected']
        """Character to display when unselected."""
        self._expanded_char: str = theme['groupSubWinChars']['expanded']
        """Character to display when expanded."""
        self._collapsed_char: str = theme['groupSubWinChars']['collapsed']
        """Character to display when collapsed."""
        self._expanded_line: str = theme['groupSubWinChars']['expandLine']
        """Character to display when expanded to indicate grouped items."""
        self._typing_char: str = theme['groupSubWinChars']['typing']
        """Character to display when someone is typing in the group."""
        self._not_typing_char: str = theme['groupSubWinChars']['notTyping']
        """Character to display when no one is typing in the group."""
        self._selected_attr: int = calc_attributes(ThemeColours.CONTACTS_WIN_SEL_GRP, theme['contWinSelGrp'])
        """Attributes to use when selected."""
        self._unselected_attr: int = calc_attributes(ThemeColours.CONTACTS_WIN_UNSEL_GRP, theme['contWinUnselGrp'])
        """Attributes to use when unselected."""
        self._width: int = 0
        """The width of the group item."""
        self._height: int = 1
        """The height of the group item."""

        self._display_lines: list[str] = []
        """The lines to display on the window."""
        self.__update_display_lines__()
        self.__set_width__()
        return

####################################
# Internal methods:
####################################
    def __set_width__(self) -> None:
        if self.is_expanded:
            self._width = 0
            for line in self._display_lines:
                self._width = max(self.width, len(line))
        else:
            self._width = len(self._display_lines[0])
        return

    def __set_height__(self) -> None:
        if self.is_expanded:
            self._height = len(self._display_lines)
        else:
            self._height = 1
        return

    def __get_num_unread_in_conversation__(self) -> int:
        if common.CURRENT_ACCOUNT is None:
            return 0
        messages: SignalMessages = common.CURRENT_ACCOUNT.messages
        # Get the unread messages for this group:
        message_filer: int = MessageFilter.NOT_READ
        conversation = messages.get_conversation(self._group, message_filer)
        count = 0
        for message in conversation:
            if isinstance(message, SignalReceivedMessage):
                count += 1
        return count

    def __gen_first_line__(self) -> str:
        first_line = self.selected_char + self.expanded_char
        num_unread = self.__get_num_unread_in_conversation__()
        first_line += common.get_unread_char(num_unread)
        if self._group.is_typing:
            first_line += self._typing_char
        else:
            first_line += self._not_typing_char
        first_line += self._group.get_display_name()
        return first_line

    def __gen_second_line__(self) -> str:
        second_line = self._bg_char + self._expanded_line
        second_line += common.STRINGS['groupItemLabels']['lastSeen'] + ':' + self._bg_char
        if self._group.last_seen is None:
            second_line += common.STRINGS['groupItemLabels']['unknown']
        else:
            second_line += self._group.last_seen.get_display_time()
        second_line += self._bg_char + common.STRINGS['groupItemLabels']['expires'] + ':' + self._bg_char
        second_line += str(self._group.expiration)
        return second_line

    def __get_third_line__(self) -> str:
        third_line = self._bg_char + self._expanded_line
        third_line += common.STRINGS['groupItemLabels']['numMembers'] + ':' + self._bg_char
        third_line += str(len(self._group.members))
        third_line += self._bg_char + common.STRINGS['groupItemLabels']['groupId'] + ':' + self._bg_char
        third_line += self._group.id
        return third_line

    def __get_fourth_line__(self) -> str:
        fourth_line = self._bg_char + self._expanded_line
        fourth_line += common.STRINGS['groupItemLabels']['description'] + ':' + self._bg_char
        if self._group.description is None:
            fourth_line += common.STRINGS['groupItemLabels']['notSet']
        else:
            fourth_line += self._group.description
        return fourth_line

    def __update_display_lines__(self) -> None:
        self._display_lines = [
            self.__gen_first_line__(), self.__gen_second_line__(), self.__get_third_line__(), self.__get_fourth_line__()
        ]
        return

######################################
# External Methods:
######################################
    def redraw(self) -> None:
        """
        Redraw the group item on the pad.
        :return:
        """
        _, num_cols = self._pad.getmaxyx()
        self.__update_display_lines__()
        # Fill in the back ground of the first line:
        for col in range(0, num_cols):
            add_ch(self._pad, self._bg_char, self.attrs, self.top, col)
        # Add the first line:
        add_str(self._pad, self._display_lines[0], self.attrs, self.top, self.left)
        if self.is_expanded:
            for i in range(1, len(self._display_lines)):
                # Fill in the background of the line:
                for col in range(1, num_cols):
                    add_ch(self._pad, self._bg_char, self.attrs, self.top + i, col)
                # Add the display line:
                add_str(self._pad, self._display_lines[i], self.attrs, self.top + i, self.left)
        return

######################################
# Properties:
######################################
    @property
    def group(self) -> SignalGroup:
        return self._group

    @property
    def is_selected(self) -> bool:
        """
        Is this group item selected?
        :return: Bool: True the item is selected, False it is not.
        """
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        """
        Is this group selected?
        Setter.
        :param value: bool: True the item is selected, False it is not.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._is_selected = value
        return

    @property
    def is_expanded(self) -> bool:
        """
        Is this group item expanded?
        :return: bool: True the item is expanded, False it is not.
        """
        return self._is_expanded

    @is_expanded.setter
    def is_expanded(self, value: bool) -> None:
        """
        Is this group item expanded?
        :param value: bool: True the item is expanded, False it is not.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value = self._is_expanded
        self._is_expanded = value
        if old_value != value:
            self._display_lines[0] = self.__gen_first_line__()
            self.__set_height__()
            self.__set_width__()
        return

    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, value):
        self._pad = value
        return

    @property
    def selected_char(self) -> str:
        """
        Return the selected / unselected character to use.
        :return: str: The char.
        """
        if self._is_selected:
            return self._selected_char
        return self._unselected_char

    @property
    def expanded_char(self) -> str:
        """
        Return the current expanded char based on _is_expanded.
        :return: str: The char.
        """
        if self._is_expanded:
            return self._expanded_char
        return self._collapsed_char

    @property
    def attrs(self) -> int:
        """
        Return the current attributes based on _is_selected.
        :return: int: The current attributes.
        """
        if self._is_selected:
            return self._selected_attr
        return self._unselected_attr

    @property
    def top_left(self) -> tuple[int, int]:
        """
        The top left corner of the group item.
        :return: tuple[int, int]: The top left corner: (ROW, COL).
        """
        return self._pad_top_left

    @property
    def size(self) -> tuple[int, int]:
        """
        The size of the group item.
        :return: tuple[int, int]: The size: (HEIGHT, WIDTH)
        """
        return self._height, self._width

    @property
    def bottom_right(self) -> tuple[int, int]:
        """
        The bottom right of the group item.
        :return: tuple[int, int]: The bottom right: (ROW, COL).
        """
        return self._pad_top_left[ROW] + self._height - 1, self._pad_top_left[COL] + self._width - 1

    @property
    def top(self) -> int:
        """
        The top most row of the group item.
        :return: int: The top row.
        """
        return self._pad_top_left[TOP]

    @top.setter
    def top(self, value: int) -> None:
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_top_left = (value, self._pad_top_left[LEFT])
        return

    @property
    def left(self) -> int:
        """
        The left most column of the group item.
        :return: int: The left column.
        """
        return self._pad_top_left[LEFT]

    @property
    def bottom(self) -> int:
        """
        The bottom most row of the group item.
        :return: int: The bottom row.
        """
        return self._pad_top_left[TOP] + self._height - 1

    @property
    def right(self) -> int:
        """
        The right most row of the group item.
        :return: int: The right row.
        """
        return self._pad_top_left[LEFT] + self._width - 1

    @property
    def height(self) -> int:
        """
        The height of the group item.
        :return: int: The height in rows.
        """
        return self._height

    @property
    def width(self) -> int:
        """
        The width of the group item.
        :return: int: The width in columns.
        """
        return self._width

    @property
    def max_width(self) -> int:
        """
        The maximum width of this group item.
        :return: int: The max width.
        """
        max_width: int = 0
        for line in self._display_lines:
            max_width = max(max_width, len(line))
        return max_width
