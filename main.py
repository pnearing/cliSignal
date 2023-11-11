#!/usr/bin/env python3
from typing import Final, Optional, Callable, Any
import argparse
import os.path
import curses
from enum import IntEnum
from SignalCliApi.signalCli import SignalCli
from configFile import ConfigFile, ConfigFileError
import common
from themes import load_theme, init_colours
from mainWindow import MainWindow
from contactsWindow import ContactsWindow
from messagesWindow import MessagesWindow
from typingWindow import TypingWindow
from linkWindow import LinkWindow
from menuBar import MenuBar
from quitWindow import QuitWindow

#########################################
# Enums:
#########################################
class Focus(IntEnum):
    """
    Focused windows / elements. Indexes focus_windows list.
    """
    MAIN = 0
    CONTACTS = 1
    MESSAGES = 2
    TYPING = 3
    MENU_BAR = 4


#########################################
# Constants:
#########################################
_WORKING_DIR_NAME: Final[str] = '.cliSignal'
"""Name of the working directory under $HOME."""
_CONFIG_NAME: Final[str] = 'cliSignal'
"""Name to give our config file configuration."""
_CONFIG_FILE_NAME: Final[str] = 'cliSignal.config'
"""Name of the cliSignal config file."""
_SIGNAL_CONFIG_DIR_NAME: Final[str] = 'signal-cli'
"""Name to give the signal-cli config directory. (where signal-cli stores it's files)."""
_SIGNAL_LOG_FILE_NAME: Final[str] = 'signal-cli.log'
"""Name of the signal-cli log file."""
_CLI_SIGNAL_LOG_FILE_NAME: Final[str] = 'cliSignal.log'
"""Name of the cliSignal log file."""
_WORKING_DIR: Final[str] = os.path.join(os.environ.get("HOME"), _WORKING_DIR_NAME)
"""The full path to the working directory."""
_SIGNAL_LOG_PATH: Final[str] = os.path.join(_WORKING_DIR, _SIGNAL_LOG_FILE_NAME)
"""The full path to the log file."""
_SIGNAL_CONFIG_DIR: Final[str] = os.path.join(_WORKING_DIR, _SIGNAL_CONFIG_DIR_NAME)
"""The full path to the default signal-cli config directory."""
_CLI_SIGNAL_CONFIG_FILE_PATH: Final[str] = os.path.join(_WORKING_DIR, _CONFIG_FILE_NAME)
"""The full path to the cli signal config file."""

#########################################
# Vars:
#########################################
# _CURRENT_FOCUS: Focus = Focus.MAIN
_CURRENT_FOCUS: Focus = Focus.MENU_BAR


#########################################
# My menu callbacks:
#########################################
def main_menu_file_cb(status: str, window: curses.window, *args: list[Any]) -> None:
    """
    Main menu file callback.
    :param status: str: The current status, either 'activated' or 'deactivated'.
    :param window: curses.window: The std_screen object.
    :return: None
    """
    return


def main_menu_accounts_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Main menu accounts callback.
    :return: None
    """
    return


def main_menu_help_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Main menu help callback.
    :return:
    """
    return


def file_menu_settings_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    File menu settings callback.
    :return: None
    """
    return


def file_menu_quit_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    File menu quit callback.
    :return: None
    """
    raise KeyboardInterrupt


def accounts_menu_switch_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Accounts menu, switch callback.
    :return: None
    """
    return


def accounts_menu_link_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Accounts menu, link callback.
    :return: None
    """
    curses.beep()
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


def help_menu_version_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    The help menu, version callback.
    :return: None
    """
    return


#########################################
# Signal callbacks:
#########################################
def signal_start_up_cb(state: str) -> None:
    """
    Signal start up callback.
    :param state: str, the current state of the startup process.
    :return: None
    """
    print("SIGNAL:", state)
    return


def signal_received_message_cb():
    return


def signal_receipt_message_cb():
    return


def signal_sync_message_cb():
    return


def signal_typing_message_cb():
    return


def signal_story_message_cb():
    return


def signal_payment_message_cb():
    return


def signal_reaction_message_cb():
    return


def signal_call_message_cb():
    return


#########################################
# Functions:
#########################################
def confirm_quit(quit_window: QuitWindow) -> bool:
    """
    Show an "are you sure message", and return users' input.
    :return: bool: True, the user quits; False, the user doesn't quit.
    """
    message: str = common.STRINGS['messages']['quit']
    confirm_str: str = common.STRINGS['other']['yesOrNo']

    return True


#########################################
# Main:
#########################################
def main(std_screen: curses.window, signal_cli: SignalCli) -> None:
    global _CURRENT_FOCUS
    # Setup extended key codes:
    std_screen.keypad(True)

    # Ask for mouse move events, and position change event:
    reset_mouse_mask: Optional[int] = None
    if common.SETTINGS['useMouse']:
        # Set the curses mouse mask:
        response = curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        if response != 0:  # Complete failure returns 0, no mask to reset to.
            common.SETTINGS['useMouse'] = False
        else:  # Response is a tuple (avail_mask, old_mask)
            reset_mouse_mask = response[1]

    # Setup colour pairs according to theme:
    if not curses.has_extended_color_support():
        raise RuntimeError("Terminal capable of 256 colours required.")
    theme: dict[str, dict[str, int | bool | str]] = load_theme()
    init_colours(theme)

    # Create sub-windows:
    link_window: LinkWindow = LinkWindow((22, 22), (3, 3), theme)
    quit_window: QuitWindow = QuitWindow((23, 4), (3, 3), theme)
    # Create the callback dict:
    callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]] = {
        'main': {
            'file': (main_menu_file_cb, None),
            'accounts': (main_menu_accounts_cb, None),
            'help': (main_menu_help_cb, None),
        },
        'file': {
            'settings': (file_menu_settings_cb, None),
            'quit': (file_menu_quit_cb, None),
        },
        'accounts': {
            'switch': (accounts_menu_switch_cb, None),
            'link': (accounts_menu_link_cb, [link_window, signal_cli]),
            'register': (accounts_menu_register_cb, None),
        },
        'help': {
            'shortcuts': (help_menu_shortcuts_cb, None),
            'about': (help_menu_about_cb, None),
            'version': (help_menu_version_cb, None),
        },
    }

    # Create the windows:
    main_window = MainWindow(std_screen, theme, callbacks)

    # Store references to the windows for focus:
    focus_windows: tuple[MainWindow, ContactsWindow, MessagesWindow, TypingWindow, MenuBar] = (
        main_window, main_window.contacts_window, main_window.messages_window, main_window.typing_window,
        main_window.menu_bar
    )

    # Set initial focus
    focus_windows[_CURRENT_FOCUS].is_focused = True

    # Draw the window for the first time:
    main_window.redraw()

    # Main loop:
    while True:
        try:
            std_screen.move(0, 0)
            while True:
                char_code: int = std_screen.getch()
                std_screen.addstr(10, 10, "    ")
                std_screen.addstr(10, 10, str(char_code))
                std_screen.refresh()

                # Pre-process char code:
                if char_code == curses.KEY_RESIZE:  # Resize the windows:
                    main_window.resize()
                    main_window.redraw()
                    continue
                elif char_code == curses.KEY_MOUSE:  # Mouse move / button hit:
                    _, mouse_col, mouse_row, _, button_state = curses.getmouse()
                    mouse_pos: tuple[int, int] = (mouse_row, mouse_col)
                    # Set the window focus:
                    focus_windows[_CURRENT_FOCUS].is_focused = False
                    if focus_windows[Focus.CONTACTS].is_mouse_over(mouse_pos):
                        _CURRENT_FOCUS = Focus.CONTACTS
                    elif focus_windows[Focus.MESSAGES].is_mouse_over(mouse_pos):
                        _CURRENT_FOCUS = Focus.MESSAGES
                    elif focus_windows[Focus.TYPING].is_mouse_over(mouse_pos):
                        _CURRENT_FOCUS = Focus.TYPING
                    elif focus_windows[Focus.MENU_BAR].is_mouse_over(mouse_pos):
                        _CURRENT_FOCUS = Focus.MENU_BAR
                    focus_windows[_CURRENT_FOCUS].is_focused = True
                    # TODO: Process button state.
                    continue

                # Hand the char code to the appropriate window for handling.
                char_handled: bool
                if _CURRENT_FOCUS == Focus.MENU_BAR:
                    char_handled = focus_windows[Focus.MENU_BAR].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue
                elif _CURRENT_FOCUS == Focus.CONTACTS:
                    char_handled = focus_windows[Focus.CONTACTS].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue
                elif _CURRENT_FOCUS == Focus.MESSAGES:
                    char_handled = focus_windows[Focus.MESSAGES].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue
                elif _CURRENT_FOCUS == Focus.TYPING:
                    char_handled = focus_windows[Focus.TYPING].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue

                # If the window didn't handle the character, we want to handle it:
                if char_code == common.KEY_TAB:  # Tab hit switch focus.
                    # Un-focus current focus, and increment focus:
                    focus_windows[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS += 1
                    # Wrap focus if needed:
                    if _CURRENT_FOCUS > Focus.MENU_BAR:
                        _CURRENT_FOCUS = Focus.CONTACTS
                    # Set the new focus and redraw:
                    focus_windows[_CURRENT_FOCUS].is_focused = True
                    main_window.redraw()
                    curses.doupdate()
                    continue
                elif char_code == common.KEY_SHIFT_TAB:  # Shift-Tab hit, switch focus backwards.
                    # Un-focus current focus, and decrement focus:
                    focus_windows[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS -= 1
                    # Wrap focus if necessary:
                    if _CURRENT_FOCUS < Focus.CONTACTS:
                        _CURRENT_FOCUS = Focus.MENU_BAR
                    # Set the focus and redraw:
                    focus_windows[_CURRENT_FOCUS].is_focused = True
                    main_window.redraw()
                    curses.doupdate()
                    continue
                elif char_code == curses.KEY_F1:
                    # Shift the focus to the menu bar:
                    focus_windows[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS = Focus.MENU_BAR
                    focus_windows[_CURRENT_FOCUS].is_focused = True
                    # Activate the file menu:
                    menu_bar = main_window.menu_bar
                    # If there is a menu currently active, deactivate it.
                    if menu_bar.is_menu_activated:
                        menu_bar.menu_bar_items[menu_bar.selection].deactivate()
                    # Set the selection to the file menu, set the active menu and activate the file menu.:
                    menu_bar.selection = common.MenuBarSelections.FILE
                    menu_bar._active_menu = menu_bar.menus[menu_bar.selection]
                    menu_bar.menu_bar_items[menu_bar.selection].activate()
                    # Redraw the window:
                    main_window.redraw()
                    curses.doupdate()
                    continue
                elif char_code == curses.KEY_F2:
                    # Shift the focus to the menu bar:
                    focus_windows[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS = Focus.MENU_BAR
                    focus_windows[_CURRENT_FOCUS].is_focused = True
                    # Activate the accounts menu:
                    menu_bar = main_window.menu_bar
                    # If there is an active menu, deactivate it.
                    if menu_bar.is_menu_activated:
                        menu_bar.menu_bar_items[menu_bar.selection].deactivate()
                    # Set the selection to the accounts menu:
                    menu_bar.selection = common.MenuBarSelections.ACCOUNTS
                    menu_bar._active_menu = menu_bar.menus[menu_bar.selection]
                    menu_bar.menu_bar_items[menu_bar.selection].activate()
                    # Redraw the window:
                    main_window.redraw()
                    curses.doupdate()
                    continue
                elif char_code == curses.KEY_F3:
                    # Shift focus to menu bar:
                    focus_windows[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS = Focus.MENU_BAR
                    focus_windows[_CURRENT_FOCUS].is_focused = True
                    # Activate the help menu:
                    menu_bar = main_window.menu_bar
                    # If there is an active menu, deactivate it:
                    if menu_bar.is_menu_activated:
                        menu_bar.menu_bar_items[menu_bar.selection].deactivate()
                    menu_bar.selection = common.MenuBarSelections.HELP
                    menu_bar._active_menu = menu_bar.menus[menu_bar.selection]
                    menu_bar.menu_bar_items[menu_bar.selection].activate()
                    # Redraw the window:
                    main_window.redraw()
                    curses.doupdate()
                    continue

        except KeyboardInterrupt:

            user_response: bool = confirm_quit()
            break  # TODO: Are you sure message.

    # Fix mouse mask:
    if common.SETTINGS['useMouse']:
        curses.mousemask(reset_mouse_mask)

    return


#########################################
# Start:
#########################################
if __name__ == '__main__':
    # Setup .cliSignal directory, and change to it:
    if not os.path.exists(_WORKING_DIR):
        try:
            os.mkdir(_WORKING_DIR, 0o700)
        except (OSError, PermissionError, FileNotFoundError):
            print("ERROR: Failed to create '%s' directory." % _WORKING_DIR)
            exit(2)

    # Check working directory permissions, and if they are wrong abort.
    if oct(os.stat(_WORKING_DIR).st_mode)[-3:] != oct(0o700)[-3:]:
        print("ERROR: Working directory: '%s', permissions are not 700." % _WORKING_DIR)
        exit(3)
    common.SETTINGS['workingDir'] = _WORKING_DIR
    # Change to working directory:
    os.chdir(_WORKING_DIR)

    # Setup command line arguments:
    parser = argparse.ArgumentParser(description="Command line Signal client.",
                                     epilog="Written by Peter Nearing."
                                     )
    # Config options:
    parser.add_argument('--config',
                        help="The full path to the config file, default is $HOME/.cliSignal/cliSignal.config",
                        type=str
                        )
    parser.add_argument('--store',
                        help="Save the command line options to the config.",
                        action='store_true',
                        default=False
                        )
    # Signal options:
    parser.add_argument('--signalConfigDir',
                        help="The full path to the signal config directory.",
                        type=str
                        )
    parser.add_argument('--signalSocketPath',
                        help="The full path to the socket file. If you are starting signal (the default action, "
                             "this must be a directory. Otherwise if using --noStartSignal, this must be an existing "
                             "socket file.",
                        type=str
                        )
    parser.add_argument('--signalExecPath',
                        help="The full path to the signal-cli executable.",
                        type=str
                        )
    parser.add_argument('--noStartSignal',
                        help="Start the signal daemon.",
                        action='store_true',
                        default=False
                        )
    # Colour theme options:
    parser.add_argument('--theme',
                        help='The theme to use, either "light", "dark", or "custom".',
                        type=str
                        )
    parser.add_argument('--themePath',
                        help="The path to the custom theme json file, required if --theme=custom",
                        type=str
                        )
    # Settings:
    # Use mouse:
    use_mouse = parser.add_mutually_exclusive_group()
    use_mouse.add_argument('--useMouse',
                           help="Try and use the mouse, NOTE: Sometimes this leaves the terminal in an unstable state.",
                           action='store_true',
                           default=False
                           )
    use_mouse.add_argument('--noUseMouse',
                           help="Turn the mouse off.",
                           action='store_false',
                           dest='useMouse'
                           )
    # Parse args:
    _args: argparse.Namespace = parser.parse_args()

    # Parse --config option:
    cli_signal_config_path: str = _CLI_SIGNAL_CONFIG_FILE_PATH
    if _args.config is not None:
        cli_signal_config_path: str = _args.config

    # load config:
    try:
        config_file: ConfigFile = ConfigFile(config_name=_CONFIG_NAME,
                                             file_path=cli_signal_config_path,
                                             set_permissions=0o600,
                                             enforce_permissions=True,
                                             create_default=True,
                                             do_load=True
                                             )
    except ConfigFileError as e:
        if e.error_number == 21:
            print("ERROR: Permissions of config file must be 600.")
        else:
            print("ERROR: ConfigFileError:", e.error_message)
        exit(4)

    # Validate / act on arguments:
    # Signal arguments:
    # --noStartSignal:
    if _args.noStartSignal:
        common.SETTINGS['startSignal'] = False

    # --signalConfigDir:
    common.SETTINGS['signalConfigDir'] = _SIGNAL_CONFIG_DIR
    if _args.signalConfigDir is not None:
        common.SETTINGS['signalConfigDir'] = _args.signalConfigPath

    # --signalSocketPath:
    if _args.signalSocketPath is not None:
        common.SETTINGS['signalSocketPath'] = _args.signalSocketFile
    if common.SETTINGS['signalSocketPath'] is not None:
        if (not os.path.exists(common.SETTINGS['signalSocketPath']) or
                not os.path.isfile(common.SETTINGS['signalSocketPath'])):
            print("ERROR: --signalSocketPath must point to an existing socket file.")
            exit(6)

    # --signalExecPath:
    if _args.signalExecPath is not None:
        common.SETTINGS['signalExecPath'] = _args.signalExecPath
    if common.SETTINGS['signalExecPath'] is not None and (not os.path.exists(common.SETTINGS['signalExecPath']) or
                                                          not os.path.isfile(common.SETTINGS['signalExecPath'])):
        print("ERROR: --signalExecPath must point to an existing signal-cli executable file.")
        exit(7)

    # Verify arguments; If --noStartSignal, --signalSocketPath must be defined:
    if _args.noStartSignal and common.SETTINGS['signalSocketPath'] is None:
        print("ERROR: --signalSocketPath must point to an existing file if using --noStartSignal.")
        exit(8)

    # Theme arguments:
    # --theme:
    if _args.theme is not None:
        if _args.theme not in ('light', 'dark', 'custom'):
            print("ERROR: --theme must be either: 'light', 'dark', or 'custom'.")
            exit(9)
        common.SETTINGS['theme'] = _args.theme
    # Verify theme is correct:
    if common.SETTINGS['theme'] not in ('light', 'dark', 'custom'):
        print("ERROR: 'theme' must be one of: 'light', 'dark', or 'custom'")
        exit(10)
    if common.SETTINGS['theme'] == 'custom':
        # If there is no theme path, throw an error.
        if _args.themePath is None and common.SETTINGS['themePath'] is None:
            print("ERROR: If --theme is 'custom', either --themePath must be supplied, or 'themePath' must be "
                  "defined in your configuration file.")
            exit(11)
        # Override settings theme path with the args theme path:
        elif _args.themePath is not None:
            common.SETTINGS['themePath'] = _args.themePath
        # Check that the theme path exists:
        if not os.path.exists(common.SETTINGS['themePath']) or not os.path.isfile(common.SETTINGS['themePath']):
            print("ERROR: 'themePath' must point to an existing file.")
            exit(12)

    # Settings arguments:
    # Use mouse:
    common.SETTINGS['useMouse'] = _args.useMouse

    # Parse: --store
    if _args.store:
        try:
            config_file.save()
        except ConfigFileError as e:
            print("ERROR:", e.error_message)
            exit(9)

    # Make signal-cli config dir if required:
    if not os.path.exists(common.SETTINGS['signalConfigDir']):
        try:
            os.mkdir(_SIGNAL_CONFIG_DIR, 0o700)
        except (OSError, FileNotFoundError, PermissionError):
            print("ERROR: Failed to create '%s' directory.")
            exit(4)

    # Start signal:
    print("Starting signal.")
    _signal_cli: SignalCli = SignalCli(
        signal_config_path=common.SETTINGS['signalConfigDir'],
        signal_exec_path=common.SETTINGS['signalExecPath'],
        log_file_path=_SIGNAL_LOG_PATH,
        server_address=common.SETTINGS['signalSocketPath'],
        start_signal=common.SETTINGS['startSignal'],
        callback=(signal_start_up_cb, None),
        # debug=True
    )

    # Tell the terminal to report mouse movements:
    if common.SETTINGS['useMouse']:
        print('\033[?1003h', end='', flush=True)

    # Run main:
    curses.wrapper(main, _signal_cli)

    # Tell the terminal to not report mouse movements:
    if common.SETTINGS['useMouse']:
        print('\033[?1003l', end='', flush=True)

    # Stop signal
    print("Stopping signal.")
    _signal_cli.stop_signal()
    exit(0)
