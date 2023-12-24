#!/usr/bin/env python3
"""
File: main.py
"""
from typing import Optional, Callable, Any
import argparse
import os.path
import curses
import logging

import prettyPrint
from SignalCliApi import SignalSyncMessage, SignalContacts, SignalTypingMessage
from configFile import ConfigFile, ConfigFileError
from contactsSubWindow import ContactsSubWindow
from cursesFunctions import get_mouse, terminal_bell
from groupsSubWIndow import GroupsSubWindow
from messagesWindow import MessagesWindow
from prettyPrint import print_coloured
from terminal import Colours

from SignalCliApi.signalReceivedMessage import SignalReceivedMessage
from SignalCliApi.signalReaction import SignalReaction
from SignalCliApi.signalCommon import LinkAccountCallbackStates, SyncTypes, RecipientTypes
from SignalCliApi.signalAccount import SignalAccount
from SignalCliApi.signalCli import SignalCli
from SignalCliApi.signalExceptions import SignalError, SignalAlreadyRunningError
from SignalCliApi.signalReceipt import SignalReceipt
import common
from common import Focus, out_error, out_info, out_debug, out_warning
import arguments
from cliExceptions import Quit
from themes import load_theme, init_colours
from mainWindow import MainWindow
from linkWindow import LinkWindow, LinkMessages
from window import Window
from qrcodeWindow import QRCodeWindow
import runCallback
import typeError
from typeError import __type_error__

runCallback.set_suppress_error(True)  # Supress errors calling callbacks.
typeError.set_use_syslog(False)  # Dont' log to syslog.
typeError.set_use_logging(True)  # Use Logging.


#########################################
# My menu callbacks:
#########################################
def file_menu_settings_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    File menu settings callback.
    :return: None
    """
    return


def file_menu_quit_cb(status: str, std_screen: curses.window) -> None:
    """
    File menu quit callback.
    :return: None
    """

    if not common.SETTINGS['quitConfirm']:
        raise Quit()
    common.MAIN_WINDOW.hide_sub_windows()
    common.MAIN_WINDOW.quit_window.is_visible = True
    set_current_focus(Focus.QUIT)
    return


def accounts_menu_switch_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Accounts menu, switch callback.
    :return: None
    """
    return


def accounts_menu_link_cb(status: str,
                          std_screen: curses.window,
                          signal_cli: SignalCli
                          ) -> None:
    """
    Accounts menu, link callback.
    :param status: str: The call back status.
    :param std_screen: curses.window: The std screen
    :param signal_cli: SignalCli: The signal cli object.
    :return: None
    """
    # Set vars:
    # global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW, _DEVICE_NAME, _LAST_FOCUS, _SIGNAL_LINK_THREAD
    link_window: LinkWindow = common.MAIN_WINDOW.link_window
    qr_window: QRCodeWindow = common.MAIN_WINDOW.qr_window

    # Set the generating message, and hide the button:
    link_window.current_message = LinkMessages.GENERATE
    link_window.show_button = False

    # Set the window as visible, and set the focus:
    link_window.is_visible = True
    set_current_focus(Focus.LINK)
    # Redraw:
    common.MAIN_WINDOW.redraw()
    # Start the link thread.
    signal_cli.start_link_thread(
        callback=(signal_link_cb, [signal_cli]),
        gen_text_qr=True,
        png_qr_file_path=None,
        device_name=common.DEVICE_NAME,
        wait_time=0.1
    )
    # _SIGNAL_LINK_THREAD = signal_cli.generate_link_thread(callback, True, None, _DEVICE_NAME)
    # _SIGNAL_LINK_THREAD.start()
    return


def accounts_menu_register_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Accounts menu, register callback.
    :return: None
    """
    return


def help_menu_shortcuts_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    The help menu, Keyboard shortcuts callback.
    :return: None
    """
    return


def help_menu_about_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    The help menu, about callback.
    :return: None
    """
    return


def help_menu_version_cb(status: str, std_screen: curses.window, *args: tuple[Any, ...]) -> None:
    """
    The help menu, version callback.
    :return: None
    """
    # global _MAIN_WINDOW
    set_current_focus(Focus.VERSION)
    common.MAIN_WINDOW.ver_window.is_visible = True
    return


#########################################
# Button callbacks:
#########################################


#########################################
# Signal callbacks:
#########################################
def signal_start_up_cb(state: str) -> None:
    """
    Signal start up callback.
    :param state: str, the current state of the startup process.
    :return: None
    """
    # global _VERBOSE
    if common.VERBOSE:
        print_coloured("SIGNAL:", fg_colour=Colours.FG.blue, bold=True, end='')
        print(state)
    return


def signal_link_cb(state: str,
                   data: Optional[tuple[Optional[str], Optional[str]] | str | SignalAccount],
                   signal_cli: SignalCli
                   ) -> bool:
    """
    Link account signal callback.
    :param state: str: The current state.
    :param data: Optional[tuple[Optional[str], Optional[str]] | str | SignalAccount]
    :param signal_cli: SignalCli: The signal_cli object.
    :return: bool: If return True, cancel the link process.
    """
    # global _SIGNAL_LINK_THREAD, _MAIN_WINDOW
    logger: logging.Logger = logging.getLogger(__name__ + '.' + signal_link_cb.__name__)
    if state == LinkAccountCallbackStates.LINK_WAITING.value:
        return False
    logger.debug("Called with state: %s" % state)
    link_window: LinkWindow = common.MAIN_WINDOW.link_window
    qr_window: QRCodeWindow = common.MAIN_WINDOW.qr_window
    if state == LinkAccountCallbackStates.GENERATE_QR_STOP.value:
        link_window.is_visible = False
        qr_window.qrcode = data[0].splitlines(keepends=False)
        qr_window.is_visible = True
        set_current_focus(Focus.QR_CODE)
        common.MAIN_WINDOW.redraw()
        return False
    elif state == LinkAccountCallbackStates.LINK_SUCCESS.value:
        link_window.current_message = LinkMessages.SUCCESS
    elif state == LinkAccountCallbackStates.LINK_EXISTS_ERROR.value:
        link_window.current_message = LinkMessages.EXISTS
    elif state == LinkAccountCallbackStates.LINK_UNKNOWN_ERROR.value:
        link_window.current_message = LinkMessages.UNKNOWN
    elif state == LinkAccountCallbackStates.LINK_TIMEOUT_ERROR.value:
        link_window.current_message = LinkMessages.TIMEOUT
    else:
        return False
    qr_window.is_visible = False
    link_window.show_button = True
    link_window.is_visible = True
    set_current_focus(Focus.LINK)
    common.MAIN_WINDOW.redraw()
    signal_cli.stop_link_thread()
    return False


def signal_received_message_cb(account: SignalAccount, message: SignalReceivedMessage):
    out_debug("Receive message callback...")
    messages_window: MessagesWindow = common.MAIN_WINDOW.messages_window
    contacts_sub_window: ContactsSubWindow = common.MAIN_WINDOW.contacts_window.contacts_win
    groups_sub_window: GroupsSubWindow = common.MAIN_WINDOW.contacts_window.groups_win
    main_window: MainWindow = common.MAIN_WINDOW
    if common.TIME_STARTED < message.timestamp.datetime_obj:
        out_debug("Ringing bell.")
        terminal_bell()
    if common.CURRENT_RECIPIENT is not None:
        if message.sender == common.CURRENT_RECIPIENT or message.recipient == common.CURRENT_RECIPIENT:
            messages_window.message_received()
            if common.CURRENT_FOCUS == Focus.MESSAGES:
                message.mark_read()
    if message.recipient.recipient_type == RecipientTypes.GROUP:
        groups_sub_window.update()
    elif message.recipient.recipient_type == RecipientTypes.CONTACT:
        contacts_sub_window.update()
    return


def signal_receipt_message_cb(account: SignalAccount, receipt: SignalReceipt):
    out_debug("Receipt message callback...")
    messages_window: MessagesWindow = common.MAIN_WINDOW.messages_window
    if receipt.sender == common.CURRENT_RECIPIENT:
        messages_window.update()
    return


def signal_sync_message_cb(account: SignalAccount, sync_message: SignalSyncMessage):
    out_debug("Sync message callback...")
    if sync_message.sync_type == SyncTypes.SENT_MESSAGES:
        common.MAIN_WINDOW.messages_window.message_received()
    elif sync_message.sync_type == SyncTypes.READ_MESSAGES:
        common.MAIN_WINDOW.messages_window.message_received()
    return


def signal_typing_message_cb(account, typing_message: SignalTypingMessage):
    out_debug("Typing message callback...")
    return


def signal_story_message_cb(*args):
    out_debug("Story message callback...")
    terminal_bell()
    return


def signal_reaction_message_cb(account: SignalAccount, message: SignalReaction):
    out_debug("Reaction message callback...")
    terminal_bell()
    if common.CURRENT_RECIPIENT is not None:
        if message.recipient == common.CURRENT_RECIPIENT or message.sender == common.CURRENT_RECIPIENT:
            common.MAIN_WINDOW.messages_window.message_received()
    return


def signal_call_message_cb(*args):
    out_debug("Call message callback...")
    terminal_bell()
    return


#########################################
# Functions:
#########################################


def __do_resize__() -> None:
    """
    Do the resize of the windows:
    :return: None
    """
    # global _RESIZING, _MAIN_WINDOW
    common.RESIZING = True
    common.MAIN_WINDOW.resize()
    # _MAIN_WINDOW.redraw()
    common.RESIZING = False
    return


def __set_hover_focus__(mouse_pos: tuple[int, int]) -> None:
    """
    Set the focus based on mouse position.
    :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
    :return: None
    """
    # global _FOCUS_WINDOWS, _CURRENT_FOCUS, _MAIN_WINDOW
    # Do not switch focus if we're focusing on the status bar:
    if common.MAIN_WINDOW.status_bar.is_mouse_over(mouse_pos):
        return

    # Check that a menu is active, and if not, don't switch focus.
    if common.MAIN_WINDOW.menu_bar.is_menu_activated:
        return

    # Check if the mouse is over one of the sub windows:
    if common.MAIN_WINDOW.is_sub_window_visible:
        window = common.MAIN_WINDOW.get_visible_sub_window()
        if window.is_mouse_over(mouse_pos):
            set_current_focus(window.focus_id)
        else:
            set_current_focus(Focus.MAIN)
        return

    # Check if the mouse is over the menu bar:
    if common.MAIN_WINDOW.menu_bar.is_mouse_over(mouse_pos):
        set_current_focus(Focus.MENU_BAR)

    # Check if the mouse is over one of the primary windows:
    for window in common.MAIN_WINDOW.primary_windows:
        if window.is_mouse_over(mouse_pos):
            set_current_focus(window.focus_id)
    common.MAIN_WINDOW.contacts_window.hover_focus(mouse_pos)
    return


def __parse_mouse__() -> Optional[bool]:
    """
    Parse the mouse actions.
    :return: Optional[bool]: Return None: Char wasn't handled, processing should continue; Return True: char was
        handled, and processing shouldn't continue; Return False: char wasn't handled, processing shouldn't continue.
    """
    # global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Get the mouse position and button state:
    mouse_pos, button_state = get_mouse()
    # Update the status bar:
    common.MOUSE_POS = mouse_pos
    common.BUTTON_STATE = button_state

    # Pass the mouse to the currently visible sub-window:
    return_value: Optional[bool]
    if common.MAIN_WINDOW.is_sub_window_visible:
        window = common.MAIN_WINDOW.get_visible_sub_window()
        return_value = window.process_mouse(mouse_pos, button_state)
        if return_value is not None:
            if return_value is False:
                window.is_visible = False
            return return_value

    # Pass the mouse to the menu bar:
    if common.MAIN_WINDOW.menu_bar.is_mouse_over(mouse_pos):
        return_value = common.MAIN_WINDOW.menu_bar.process_mouse(mouse_pos, button_state)
        if return_value is not None:
            return return_value

    # Pass the mouse to a main window if the mouse is over it:
    for window in common.MAIN_WINDOW.primary_windows:
        if window.is_mouse_over(mouse_pos):
            return_value = window.process_mouse(mouse_pos, button_state)
            if return_value is not None:
                return return_value

    # Mouse move focus:
    if common.SETTINGS['mouseMoveFocus']:
        __set_hover_focus__(mouse_pos)
    return False


def set_current_focus(value: Focus) -> None:
    """
    Set the _CURRENT_FOCUS variable.
    :param value: Focus: The focus enum value for the window.
    :return: None
    """
    # global _CURRENT_FOCUS, _LAST_FOCUS, _FOCUS_WINDOWS
    if not isinstance(value, Focus):
        __type_error__("value", "Focus", value)
    if value != common.CURRENT_FOCUS:
        common.FOCUS_WINDOWS[common.CURRENT_FOCUS].is_focused = False
        common.LAST_FOCUS = common.CURRENT_FOCUS
        common.CURRENT_FOCUS = value
        common.FOCUS_WINDOWS[common.CURRENT_FOCUS].is_focused = True
    return


def inc_focus() -> None:
    """
    Increment the window focus.
    :return: None
    """
    # global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Increment focus:
    next_focus: int = common.CURRENT_FOCUS + 1
    # Wrap focus if needed:
    if next_focus > Focus.MENU_BAR:
        next_focus = Focus.CONTACTS
    # Set new focus
    set_current_focus(Focus(next_focus))
    return


def dec_focus() -> None:
    """
    Decrement the focus.
    :return: None
    """
    # global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Decrement focus:
    next_focus: int = common.CURRENT_FOCUS - 1
    # Wrap focus if necessary:
    if next_focus < Focus.CONTACTS:
        next_focus = Focus.MENU_BAR
    # Set the new focus:
    set_current_focus(Focus(next_focus))
    return


def __preprocess_key__(char_code: int) -> Optional[bool]:
    """
    Pre-process a key, catches resize.
    :param char_code: int: The char code received.
    :return: Optional[bool]: True if char handled and processing shouldn't continue. False if not handled and processing
        shouldn't continue, return None key wasn't handled and processing should continue.
    """
    if char_code == curses.KEY_RESIZE:
        __do_resize__()
        return True
    elif char_code == curses.KEY_MOUSE:
        return __parse_mouse__()
    return None


def __stop_mouse__() -> None:
    """
    Stop the mouse support:
    :return: None
    """
    # Pull in reset mouse mask:
    # global common.MOUSE_RESET_MASK
    out_info("Stopping mouse.")
    # If it's not None, reset the mouse mask.
    if common.MOUSE_RESET_MASK is not None:
        out_debug("Resetting mouse mask.")
        curses.mousemask(common.MOUSE_RESET_MASK)
    # Tell the terminal to stop processing mouse movements:
    out_debug("Sending terminal stop report characters.")
    print('\033[?1003l', end='', flush=True)
    return


def __start_mouse__() -> bool:
    """
    Start the mouse.
    :return: bool: True mouse was started, False it was not.
    """
    # Pull in reset mouse mask:
    # global _MOUSE_RESET_MASK
    out_info("Starting mouse support.")
    # Set the curses mouse mask:
    out_debug('Setting mouse mask...')
    response = curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    if response == 0:  # Complete failure returns 0, no mask to reset to.
        common.MOUSE_RESET_MASK = None
        out_warning("Error starting mouse, not using mouse.")
        return False
    else:  # Response is a tuple (avail_mask, old_mask)
        out_debug("Setting mouse mask success.")
        common.MOUSE_RESET_MASK = response[1]
    # Tell the terminal to report mouse movement.
    out_debug("Sending terminal control characters...")
    print('\033[?1003h', end='', flush=True)
    return True


#########################################
# Main:
#########################################
def main(std_screen: curses.window, signal_cli: SignalCli) -> None:
    """
    Main.
    :param std_screen: curses.window: The std_screen main window.
    :param signal_cli: The SignalCli instance.
    :return: None
    """
    # global _DEBUG, _VERBOSE, _CURRENT_FOCUS, _LAST_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW, _RESIZING, _EXIT_ERROR

    # Set up extended key codes; And turn off the cursor:
    std_screen.keypad(True)
    std_screen.nodelay(True)
    if not common.DEBUG:
        curses.curs_set(False)

    # Set up colour pairs according to theme:
    if not curses.has_extended_color_support():
        message: str = "Terminal must have 256 colour support."
        out_error(message)
        _EXIT_ERROR = RuntimeError(message)
        return
    theme: dict[str, dict[str, int | bool | str]] = load_theme()
    init_colours(theme)

    # Set up the mouse:
    if common.SETTINGS['useMouse']:
        if not __start_mouse__():
            common.SETTINGS['useMouse'] = False

    # Create the callback dict:
    callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]] = {
        'file': {
            'settings': (file_menu_settings_cb, None),
            'quit': (file_menu_quit_cb, None),
        },
        'accounts': {
            'switch': (accounts_menu_switch_cb, None),
            'link': (accounts_menu_link_cb, [signal_cli]),
            'register': (accounts_menu_register_cb, None),
        },
        'help': {
            'shortcuts': (help_menu_shortcuts_cb, None),
            'about': (help_menu_about_cb, None),
            'version': (help_menu_version_cb, None),
        },
    }

    # Create the main windows:
    main_window = MainWindow(
        std_screen=std_screen,
        theme=theme,
        callbacks=callbacks,
    )

    # Store references to the windows for focus, and redrawing:
    common.MAIN_WINDOW = main_window
    common.FOCUS_WINDOWS = (
        main_window, main_window.contacts_window, main_window.messages_window, main_window.typing_window,
        main_window.menu_bar, main_window.status_bar, main_window.quit_window, main_window.link_window,
        main_window.qr_window, main_window.ver_window
    )
    # Call set_current_focus for the first time:
    set_current_focus(Focus.CONTACTS)
    main_window.contacts_window.is_focused = True
    # Set visible status items:
    if common.DEBUG:
        main_window.status_bar.is_char_code_visible = True
        if common.SETTINGS['useMouse']:
            main_window.status_bar.is_mouse_visible = True
    # main_window.redraw()
    try:
        # Main loop:
        while True:
            try:
                # Input loop:
                while True:
                    # Draw the main window:
                    main_window.redraw()

                    # If the account has changed, change the account in the contacts window.
                    if common.CURRENT_ACCOUNT_CHANGED:
                        main_window.contacts_window.account_changed()
                        common.CURRENT_ACCOUNT_CHANGED = False

                    # If the recipient has changed, change the recipient in the messages window.
                    if common.CURRENT_RECIPIENT_CHANGED:
                        main_window.messages_window.recipient_changed()
                        common.CURRENT_RECIPIENT_CHANGED = False

                    # Get the character and update the status bar if required.
                    char_code: int = std_screen.getch()

                    # If no char, continue:
                    if char_code == -1:
                        continue

                    # Update the character code on the status bar:
                    common.CHAR_CODE = char_code

                    # Pre-process char code, catches mouse, and resize events:
                    char_handled = __preprocess_key__(char_code)
                    if char_handled is not None:
                        continue

                    # Check if a sub-window is visible, and if so, hand the key there:
                    #   If it returns False, hide the window.
                    if main_window.is_sub_window_visible:
                        sub_window: Window = main_window.get_visible_sub_window()
                        char_handled = sub_window.process_key(char_code)
                        if char_handled is False:
                            sub_window.is_visible = False
                            set_current_focus(Focus.MENU_BAR)
                            continue
                        elif char_handled is True:
                            continue

                    # Secondly, check the menu bar for the key press, IE: The 'F' keys.:
                    char_handled = main_window.menu_bar.process_key(char_code)
                    if char_handled is not None:
                        set_current_focus(Focus.MENU_BAR)
                        continue

                    # Check the 'Contacts' window for accelerators: 'C' & 'G' only if it's not focused:
                    if not main_window.contacts_window.is_focused:
                        char_handled = main_window.contacts_window.process_key(char_code)
                        if char_handled is not None:
                            if char_handled is True:
                                set_current_focus(Focus.CONTACTS)
                                if char_code in main_window.contacts_window.contacts_win.focus_chars:
                                    main_window.contacts_window.current_focus = common.ContactsFocus.CONTACTS
                                elif char_code in main_window.contacts_window.groups_win.focus_chars:
                                    main_window.contacts_window.current_focus = common.ContactsFocus.GROUPS
                            continue
                    # Pass the char to the typing window, and if it returns True, a message was sent.
                    if common.CURRENT_FOCUS == Focus.TYPING:
                        char_handled = main_window.typing_window.process_key(char_code)
                        if char_handled is True:
                            main_window.messages_window.message_received()
                            continue
                        elif char_handled is False:
                            continue

                    # Finally, send the key to the focused primary window:
                    char_handled = common.FOCUS_WINDOWS[common.CURRENT_FOCUS].process_key(char_code)
                    if char_handled is not None:
                        continue

                    # Switch focus on Tab and Shift Tab, only if a sub-window isn't visible.
                    if not main_window.is_sub_window_visible:
                        if char_code == common.KEY_TAB:
                            inc_focus()
                        elif char_code == common.KEY_SHIFT_TAB:
                            dec_focus()

            except KeyboardInterrupt:
                if not common.SETTINGS['quitConfirm']:
                    raise Quit()
                else:
                    file_menu_quit_cb("", std_screen)
                    continue

            except (curses.error, SignalError) as e:
                _EXIT_ERROR = e
                raise Quit

    except Quit:
        pass
    # Fix mouse mask:
    __stop_mouse__()
    return


#########################################
# Start up functions:
#########################################
def __start_receive_thread__(signal_cli: SignalCli) -> None:
    """
    Start the receive thread
    :return: None
    """
    if common.RECEIVE_THREAD is not None:
        raise RuntimeError("Receive already started.")
    out_info("Starting receive thread.")
    thread = signal_cli.start_receive(
        account=common.CURRENT_ACCOUNT,
        received_message_callback=(signal_received_message_cb, None),
        receipt_message_callback=(signal_receipt_message_cb, None),
        sync_message_callback=(signal_sync_message_cb, None),
        typing_message_callback=(signal_typing_message_cb, None),
        story_message_callback=(signal_story_message_cb, None),
        reaction_message_callback=(signal_reaction_message_cb, None),
        call_message_callback=(signal_call_message_cb, None),
        do_expunge=common.SETTINGS['doExpunge'],
    )
    out_info("Receive thread started.")
    common.RECEIVE_THREAD = thread
    return


def __stop_receive_thread__(signal_cli: SignalCli) -> None:
    if common.RECEIVE_THREAD is None:
        raise RuntimeError("Receive already stopped.")
    out_info("Stopping receive thread.")
    signal_cli.stop_receive(common.CURRENT_ACCOUNT)
    out_info("Receive thread stopped.")
    return


def __setup_contacts_user_obj__(account: SignalAccount):
    contacts: SignalContacts = account.contacts
    for contact in contacts:
        if not isinstance(contact.user_obj, dict):
            contact.user_obj = {
                'sound': '<DEFAULT>',
            }
    return


if __name__ == '__main__':

    # Setup .cliSignal directory, and change to it:
    if not os.path.exists(common.WORKING_DIR):
        try:
            os.mkdir(common.WORKING_DIR, 0o700)
        except (OSError, PermissionError, FileNotFoundError):
            out_error("Failed to create '%s' directory." % common.WORKING_DIR)
            exit(2)

    # Check working directory permissions, and if they are wrong, abort.
    if oct(os.stat(common.WORKING_DIR).st_mode)[-3:] != oct(0o700)[-3:]:
        out_error("Working directory: '%s', permissions are not 700." % common.WORKING_DIR)
        exit(3)
    common.SETTINGS['workingDir'] = common.WORKING_DIR
    # Change to working directory:
    os.chdir(common.WORKING_DIR)

    # Setup command line arguments:
    parser = arguments.create_parser()
    # Parse args:
    _args: argparse.Namespace = parser.parse_args()

    # Parse --debug and --verbose options:
    log_level = logging.WARNING
    if _args.debug:
        common.DEBUG = True
        common.VERBOSE = True
        prettyPrint.DEBUG = True
        prettyPrint.VERBOSE = True
        common.LOG_LEVEL = logging.DEBUG
        runCallback.set_suppress_error(False)
    elif _args.verbose:
        common.DEBUG = False
        common.VERBOSE = True
        prettyPrint.VERBOSE = True
        common.LOG_LEVEL = logging.INFO

    # Set logging path:
    common.SETTINGS['logPath'] = common.CLI_SIGNAL_LOG_PATH
    logging.basicConfig(filename=common.CLI_SIGNAL_LOG_PATH, encoding='utf-8', level=common.LOG_LEVEL,
                        format='%(levelname)s : [%(asctime)s] : (%(name)s) : %(message)s')
    common.LOGGER = logging.getLogger(__name__)
    common.LOGGER.debug("Logging started.")

    # Parse --config option:
    cli_signal_config_path: str = common.CLI_SIGNAL_CONFIG_FILE_PATH
    if _args.config is not None:
        cli_signal_config_path: str = _args.config

    # load config:
    try:
        config_file: ConfigFile = ConfigFile(config_name=common.CONFIG_NAME,
                                             file_path=cli_signal_config_path,
                                             set_permissions=0o600,
                                             enforce_permissions=True,
                                             create_default=True,
                                             do_load=True
                                             )
    except ConfigFileError as _e:
        if _e.error_number == 21:
            out_error("Permissions of config file must be 600.")
        else:
            out_error("ConfigFileError: %s" % _e.error_message)
        exit(4)

    # Validate / act on arguments:
    arguments.act_on_settings(_args)

    # Check the signal socket path:
    if common.SETTINGS['signalSocketPath'] is not None:
        if (not os.path.exists(common.SETTINGS['signalSocketPath']) or
                not os.path.isfile(common.SETTINGS['signalSocketPath'])):
            out_error("--signalSocketPath must point to an existing socket file.")
            exit(5)

    # Check the signal exec path:
    if common.SETTINGS['signalExecPath'] is not None and (not os.path.exists(common.SETTINGS['signalExecPath']) or
                                                          not os.path.isfile(common.SETTINGS['signalExecPath'])):
        out_error("--signalExecPath must point to an existing signal-cli executable file.")
        exit(6)

    # Verify arguments; If --noStartSignal, --signalSocketPath must be defined:
    if _args.noStartSignal and common.SETTINGS['signalSocketPath'] is None:
        out_error("--signalSocketPath must point to an existing file if using --noStartSignal.")
        exit(7)

    # Verify theme is correct:
    if common.SETTINGS['theme'] not in ('light', 'dark', 'custom'):
        out_error("--theme must be one of: 'light', 'dark', or 'custom'")
        exit(9)
    if common.SETTINGS['theme'] == 'custom':
        # If there is no theme path, throw an error.
        if _args.themePath is None and common.SETTINGS['themePath'] is None:
            out_error("If --theme is 'custom', either --themePath must be supplied, or 'themePath' must be "
                      "defined in your configuration file.")
            exit(10)
        # Override settings theme path with the args theme path:
        # elif _args.themePath is not None:
        #     common.SETTINGS['themePath'] = _args.themePath
        # Check that the theme path exists:
        if not os.path.exists(common.SETTINGS['themePath']) or not os.path.isfile(common.SETTINGS['themePath']):
            out_error("'themePath' must point to an existing file.")
            exit(11)

    ################################
    # Parse settings:

    ################################
    # Parse --account:
    if _args.account is not None:
        common.SETTINGS['defaultAccount'] = _args.account
    #################################
    # Parse: --store
    if _args.store:
        try:
            config_file.save()
        except ConfigFileError as e:
            out_error(e.error_message)
            exit(12)

    # Make signal-cli config dir if required:
    if not os.path.exists(common.SETTINGS['signalConfigDir']):
        try:
            os.mkdir(common.SIGNAL_CONFIG_DIR, 0o700)
        except (OSError, FileNotFoundError, PermissionError):
            out_error("Failed to create '%s' directory." % common.SETTINGS['signalConfigDir'])
            exit(13)

    # Start signal:
    out_info("Starting signal-cli...", force=True)
    try:
        _signal_cli: SignalCli = SignalCli(
            signal_config_path=common.SETTINGS['signalConfigDir'],
            signal_exec_path=common.SETTINGS['signalExecPath'],
            log_file_path=common.SIGNAL_LOG_PATH,
            server_address=common.SETTINGS['signalSocketPath'],
            start_signal=common.SETTINGS['startSignal'],
            callback=(signal_start_up_cb, None),
        )
    except FileNotFoundError as _e:
        out_error("Failed to start signal-cli: %s" % _e.args[0])
        exit(14)
    except FileExistsError as _e:
        out_error("Failed to start signal-cli: %s" % _e.args[0])
        exit(15)
    except SignalAlreadyRunningError:
        out_error("Failed to start signal-cli, signal instance already running.")
        exit(16)
    except TimeoutError as _e:
        out_error("Failed to start signal-cli: %s" % _e.args[0])
        exit(17)

    # Load the account:
    if common.SETTINGS['defaultAccount'] is not None:
        try:
            common.CURRENT_ACCOUNT = _signal_cli.accounts.get_by_number(common.SETTINGS['defaultAccount'])
        except ValueError as _e:
            out_error("Invalid account, number not in right format.")
            _signal_cli.stop_signal()
            exit(18)
        if common.CURRENT_ACCOUNT is None:
            out_error("Account: %s not registered." % common.SETTINGS['defaultAccount'])
            _signal_cli.stop_signal()
            exit(19)
    elif len(_signal_cli.accounts) > 0:
        common.CURRENT_ACCOUNT = _signal_cli.accounts[0]

    if common.CURRENT_ACCOUNT is not None:
        __setup_contacts_user_obj__(common.CURRENT_ACCOUNT)
        __start_receive_thread__(_signal_cli)

    # Run main:
    common.IS_CURSES_STARTED = True
    curses.wrapper(main, _signal_cli)
    common.IS_CURSES_STARTED = False

    if common.RECEIVE_THREAD is not None:
        out_info("Stopping Receive thread.")
        _signal_cli.stop_receive(common.CURRENT_ACCOUNT)
        out_info("Receive thread stopped.")

    # Stop signal
    out_info("Stopping signal.", force=True)
    if _signal_cli.link_thread is not None:
        _signal_cli.stop_link_thread()
    _signal_cli.stop_signal()

    # Check for error:
    if common.EXIT_ERROR is not None:
        if common.RESIZING:
            out_error("Window size too small. Fatal.")
        out_error("EXITED DUE TO ERROR: %s" % str(common.EXIT_ERROR.args))
        if isinstance(common.EXIT_ERROR, SignalError):
            out_error("Signal error code: %i" % common.EXIT_ERROR.code)
            out_error("Signal error message: %s" % common.EXIT_ERROR.message)
            if common.DEBUG:
                raise common.EXIT_ERROR

        if common.DEBUG:
            print(common.EXIT_ERROR.__traceback__)
            raise common.EXIT_ERROR
        exit(20)
    exit(0)
