#!/usr/bin/env python3
"""
File: messageItem.py
    Store and display a single message.
"""
import curses
import logging
from typing import Optional

from SignalCliApi import SignalReceivedMessage, SignalSentMessage
from common import TOP, LEFT, __type_check_position_or_size__, out_debug
from cursesFunctions import draw_border_on_win, calc_attributes, add_str, add_title_to_win, add_ch
from themes import ThemeColours
from typeError import __type_error__


class MessageItem(object):
    """
    Store and display a single message.
    """
    def __init__(self,
                 message: SignalReceivedMessage | SignalSentMessage,
                 pad_width: int,
                 theme: dict[str, dict[str, str | bool | int]]
                 ) -> None:
        """
        Initialize a message item.
        :param message: SignalReceivedMessage | SignalSentMessage: The message to display.
        :param pad_width: int: The width of the pad.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        self._message: SignalReceivedMessage | SignalSentMessage = message
        """The message to display"""

        self._pad_width: int = pad_width
        """The width of the pad."""

        self._bg_char = theme['backgroundChars']['messagesWin']
        """The background character to use."""

        self._border_chars = theme['messageBorderChars']
        """The border characters for a message."""

        self._undelivered_char: str = theme['messages']['undelivered']
        """Character to show when message has not been delivered."""

        self._delivered_char: str = theme['messages']['delivered']
        """Character to show when message was delivered but not yet read."""

        self._read_char: str = theme['messages']['read']
        """Character to show when message was delivered and read."""

        self._expire_char: str = theme['messages']['expires']
        """Character to show when a message has an expiry time."""

        self._expired_char: str = theme['messages']['expired']
        """Character to show when a message is expired."""

        self._no_expire_char: str = theme['messages']['noExpire']
        """Character to show when a message has no expiry time."""

        self._expired_char: str = theme['messages']['expired']
        """Character to show when a message has expired."""

        self._head_lead_char: str = theme['messages']['headLead']
        """The header lead character."""

        self._head_tail_char: str = theme['messages']['headTail']
        """The header tail character."""

        self._foot_lead_char: str = theme['messages']['footLead']
        """The footer lead character."""

        self._foot_tail_char: str = theme['messages']['footTail']
        """The footer tail character."""

        self._seperator_char: str = theme['messages']['seperator']
        """The indicator seperator character."""

        self._sent_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_TEXT, theme['msgsWinSentText'])
        """Sent message attributes."""

        self._recv_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_TEXT, theme['msgsWinRecvText'])
        """Received message attributes."""

        self._indicator_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_INDICATOR, theme['msgsWinIndicator'])
        """The delivery indicator attributes."""

        self._sent_border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_BORDER,
                                                       theme['msgsWinSentBorder'])
        """The sent messages border attributes"""

        self._sent_sel_border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_BORDER,
                                                           theme['msgsWinSentSelBorder'])
        """The sent message selected border attributes."""

        self._recv_border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_BORDER,
                                                       theme['msgsWinRecvBorder'])
        """The received message border attributes."""

        self._recv_sel_border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_BORDER,
                                                           theme['msgsWinRecvSelBorder'])
        """The received message selected border attributes."""

        self._sent_dt_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_TIME, theme['msgsWinSentTime'])
        """The sent message date time attributes."""

        self._recv_dt_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_TIME, theme['msgsWinRecvTime'])
        """The received message date time attributes."""

        self._pad: Optional[curses.window] = None
        """The pad to draw on."""

        self._width = int(pad_width * 0.75)
        """The width of the message on the pad."""

        left: int
        if isinstance(message, SignalSentMessage):
            left = pad_width - self._width - 1
        else:
            left = 0

        self._top_left = (0, left)
        """The top left of the message on the pad."""

        self._display_lines: list[str] = []
        """The rows to display on the screen."""
        self.__update_display_lines__()

        self._is_selected: bool = False
        """True if this item is selected."""
        return

    def __update_display_lines__(self) -> None:
        # Determine display strings:
        display_string: str
        if self._message.mentions is not None and len(self._message.mentions) > 0:
            display_string = self._message.parse_mentions()
        elif self._message.sticker is not None:
            if self._message.sticker.emoji is not None:
                display_string = "Sticker: %s" % self._message.sticker.emoji
            else:
                display_string = "Sticker: Emoji not set."
        else:
            display_string = self._message.body

        if display_string is None:
            logger: logging.Logger = logging.getLogger(__name__ + '.' + self.__update_display_lines__.__name__)
            logger.debug("Display string is None....")
            logger.debug(str(self._message.__to_dict__()))
            self._display_lines = ['<ERROR>']
            return

        self._display_lines = ['', ]
        count: int = 0
        row: int = 0
        for i, char in enumerate(display_string):
            count += 1
            if char != '\n':
                if count <= self.width - 2:
                    self._display_lines[row] += char
                else:
                    row += 1
                    self._display_lines.append(char)
                    count = 0
            else:
                row += 1
                self._display_lines.append('')
                count = 0
        for i, line in enumerate(self._display_lines):
            self._display_lines[i] = line.lstrip()
        return

#############################
# External methods:
#############################
    def redraw(self) -> None:
        # Draw a border around the message:
        message_box_size = (self.height, self.effective_width)
        message_box_top_left = (self.top, self.effective_left)
        draw_border_on_win(window=self._pad, border_attrs=self.border_attrs,
                           ts=self._border_chars['ts'], bs=self._border_chars['bs'],
                           ls=self._border_chars['ls'], rs=self._border_chars['rs'],
                           tl=self._border_chars['tl'], tr=self._border_chars['tr'],
                           bl=self._border_chars['bl'], br=self._border_chars['br'],
                           size=message_box_size, top_left=message_box_top_left)

        # Add the header to the message border.
        date_string = self._message.timestamp.get_display_time()
        add_ch(self._pad, self._head_lead_char, self.border_attrs, self.top, self.effective_left + 1)
        add_str(self._pad, date_string, self.dt_attrs)
        add_ch(self._pad, self._seperator_char, self.border_attrs)
        add_ch(self._pad, self.status_char, self._indicator_attrs)
        add_ch(self._pad, self._seperator_char, self.border_attrs)
        add_ch(self._pad, self.expires_char, self._indicator_attrs)
        add_ch(self._pad, self._head_tail_char, self.border_attrs)

        # Add the footer to the message border:
        # TODO: Add reactions to the message.

        # Add the body of the message:
        for i, line in enumerate(self._display_lines):
            add_str(self._pad, line, self.text_attrs, self.top + i + 1, self.effective_left + 1)

        return

#############################
# Properties:
#############################
    ###############
    # Selected:
    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._is_selected = value
        return

    ###############
    # Is sent message:

    @property
    def is_sent_message(self) -> bool:
        return isinstance(self._message, SignalSentMessage)

    ###############
    # Message item size and position on the pad.
    @property
    def height(self):
        return len(self._display_lines) + 2

    @property
    def width(self):
        return self._width

    @property
    def size(self):
        return self.height, self.width

    @property
    def top_left(self):
        return self._top_left

    @top_left.setter
    def top_left(self, value: tuple[int, int]) -> None:
        if not __type_check_position_or_size__(value):
            __type_error__('value', 'tuple[int, int]', value)
        self._top_left = value
        return

    @property
    def top(self):
        return self._top_left[TOP]

    @top.setter
    def top(self, value: int):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        if value < 0:
            raise ValueError('top must be >= 0.')
        self._top_left = (value, self._top_left[LEFT])
        return

    @property
    def left(self):
        return self._top_left[LEFT]

    @property
    def bottom_right(self):
        return self._top_left[TOP] + self.height - 1, self._top_left[LEFT] + self.width - 1

    @property
    def bottom(self):
        return self._top_left[TOP] + self.height - 1

    @property
    def right(self):
        return self._top_left[LEFT] + self.width - 1

    @property
    def effective_width(self):
        width = 37  # Minimum width for displaying the title.
        for line in self._display_lines:
            width = max(width, len(line))
        return width

    @property
    def effective_left(self):
        if self.is_sent_message:
            left = (self.right + 1) - self.effective_width
            if left < self.left:
                left = self.left
            return left
        else:
            return self.left
    #################
    # pad properties:
    @property
    def pad(self) -> curses.window:
        return self._pad

    @pad.setter
    def pad(self, value) -> None:
        self._pad = value
        return

    ####################
    # attribute properties:
    @property
    def border_attrs(self):
        if self.is_selected:
            if isinstance(self._message, SignalSentMessage):
                return self._sent_sel_border_attrs
            else:
                return self._recv_sel_border_attrs
        else:
            if isinstance(self._message, SignalSentMessage):
                return self._sent_border_attrs
            else:
                return self._recv_border_attrs

    @property
    def text_attrs(self):
        if isinstance(self._message, SignalSentMessage):
            return self._sent_text_attrs
        else:
            return self._recv_text_attrs

    @property
    def dt_attrs(self):
        if isinstance(self._message, SignalSentMessage):
            return self._sent_dt_attrs
        else:
            return self._recv_dt_attrs

    #################
    # Character properties:
    @property
    def status_char(self):
        if isinstance(self._message, SignalSentMessage):
            if self._message.is_delivered and not self._message.is_read:
                return self._delivered_char
            elif self._message.is_delivered and self._message.is_read:
                return self._read_char
            return self._undelivered_char
        else:
            if self._message.is_read:
                return self._read_char
            return self._delivered_char

    @property
    def expires_char(self):
        if self._message.expiration is not None and not self._message.is_expired:
            return self._expire_char
        elif self._message.expiration is not None and self._message.is_expired:
            return self._expired_char
        return self._no_expire_char
