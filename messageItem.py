#!/usr/bin/env python3
"""
File: messageItem.py
    Store and display a single message.
"""
import curses
import logging
from typing import Optional

import common
from SignalCliApi import SignalReceivedMessage, SignalSentMessage, SignalReaction, SignalReactions
from SignalCliApi.signalCommon import RecipientTypes
from common import TOP, LEFT, __type_check_position_or_size__, out_debug, get_subscript_char, STRINGS
from cursesFunctions import draw_border_on_win, calc_attributes, add_str, add_title_to_win, add_ch
from themes import ThemeColours
from typeError import __type_error__


def __strip_control_characters__(line: str) -> str:
    return_line = ''
    for char in line:
        if ord(char) < 0x2400 or ord(char) > 0x2426:
            return_line += char
    return return_line


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

        self._pad: Optional[curses.window] = None
        """The pad to draw on."""

        self._top = 0
        """The top of the message on the pad."""

        self._is_selected: bool = False
        """True if this item is selected."""

        self._display_lines: list[str] = []
        """The rows to display on the screen."""
        self.__update_display_lines__()

        #########
        # Border chars:
        self._border_unsel_chars = theme['messageBorderUnselChars']
        """The border characters for an unselected message."""
        self._border_sel_chars: dict[str, str] = theme['messageBorderSelChars']
        """The border characters for a selected message."""

        ############
        # Delivery chars:
        self._undelivered_char: str = theme['messages']['undelivered']
        """Character to show when message has not been delivered."""
        self._delivered_char: str = theme['messages']['delivered']
        """Character to show when message was delivered but not yet read."""
        self._read_char: str = theme['messages']['read']
        """Character to show when message was delivered and read."""

        ##########
        # Expiry chars:
        self._expire_char: str = theme['messages']['expires']
        """Character to show when a message has an expiry time."""
        self._expired_char: str = theme['messages']['expired']
        """Character to show when a message is expired."""
        self._no_expire_char: str = theme['messages']['noExpire']
        """Character to show when a message has no expiry time."""
        self._expired_char: str = theme['messages']['expired']
        """Character to show when a message has expired."""

        #########
        # Header chars:
        self._head_lead_char: str = theme['messages']['headLead']
        """The header lead character."""
        self._head_tail_char: str = theme['messages']['headTail']
        """The header tail character."""

        #########
        # Footer chars:
        self._foot_lead_char: str = theme['messages']['footLead']
        """The footer lead character."""
        self._foot_tail_char: str = theme['messages']['footTail']
        """The footer tail character."""

        ###########
        # Indicator seperator char:
        self._seperator_char: str = theme['messages']['seperator']
        """The indicator seperator character."""

        ############
        # Horizontal seperator bar chars:
        self._bar_lead_char: str = theme['messages']['barLead']
        """The leading character for the seperator bar."""
        self._bar_mid_char: str = theme['messages']['barMid']
        """The middle character for the seperator bar."""
        self._bar_tail_char: str = theme['messages']['barTail']
        """The tailing character for the seperator bar."""

        #################
        # Horizontal bar title chars:
        self._bar_title_lead_char: str = theme['messages']['barTitleLead']
        """The leading title character."""

        self._bar_title_tail_char: str = theme['messages']['barTitleTail']
        """The tailing title character."""

        ##################
        # Message seperator bar chars:
        self._msg_bar_lead: str = theme['messages']['msgBarLead']
        """The leading character for the message bar."""
        self._msg_bar_mid: str = theme['messages']['msgBarMid']
        """The middle character for the message bar."""
        self._msg_bar_tail: str = theme['messages']['msgBarTail']
        """The tailing character for the message bar."""

        ##################
        # Message background attributes:
        self._sent_msg_bg: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_MSG_BG, theme['msgsWinSentMsgBG'])
        """Sent message unselected background attributes."""
        self._sent_sel_msg_bg: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_MSG_BG,
                                                     theme['msgsWinSentSelMsgBG'])
        """Sent message selected background attributes."""
        self._recv_msg_bg: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_MSG_BG, theme['msgsWinRecvMsgBG'])
        """Received message unselected background attributes."""
        self._recv_sel_msg_bg: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_MGS_BG,
                                                     theme['msgsWinRecvSelMsgBG'])
        """Received message selected background attributes."""

        ##################
        # Message text attributes:
        self._sent_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_TEXT, theme['msgsWinSentText'])
        """Sent message text attributes."""
        self._sent_sel_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_TEXT,
                                                         theme['msgsWinSentSelText'])
        """Sent message selected text attributes."""
        self._recv_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_TEXT, theme['msgsWinRecvText'])
        """Received message text attributes."""
        self._recv_sel_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_TEXT,
                                                         theme['msgsWinRecvSelText'])
        """Received message selected text attributes."""

        ################
        # Status indicator attributes:
        self._sent_indicator_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_INDICATOR,
                                                          theme['msgsWinSentIndicator'])
        """Sent message indicator attributes."""
        self._sent_sel_indicator_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_INDICATOR,
                                                              theme['msgsWinSentSelIndicator'])
        """Sent messages selected indicator attributes."""
        self._recv_indicator_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_INDICATOR,
                                                          theme['msgsWinRecvIndicator'])
        """Received message indicator attributes."""
        self._recv_sel_indicator_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_INDICATOR,
                                                              theme['msgsWinRecvSelIndicator'])
        """Received message selected indicator attributes."""

        ##################
        # Message border attributes:
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

        ###################
        # Date time attributes:
        self._sent_dt_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_TIME, theme['msgsWinSentTime'])
        """The sent message date time attributes."""
        self._sent_sel_dt_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_TIME,
                                                       theme['msgsWinSentSelTime'])
        """The sent message selected date time attributes."""

        self._recv_dt_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_TIME, theme['msgsWinRecvTime'])
        """The received message date time attributes."""
        self._recv_sel_dt_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_TIME,
                                                       theme['msgsWinRecvSelTime'])
        """The received message selected date time attributes."""

        #################
        # Sticker label attributes:
        self._sent_sticker_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_STICKER_LABEL,
                                                              theme['msgsWinSentStickerLabel'])
        """The sent sticker unselected label attributes."""
        self._sent_sel_sticker_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_STICKER_LABEL,
                                                                  theme['msgsWinSentSelStickerLabel'])
        """The sent sticker selected label attributes."""
        self._recv_sticker_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_STICKER_LABEL,
                                                              theme['msgsWinRecvStickerLabel'])
        """The received sticker unselected label attributes"""
        self._recv_sel_sticker_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_STICKER_LABEL,
                                                                  theme['msgsWinRecvSelStickerLabel'])
        """The received sticker selected label attributes."""

        ##############
        # Sticker value attributes:
        self._sent_sticker_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_STICKER_VALUE,
                                                              theme['msgsWinSentStickerValue'])
        """The sent sticker unselected value."""
        self._sent_sel_sticker_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_STICKER_VALUE,
                                                                  theme['msgsWinSentSelStickerValue'])
        """The sent sticker selected value attributes."""
        self._recv_sticker_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_STICKER_VALUE,
                                                              theme['msgsWinRecvStickerValue'])
        """The received sticker unselected value attributes."""
        self._recv_sel_sticker_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_STICKER_VALUE,
                                                                  theme['msgsWinRecvSelStickerValue'])

        ################
        # Attachment label attributes:
        self._sent_attach_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_ATTACH_LABEL,
                                                             theme['msgsWinSentAttachLabel'])
        """The sent attachment unselected label attributes."""
        self._sent_sel_attach_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_ATTACH_LABEL,
                                                                 theme['msgsWinSentSelAttachLabel'])
        """The sent attachment selected label attributes."""
        self._recv_attach_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_ATTACH_LABEL,
                                                             theme['msgsWinRecvAttachLabel'])
        """The received attachment unselected label attributes."""
        self._recv_sel_attach_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_ATTACH_LABEL,
                                                                 theme['msgsWinRecvSelAttachLabel'])

        ################
        # Attachment value attributes:
        self._sent_attach_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_ATTACH_VALUE,
                                                             theme['msgsWinSentAttachValue'])
        """The sent attachment unselected value attributes."""
        self._sent_sel_attach_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_ATTACH_VALUE,
                                                                 theme['msgsWinSentSelAttachValue'])
        """The sent attachment selected value attributes."""
        self._recv_attach_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_ATTACH_VALUE,
                                                             theme['msgsWinRecvAttachValue'])
        """The received attachment unselected value attributes."""
        self._recv_sel_attach_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_ATTACH_VALUE,
                                                                 theme['msgsWinRecvSelAttachValue'])

        ##############
        # Preview label attributes:
        self._sent_preview_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_PREVIEW_LABEL,
                                                              theme['msgsWinSentPreviewLabel'])
        """Sent URL preview unselected label attributes."""
        self._sent_sel_preview_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_PREVIEW_LABEL,
                                                                  theme['msgsWinSentSelPreviewLabel'])
        """The sent url preview selected label attributes."""
        self._recv_preview_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_PREVIEW_LABEL,
                                                              theme['msgsWinRecvPreviewLabel'])
        """The received url preview unselected label attributes."""
        self._recv_sel_preview_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_PREVIEW_LABEL,
                                                                  theme['msgsWinRecvSelPreviewLabel'])

        #############
        # Preview title attributes:
        self._sent_preview_title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_PREVIEW_TITLE,
                                                              theme['msgsWinSentPreviewTitle'])
        """The sent url preview unselected title attributes."""
        self._sent_sel_preview_title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_PREVIEW_TITLE,
                                                                  theme['msgsWinSentSelPreviewTitle'])
        """The sent url preview selected title attributes."""
        self._recv_preview_title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_PREVIEW_TITLE,
                                                              theme['msgsWinRecvPreviewTitle'])
        """The received url preview unselected title attributes."""
        self._recv_sel_preview_title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_PREVIEW_TITLE,
                                                                  theme['msgsWinRecvSelPreviewTitle'])
        """The received url preview selected title attributes."""

        ################
        # URL Preview description attributes:
        self._sent_preview_desc_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_PREVIEW_DESC,
                                                             theme['msgsWinSentPreviewDesc'])
        """The sent url preview unselected description attributes."""
        self._sent_sel_preview_desc_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_PREVIEW_DESC,
                                                                 theme['msgsWinSentSelPreviewDesc'])
        """The sent url preview selected description attributes."""
        self._recv_preview_desc_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_PREVIEW_DESC,
                                                             theme['msgsWinRecvPreviewDesc'])
        """The received url preview unselected description attributes."""
        self._recv_sel_preview_desc_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_PREVIEW_DESC,
                                                                 theme['msgsWinRecvSelPreviewDesc'])
        """The received url preview selected description attributes."""

        ################
        # Thumbnail label attributes:
        self._sent_thumb_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_THUMB_LABEL,
                                                            theme['msgsWinSentThumbLabel'])
        """Sent thumbnail unselected label attributes."""
        self._sent_sel_thumb_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_THUMB_LABEL,
                                                                theme['msgsWinSentSelThumbLabel'])
        """Sent thumbnail selected label attributes."""
        self._recv_thumb_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_THUMB_LABEL,
                                                            theme['msgsWinRecvThumbLabel'])
        """Received thumbnail unselected label attributes."""
        self._recv_sel_thumb_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_THUMB_LABEL,
                                                                theme['msgsWinRecvSelThumbLabel'])
        """Received thumbnail selected label attributes."""

        ################
        # Thumbnail value attributes:
        self._sent_thumb_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_THUMB_VALUE,
                                                            theme['msgsWinSentThumbValue'])
        """Sent thumbnail unselected value attributes."""
        self._sent_sel_thumb_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_THUMB_VALUE,
                                                                theme['msgsWinSentSelThumbValue'])
        """Sent thumbnail selected value attributes."""
        self._recv_thumb_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_THUMB_VALUE,
                                                            theme['msgsWinRecvThumbValue'])
        """Received thumbnail unselected value attributes."""
        self._recv_sel_thumb_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_THUMB_VALUE,
                                                                theme['msgsWinRecvSelThumbValue'])
        """Received thumbnail selected value attributes."""

        ##################
        # quote label attributes:
        self._sent_quote_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_LABEL,
                                                            theme['msgsWinSentQuoteLabel'])
        """Sent quoted message unselected label attributes."""
        self._sent_sel_quote_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_LABEL,
                                                                theme['msgsWinSentSelQuoteLabel'])
        """Sent quoted message selected label attributes."""
        self._recv_quote_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_LABEL,
                                                            theme['msgsWinRecvQuoteLabel'])
        """Received quoted message unselected label attributes."""
        self._recv_sel_quote_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_LABEL,
                                                                theme['msgsWinRecvSelQuoteLabel'])

        ####################
        # Quote thumbnail label attributes:
        self._sent_quote_thumb_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_THUMB_LABEL,
                                                                  theme['msgsWinSentQuoteThumbLabel'])
        """Sent quoted message, unselected thumbnail label attributes."""
        self._sent_sel_quote_thumb_label_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_THUMB_LABEL, theme['msgsWinSentSelQuoteThumbLabel'])
        """Sent quoted message, selected thumbnail label attributes."""
        self._recv_quote_thumb_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_THUMB_LABEL,
                                                                  theme['msgsWinRecvQuoteThumbLabel'])
        """Received quoted message, unselected thumbnail label attributes."""
        self._recv_sel_quote_thumb_label_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_THUMB_LABEL, theme['msgsWinRecvSelQuoteThumbLabel'])
        """Received quoted message, selected thumbnail label attributes."""

        ######################
        # Quote thumbnail value attributes:
        self._sent_quote_thumb_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_THUMB_VALUE,
                                                                  theme['msgsWinSentQuoteThumbValue'])
        """Sent quoted message, unselected thumbnail value attributes."""
        self._sent_sel_quote_thumb_value_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_THUMB_VALUE, theme['msgsWinSentSelQuoteThumbValue'])
        """Sent quoted message, selected thumbnail value attributes."""
        self._recv_quote_thumb_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_THUMB_VALUE,
                                                                  theme['msgsWinRecvQuoteThumbValue'])
        """Received quoted message, unselected thumbnail value attributes."""
        self._recv_sel_quote_thumb_value_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_THUMB_VALUE, theme['msgsWinRecvSelQuoteThumbValue'])
        ######################
        # quote attachment label attributes:
        self._sent_quote_attach_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_ATTACH_LABEL,
                                                                   theme['msgsWinSentQuoteAttachLabel'])
        """Sent quoted message unselected attachment label attributes."""
        self._sent_sel_quote_attach_label_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_ATTACH_LABEL, theme['msgsWinSentSelQuoteAttachLabel'])
        """Sent quoted message selected attachment label attributes."""
        self._recv_quote_attach_label_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_ATTACH_LABEL,
                                                                   theme['msgsWinRecvQuoteAttachLabel'])
        """Received quoted message, unselected attachment label attributes."""
        self._recv_sel_quote_attach_label_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_ATTACH_LABEL, theme['msgsWinRecvSelQuoteAttachLabel'])
        """Received quoted message, selected attachment label attributes."""

        #######################
        # quote attachment value attributes:
        self._sent_quote_attach_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_ATTACH_VALUE,
                                                                   theme['msgsWinSentQuoteAttachValue'])
        """Sent quoted message unselected attachment value attributes."""
        self._sent_sel_quote_attach_value_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_ATTACH_VALUE, theme['msgsWinSentSelQuoteAttachValue'])
        """Sent quoted message, selected attachment value attributes."""
        self._recv_quote_attach_value_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_ATTACH_VALUE,
                                                                   theme['msgsWinRecvQuoteAttachValue'])
        """Received quoted message, unselected attachment value attributes."""
        self._recv_sel_quote_attach_value_attrs: int = calc_attributes(
            ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_ATTACH_VALUE, theme['msgsWinRecvSelQuoteAttachValue'])
        """Received quoted message, selected attachment value attributes."""

        #####################
        # Quote body text attributes:
        self._sent_quote_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_TEXT,
                                                           theme['msgsWinSentQuoteText'])
        """Sent quoted message, unselected text attributes."""
        self._sent_sel_quote_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_TEXT,
                                                               theme['msgsWinSentSelQuoteText'])
        """Sent quoted message selected text attributes."""
        self._recv_quote_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_TEXT,
                                                           theme['msgsWinRecvQuoteText'])
        """Received quoted message unselected text attributes."""
        self._recv_sel_quote_text_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_TEXT,
                                                               theme['msgsWinRecvSelQuoteText'])
        """Received quoted message selected text attributes."""

        ################
        # Quote author line attributes:
        self._sent_quote_author_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_QUOTE_AUTHOR,
                                                             theme['msgsWinSentQuoteAuthor'])
        """Sent quoted message unselected author attributes."""
        self._sent_sel_quote_author_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_AUTHOR,
                                                                 theme['msgsWinSentSelQuoteAuthor'])
        """Sent quoted message, selected author attributes."""
        self._recv_quote_author_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_QUOTE_AUTHOR,
                                                             theme['msgsWinRecvQuoteAuthor'])
        """Received quoted message unselected author attributes."""
        self._recv_sel_quote_author_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_AUTHOR,
                                                                 theme['msgsWinRecvSelQuoteAuthor'])
        """Received quoted message selected author attributes."""

        return

    def __update_display_lines__(self) -> None:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.__update_display_lines__.__name__)

        # Determine display string:
        display_string: str = ''

        # Show quote:
        if self._message.quote is not None:
            quote = self._message.quote
            quote_string = '\u240D\n'
            quote_body = ('\u2416' + quote.author.get_display_name() + ' ' + STRINGS['msgsWin']['replyText'] +
                          ':\u2417\n')
            if quote.mentions is not None and len(quote.mentions) > 0:
                quote_body += quote.parse_mentions()
            else:
                quote_body += quote.text
            if len(quote.attachments) > 0:
                for attachment in quote.attachments:
                    if attachment.thumbnail is not None:
                        quote_string += '\u240E\n\u240F%s\u2410\n' % str(attachment.thumbnail.local_path)
                    else:
                        quote_string += '\u2411\n\u2412%s\u2413\n' % str(attachment.local_path)
            if quote_body is not None:
                if quote_string != '\u240D\n':
                    quote_string += '\u2425\n'
                quote_string += '\u2414' + quote_body + '\u2415\n'
            display_string = quote_string + display_string

        # Show attachments:
        if self._message.attachments is not None and len(self._message.attachments) > 0:
            attachment_string = ''
            for attachment in self._message.attachments:
                if attachment.thumbnail is not None:  # Attachment is a thumbnail:
                    attachment_string += '\u240A\n\u240B%s\u240C\n' % str(attachment.thumbnail.local_path)
                else:  # Regular attachment:
                    attachment_string += "\u2402\n\u2403%s\u2404\n" % str(attachment.local_path)
            display_string += attachment_string

        # Show preview:
        if len(self._message.previews) > 0:
            preview_string = ''
            for preview in self._message.previews:
                preview_string = '\u2405\n'
                preview_string += '\u2406' + preview.title + '\u2407\n'
                preview_string += '\u2408' + preview.description + '\u2409\n'
            if len(display_string) != 0:
                display_string += preview_string

        # If the message is a sticker:
        if self._message.body is None and self._message.sticker is not None:
            display_string += '\u2400\n'
            if self._message.sticker.emoji is not None:
                display_string += "\u2401%s" % self._message.sticker.emoji
            else:
                display_string += '\u2401Emoji Not Set.'
        elif self._message.body is not None:
            if len(display_string) > 0:
                display_string += '\u2426\n'
            if self._message.mentions is not None and len(self._message.mentions) > 0:
                display_string += self._message.parse_mentions()
            else:
                display_string += self._message.body

        if display_string is None:
            logger.debug("Display string is None....")
            logger.debug(str(self._message.__to_dict__()))
            self._display_lines = ['<ERROR>']
            return

        self._display_lines = ['', ]
        col: int = 0
        row: int = 0
        attach_value_started: bool = False
        preview_title_value_started: bool = False
        preview_desc_value_started: bool = False
        thumbnail_value_started: bool = False
        quote_attach_value_started: bool = False
        quote_thumbnail_value_started: bool = False
        quote_text_started: bool = False
        quote_author_started: bool = False
        for i, char in enumerate(display_string):
            # Select what value attributes to use by turning on and off bools.:
            if char == '\u2403':
                attach_value_started = True
            elif char == '\u2404':
                attach_value_started = False
            elif char == '\u2406':
                preview_title_value_started = True
            elif char == '\u2407':
                preview_title_value_started = False
            elif char == '\u2408':
                preview_desc_value_started = True
            elif char == '\u2409':
                preview_desc_value_started = False
            elif char == '\u240B':
                thumbnail_value_started = True
            elif char == '\u240C':
                thumbnail_value_started = False
            elif char == '\u240F':
                quote_thumbnail_value_started = True
            elif char == '\u2410':
                quote_thumbnail_value_started = False
            elif char == '\u2412':
                quote_attach_value_started = True
            elif char == '\u2413':
                quote_attach_value_started = False
            elif char == '\u2414':
                quote_text_started = True
            elif char == '\u2415':
                quote_text_started = False
            elif char == '\u2416':
                quote_author_started = True
            elif char == '\u2417':
                quote_author_started = False

            if char != '\n':
                if self.left + col + 1 < self.right - 1:
                    self._display_lines[row] += char
                    col += 1
                else:  # Wrap if needed:
                    space_idx: int = self._display_lines[row].rfind(' ')
                    if space_idx != -1:
                        word = self._display_lines[row][space_idx:]
                        word += char
                        self._display_lines[row] = self._display_lines[row][:space_idx]
                        if attach_value_started:
                            self._display_lines.append('\u2403' + word)  # Attachment value
                        elif preview_title_value_started:
                            self._display_lines.append('\u2406' + word)  # Preview title
                        elif preview_desc_value_started:
                            self._display_lines.append('\u2408' + word)  # Preview description
                        elif thumbnail_value_started:
                            self._display_lines.append('\u240B' + word)  # Thumbnail value
                        elif quote_thumbnail_value_started:
                            self._display_lines.append('\u240F' + word)  # Quoted thumbnail value
                        elif quote_attach_value_started:
                            self._display_lines.append('\u2412' + word)  # Quoted attachment value
                        elif quote_text_started:
                            self._display_lines.append('\u2414' + word)  # Quoted text
                        elif quote_author_started:
                            self._display_lines.append('\u2416' + word)  # Quote author
                        else:
                            self._display_lines.append(word)
                        row += 1
                        col = len(word + char)
                    else:
                        if attach_value_started:
                            self._display_lines.append('\u2403' + char)
                        elif preview_title_value_started:
                            self._display_lines.append('\u2406' + char)
                        elif preview_desc_value_started:
                            self._display_lines.append('\u2408' + char)
                        elif thumbnail_value_started:
                            self._display_lines.append('\u240B' + char)
                        elif quote_thumbnail_value_started:
                            self._display_lines.append('\u240F' + char)
                        elif quote_attach_value_started:
                            self._display_lines.append('\u2412' + char)
                        elif quote_text_started:
                            self._display_lines.append('\u2414' + char)
                        elif quote_author_started:
                            self._display_lines.append('\u2416' + char)
                        else:
                            self._display_lines.append(char)
                        row += 1
                        col = 0
            else:
                self._display_lines.append('')
                row += 1
                col = 0
        # Prepend the name of the sender if this is a group message:
        if self._message.recipient_type == RecipientTypes.GROUP:
            line: str = self._message.sender.get_display_name(proper_self=True) + ':'
            self._display_lines = [line, *self._display_lines]

        return

    def __build_reaction_list__(self) -> str:
        # If there are no reactions, return an empty string:
        if self._message.reactions is None or len(self._message.reactions) == 0:
            return ''
        # Mark all reactions as not processed:
        processed_reactions: dict[str, bool] = {}
        for reaction in self._message.reactions:
            processed_reactions[reaction.sender.get_id()] = False

        # Process reactions:
        emoji_list: str = ''
        for reaction in self._message.reactions:
            if processed_reactions[reaction.sender.get_id()] is False:
                emoji_list += reaction.emoji
                processed_reactions[reaction.sender.get_id()] = True
                reaction_by_emoji = self._message.reactions.get_by_emoji(reaction.emoji)
                if len(reaction_by_emoji) > 0:
                    subscript_num = len(reaction_by_emoji)
                    emoji_list += get_subscript_char(subscript_num)
                    for other_reaction in reaction_by_emoji:
                        processed_reactions[other_reaction.sender.get_id()] = True
        return emoji_list

    #############################
    # Drawing methods:
    #############################
    def __draw_message_bg__(self) -> None:
        for row in range(self.top, self.bottom):
            for col in range(self.effective_left, self.effective_left + self.effective_width):
                add_ch(self._pad, self._bg_char, self.bg_attrs, row, col)
        return

    def __draw_message_box__(self) -> None:
        # Draw a border around the message:
        message_box_size = (self.height, self.effective_width)
        message_box_top_left = (self.top, self.effective_left)
        draw_border_on_win(window=self._pad, border_attrs=self.border_attrs,
                           ts=self.border_chars['ts'], bs=self.border_chars['bs'],
                           ls=self.border_chars['ls'], rs=self.border_chars['rs'],
                           tl=self.border_chars['tl'], tr=self.border_chars['tr'],
                           bl=self.border_chars['bl'], br=self.border_chars['br'],
                           size=message_box_size, top_left=message_box_top_left)
        return

    def __draw_message_header__(self) -> None:
        date_string = self._message.timestamp.get_display_time()
        add_ch(self._pad, self._head_lead_char, self.border_attrs, self.top, self.effective_left + 1)
        add_str(self._pad, date_string, self.dt_attrs)
        add_ch(self._pad, self._seperator_char, self.border_attrs)
        add_ch(self._pad, self.status_char, self.indicator_attrs)
        add_ch(self._pad, self._seperator_char, self.border_attrs)
        add_ch(self._pad, self.expires_char, self.indicator_attrs)
        add_ch(self._pad, self._head_tail_char, self.border_attrs)
        return

    def __draw_message_footer__(self) -> None:
        if self._message.reactions is not None and len(self._message.reactions) > 0:
            reaction_list: str = self.__build_reaction_list__()
            add_ch(self._pad, self._foot_lead_char, self.border_attrs, self.bottom, self.effective_left + 1)
            add_str(self._pad, reaction_list, self.text_attrs)
            add_ch(self._pad, self._foot_tail_char, self.border_attrs)
        return

    def __draw_seperator__(self, row) -> None:
        add_ch(self._pad, self._bar_lead_char, self.border_attrs, row, self.effective_left)
        for col in range(self.effective_left + 1, self.effective_right):
            add_ch(self._pad, self._bar_mid_char, self.border_attrs, row, col)
        add_ch(self._pad, self._bar_tail_char, self.border_attrs, row, self.effective_right)
        return

    def __draw_title_on_seperator__(self, row: int, title: str, title_attrs: int) -> None:
        add_ch(self._pad, self._bar_title_lead_char, self.border_attrs, row, self.effective_left + 1)
        add_str(self._pad, title + ':', title_attrs)
        add_ch(self._pad, self._bar_title_tail_char, self.border_attrs)
        return

    def __draw_message_seperator__(self, row) -> None:
        add_ch(self._pad, self._msg_bar_lead, self.border_attrs, row, self.effective_left)
        for col in range(self.effective_left + 1, self.effective_right):
            add_ch(self._pad, self._msg_bar_mid, self.border_attrs, row, col)
        add_ch(self._pad, self._msg_bar_tail, self.border_attrs, row, self.effective_right)
        return

    #############################
    # External methods:
    #############################
    def redraw(self) -> None:
        if self._pad is None:
            return
        # Draw the message background:
        self.__draw_message_bg__()

        # Draw a border around the message:
        self.__draw_message_box__()

        # Add the header to the message border.
        self.__draw_message_header__()

        # Add the footer to the message border:
        self.__draw_message_footer__()

        # Parse the body of the message:

        for i, line in enumerate(self._display_lines):
            row: int = self.top + i + 1
            col = self.effective_left + 1
            if line == '':
                continue
            elif line[0] == '\u2400':  # Sticker label:
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['stickerLabel'], self.sticker_label_attrs)
            elif line[0] == '\u2401':  # Sticker value:
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.sticker_value_attrs, row, col)
            elif line[0] == '\u2402':  # Attachment label:
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['attachLabel'], self.attach_label_attrs)
            elif line[0] == '\u2403':  # Attachment value:
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.attach_value_attrs, row, col)
            elif line[0] == '\u2405':
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['previewLabel'], self.preview_label_attrs)
            elif line[0] == '\u2406':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.preview_title_attrs, row, col)
            elif line[0] == '\u2408':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.preview_desc_attrs, row, col)
            # attachment_string += '\u240A\n\u240B%s\u240C\n' % str(attachment.thumbnail.local_path)
            elif line[0] == '\u240A':
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['thumbLabel'], self.thumb_label_attrs)
            elif line[0] == '\u240B':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.thumb_value_attrs, row, col)
            elif line[0] == '\u240D':
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['quoteLabel'], self.quote_label_attrs)
            elif line[0] == '\u240E':
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['thumbLabel'], self.quote_thumb_label_attrs)
            elif line[0] == '\u240F':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.quote_thumb_value_attrs, row, col)
            elif line[0] == '\u2411':
                self.__draw_seperator__(row)
                self.__draw_title_on_seperator__(row, STRINGS['msgsWin']['attachLabel'], self.quote_attach_label_attrs)
            elif line[0] == '\u2412':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.quote_attach_value_attrs, row, col)
            elif line[0] == '\u2414':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.quote_text_attrs, row, col)
            elif line[0] == '\u2416':
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.quote_author_attrs, row, col)
            elif line[0] == '\u2425':
                self.__draw_seperator__(row)
            elif line[0] == '\u2426':
                self.__draw_message_seperator__(row)

            else:
                display_line = __strip_control_characters__(line)
                add_str(self._pad, display_line, self.text_attrs, row, col)

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
        self_contact = common.CURRENT_ACCOUNT.contacts.get_self()
        if self._message.recipient == self_contact and self._message.sender == self_contact:
            if self._message.device == common.CURRENT_ACCOUNT.device:
                return True
            else:
                return False
        return isinstance(self._message, SignalSentMessage)

    ###############
    # Message item size and position on the pad.
    @property
    def height(self):
        return len(self._display_lines) + 2

    @property
    def width(self):
        return round(self._pad_width * 0.75)

    @property
    def size(self):
        return self.height, self.width

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value: int):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        if value < 0:
            raise ValueError('top must be >= 0.')
        self._top = value
        return

    @property
    def left(self):
        if self.is_sent_message:
            return self._pad_width - self.width - 1
        else:
            return 0

    @property
    def top_left(self):
        return self.top, self.left

    @property
    def bottom_right(self):
        return self._top + self.height - 1, self.left + self.width - 1

    @property
    def bottom(self):
        return self._top + self.height - 1

    @property
    def right(self):
        return self.left + self.width - 1

    @property
    def effective_width(self) -> int:
        width = 33
        for line in self._display_lines:
            width_line = __strip_control_characters__(line)
            width = max(width, (len(width_line) + 2))
        if width > self.width:
            width = self.width
        return width

    @property
    def effective_left(self):
        if self.is_sent_message:
            left = self.right - (self.effective_width - 1)
            if left < self.left:
                left = self.left
            return left
        else:
            return self.left

    @property
    def effective_right(self):
        if self.is_sent_message:
            return self.right
        else:
            return self.left + (self.effective_width - 1)

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
    def bg_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_msg_bg
            else:
                return self._recv_sel_msg_bg
        else:
            if self.is_sent_message:
                return self._sent_msg_bg
            else:
                return self._recv_msg_bg

    @property
    def border_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_border_attrs
            else:
                return self._recv_sel_border_attrs
        else:
            if self.is_sent_message:
                return self._sent_border_attrs
            else:
                return self._recv_border_attrs

    @property
    def text_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_text_attrs
            else:
                return self._recv_sel_text_attrs
        else:
            if self.is_sent_message:
                return self._sent_text_attrs
            else:
                return self._recv_text_attrs

    @property
    def dt_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_dt_attrs
            else:
                return self._recv_sel_dt_attrs
        else:
            if self.is_sent_message:
                return self._sent_dt_attrs
            else:
                return self._recv_dt_attrs

    @property
    def indicator_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_indicator_attrs
            else:
                return self._recv_sel_indicator_attrs
        else:
            if self.is_sent_message:
                return self._sent_indicator_attrs
            else:
                return self._recv_indicator_attrs

    @property
    def sticker_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_sticker_label_attrs
            else:
                return self._recv_sel_sticker_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_sticker_label_attrs
            else:
                return self._recv_sticker_label_attrs

    @property
    def sticker_value_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_sticker_value_attrs
            else:
                return self._recv_sel_sticker_value_attrs
        else:
            if self.is_sent_message:
                return self._sent_sticker_value_attrs
            else:
                return self._recv_sticker_value_attrs

    @property
    def attach_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_attach_label_attrs
            else:
                return self._recv_sel_attach_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_attach_label_attrs
            else:
                return self._recv_attach_label_attrs

    @property
    def attach_value_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_attach_value_attrs
            else:
                return self._recv_sel_attach_value_attrs
        else:
            if self.is_sent_message:
                return self._sent_attach_value_attrs
            else:
                return self._recv_attach_value_attrs

    @property
    def preview_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_preview_label_attrs
            else:
                return self._recv_sel_preview_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_preview_label_attrs
            else:
                return self._recv_preview_label_attrs

    @property
    def preview_title_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_preview_title_attrs
            else:
                return self._recv_sel_preview_title_attrs
        else:
            if self.is_sent_message:
                return self._sent_preview_title_attrs
            else:
                return self._recv_preview_title_attrs

    @property
    def preview_desc_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_preview_desc_attrs
            else:
                return self._recv_sel_preview_desc_attrs
        else:
            if self.is_sent_message:
                return self._sent_preview_desc_attrs
            else:
                return self._recv_preview_desc_attrs

    @property
    def thumb_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_thumb_label_attrs
            else:
                return self._recv_sel_thumb_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_thumb_label_attrs
            else:
                return self._recv_thumb_label_attrs

    @property
    def thumb_value_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_thumb_value_attrs
            else:
                return self._recv_sel_thumb_value_attrs
        else:
            if self.is_sent_message:
                return self._sent_thumb_value_attrs
            else:
                return self._recv_thumb_value_attrs

    @property
    def quote_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_label_attrs
            else:
                return self._recv_sel_quote_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_label_attrs
            else:
                return self._recv_quote_label_attrs

    @property
    def quote_thumb_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_thumb_label_attrs
            else:
                return self._recv_sel_quote_thumb_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_thumb_label_attrs
            else:
                return self._recv_quote_thumb_label_attrs

    @property
    def quote_thumb_value_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_thumb_value_attrs
            else:
                return self._recv_sel_quote_thumb_value_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_thumb_value_attrs
            else:
                return self._recv_quote_thumb_value_attrs

    @property
    def quote_attach_label_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_attach_label_attrs
            else:
                return self._recv_sel_quote_attach_label_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_attach_label_attrs
            else:
                return self._recv_quote_attach_label_attrs

    @property
    def quote_attach_value_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_attach_value_attrs
            else:
                return self._recv_sel_quote_attach_value_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_attach_value_attrs
            else:
                return self._recv_quote_attach_value_attrs

    @property
    def quote_text_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_text_attrs
            else:
                return self._recv_sel_quote_text_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_text_attrs
            else:
                return self._recv_quote_text_attrs

    @property
    def quote_author_attrs(self):
        if self.is_selected:
            if self.is_sent_message:
                return self._sent_sel_quote_author_attrs
            else:
                return self._recv_sel_quote_author_attrs
        else:
            if self.is_sent_message:
                return self._sent_quote_author_attrs
            else:
                return self._recv_quote_author_attrs

    #################
    # Character properties:
    @property
    def border_chars(self) -> dict[str, str]:
        if self.is_selected:
            return self._border_sel_chars
        return self._border_unsel_chars

    @property
    def status_char(self):
        if self.is_sent_message:
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
