#!/usr/bin/env python3
from typing import Optional
import argparse
import os.path
import curses
from SignalCliApi import SignalCli
from configFile import ConfigFile, ConfigFileError
import common


def add_title_to_win(window: curses.window, title: str) -> None:
    """
    Add a provided title to a given window.
    :param window: The curser window to draw on.
    :param title: The title to add.
    :return: None
    """
    # Add start and end chars to the title.
    message: str = "\u2562 " + title + " \u255F"
    num_rows, num_cols = window.getmaxyx()
    col: int = int(num_cols / 2) - int(len(message) / 2)
    window.addstr(0, col, message)
    return


def add_char(window: curses.window,
             row: int,
             col: int,
             character: str,
             attrs: Optional[int] = None
             ) -> None:
    """
    Add a character to the screen, taking into account the exception that occurs when printing to the bottom right of
    the window.
    :param window: curses.window: The window to add to.
    :param row: int: The row to add at.
    :param col: int: The column to add at.
    :param character: str: The character to add.
    :param attrs: Optional[int]: The attributes to add.
    :return: None
    """
    num_rows, num_cols = window.getmaxyx()
    max_row = num_rows - 1
    max_col = num_cols - 1
    if row == max_row and col == max_col:
        try:
            if attrs is not None:
                window.addch(row, col, character, attrs)
            else:
                window.addch(row, col, character)
        except curses.error:
            pass
    else:
        if attrs is not None:
            window.addch(row, col, character, attrs)
        else:
            window.addch(row, col, character)
    return


def colour_border(window: curses.window,
                  ls: str = "\u2502",
                  rs: str = "\u2502",
                  ts: str = "\u2500",
                  bs: str = "\u2500",
                  tl: str = "\u250C",
                  tr: str = "\u2510",
                  bl: str = "\u2514",
                  br: str = "\u2518",
                  attrs: Optional[int] = None
                  ) -> None:
    """
    Draw a coloured border around a given window.
    :param window: The window to draw on.
    :param ls: str: The left side character, defaults to "│".
    :param rs: str: The right side character, defaults to "│".
    :param ts: str: The top side character, defaults to "─".
    :param bs: str: The bottom side character, defaults to "─".
    :param tl: str: The top left corner character, defaults to "┌".
    :param tr: str: The top right corner character, defaults to "┐".
    :param bl: str: The bottom left corner character, defaults to "└".
    :param br: str: The bottom right corner character, defaults to "┘".
    :param attrs: Optional[int]: The attributes to set for the border.
    :return: None
    """
    num_rows, num_cols = window.getmaxyx()
    max_row = num_rows - 1
    max_col = num_cols - 1
    # Draw top side:
    for col in range(1, max_col - 1):
        add_char(window=window, row=0, col=col, character=ts, attrs=attrs)
    # Draw bottom side:
    for col in range(1, max_col - 1):
        add_char(window=window, row=0, col=col, character=bs, attrs=attrs)
    # Draw left side:
    for row in range(1, max_row - 1):
        add_char(window=window, row=row, col=0, character=ls, attrs=attrs)
    # Draw right side:
    for row in range(1, max_row - 1):
        add_char(window=window, row=row, col=0, character=rs, attrs=attrs)
    return


def main(std_screen: curses.window) -> None:
    std_screen.attron(curses.A_BOLD)
    # std_screen.border()
    colour_border(std_screen, attrs=(curses.COLOR_BLUE | curses.A_BOLD))
    # add_title_to_win(std_screen, "cliSignal")
    std_screen.attroff(curses.A_BOLD)
    std_screen.addch(10, 10, "X", 0)
    std_screen.refresh()
    # _signal_cli: SignalCli = SignalCli(signal_config_path=common.SETTINGS['signalConfigDir'],
    #                                    signal_exec_path=common.SETTINGS['signalExecPath'],
    #                                    log_file_path=common.SETTINGS['signalLogFile'],
    #                                    server_address=common.SETTINGS['signalSocketFile'],
    #                                    start_signal=common.SETTINGS['startSignal']
    #                                    )
    curses.napms(3000)
    return


if __name__ == '__main__':
    # Setup command line arguments:
    parser = argparse.ArgumentParser(description="Command line Signal client.",
                                     epilog="Written by Peter Nearing."
                                     )
    parser.add_argument('--config',
                        help="The full path to the config file, default is $HOME/.config/cliSignal.config",
                        type=str
                        )
    parser.add_argument('--store',
                        help="Save the command line options to the config.",
                        action='store_true',
                        default=False
                        )
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
    parser.add_argument('--signalLogFile',
                        help="The full path to the signal log file, by default logging is turned off.",
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
    # Parse args:
    args: argparse.Namespace = parser.parse_args()

    # load config:
    try:
        config_file: ConfigFile = ConfigFile("cliSignal",
                                             file_path=args.config,
                                             set_permissions=0o600,
                                             enforce_permissions=True
                                             )
    except ConfigFileError as e:
        if e.error_number == 21:
            print("ERROR: Permissions of config file must be 600.")
        else:
            print("ERROR:", e.error_message)
        exit(2)
    # Validate / act on arguments:

    # --noStartSignal:
    if args.noStartSignal:
        common.SETTINGS['startSignal'] = False

    # --signalConfigDir:
    if args.signalConfigDir is not None:
        common.SETTINGS['signalConfigDir'] = args.signalConfigPath

    if common.SETTINGS['signalConfigDir'] is not None and (not os.path.exists(common.SETTINGS['signalConfigDir']) or
                                                           not os.path.isdir(common.SETTINGS['signalConfigDir'])):
        print("ERROR: --signalConfigPath must be an existing directory.")
        exit(3)

    # --signalSocketPath:
    print("DEBUG:", str(common.SETTINGS.keys()))
    if args.signalSocketPath is not None:
        common.SETTINGS['signalSocketPath'] = args.signalSocketFile
    if common.SETTINGS['signalSocketPath'] is not None:
        if (not os.path.exists(common.SETTINGS['signalSocketPath']) or
                not os.path.isfile(common.SETTINGS['signalSocketPath'])):
            print("ERROR: --signalSocketPath must point to an existing socket file.")
            exit(4)
    if args.noStartSignal and common.SETTINGS['signalSocketPath'] is None:
        print("ERROR: --signalSocketPath must point to an existing file if using --noStartSignal.")
        exit(5)

    # --signalLogFilename:
    if args.signalLogFile is not None:
        common.SETTINGS['signalLogFile'] = args.signalLogFilename
    # Check that the log file containing directory exists:
    if common.SETTINGS['signalLogFile'] is not None:
        log_dir: str = os.path.join(*os.path.split(common.SETTINGS['signalLogFile'])[:-1])
        if not os.path.exists(log_dir) or not os.path.isdir(log_dir):
            print("ERROR: Directory containing the log file doesn't exist.")
            exit(6)

    # --signalExecPath:
    if args.signalExecPath is not None:
        common.SETTINGS['signalExecPath'] = args.signalExecPath
    if common.SETTINGS['signalExecPath'] is not None and (not os.path.exists(common.SETTINGS['signalExecPath']) or
                                                          not os.path.isfile(common.SETTINGS['signalExecPath'])):
        print("ERROR: --signalExecPath must point to an existing signal-cli executable file.")
        exit(7)

    curses.wrapper(main)
    exit(0)
