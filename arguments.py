#!/usr/bin/env python3
"""
File: arguments.py
    Functions to create and handle the arguments to the program.
"""
import argparse
import logging

import common
import prettyPrint
import runCallback


def create_parser() -> argparse.ArgumentParser:
    """
    Create and return an argument parser:
    :return: argparse.ArgumentParser
    """
    # Create the parser:
    parser = argparse.ArgumentParser(description="Command line Signal client.",
                                     epilog="Written by Peter Nearing."
                                     )

    # DEBUG or verbose:
    debug_or_verbose = parser.add_mutually_exclusive_group()
    debug_or_verbose.add_argument('--debug',
                                  help="Debugging mode, be ware of the odd exception. Implies --verbose.",
                                  action='store_true',
                                  default=False
                                  )
    debug_or_verbose.add_argument('--verbose',
                                  help="Produce verbose output.",
                                  action='store_true',
                                  default=False
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
                        help="Don't start the signal daemon.",
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
                           default=None
                           )
    use_mouse.add_argument('--noUseMouse',
                           help="Turn the mouse off.",
                           action='store_false',
                           dest='useMouse'
                           )

    # Confirm on quit:
    quit_confirm = parser.add_mutually_exclusive_group()
    quit_confirm.add_argument('--confirmQuit',
                              help="Confirm before exit.",
                              action='store_true',
                              default=None
                              )
    quit_confirm.add_argument('--noConfirmQuit',
                              help="Don't confirm before exit.",
                              action='store_false',
                              dest='confirmQuit',
                              )

    # Mouse movement focus:
    mouse_focus = parser.add_mutually_exclusive_group()
    mouse_focus.add_argument('--mouseFocus',
                             help="Focus window on mouse movement.",
                             action='store_true',
                             default=None,
                             )
    mouse_focus.add_argument('--noMouseFocus',
                             help="Don't focus on mouse movement.",
                             action='store_false',
                             dest='mouseFocus'
                             )

    # Use sounds:
    use_sound = parser.add_mutually_exclusive_group()
    use_sound.add_argument('--useSound',
                           help="Use the terminal bell when events happen.",
                           action='store_true',
                           default=None
                           )
    use_sound.add_argument('--noUseSound',
                           help="Do not use the terminal bell when events occur.",
                           action='store_false',
                           dest='useSound'
                           )
    # Flash screen on beep:
    use_flash = parser.add_mutually_exclusive_group()
    use_flash.add_argument('--flashScreen',
                           help='Flash the screen on beep.',
                           action='store_true',
                           default=None
                           )
    use_flash.add_argument('--noFlashScreen',
                           help="Don't flash the screen on beep.",
                           action='store_false',
                           dest='flashScreen')
    # Hide unknown contact:
    hide_unknown_contact = parser.add_mutually_exclusive_group()
    hide_unknown_contact.add_argument('--hideUnknownContacts',
                                      help="Hide contacts without a name or number.",
                                      action='store_true',
                                      default=None)
    hide_unknown_contact.add_argument('--noHideUnknownContacts',
                                      help="Don't hid contacts with out a name or number.",
                                      action='store_true',
                                      dest='hideUnknownContacts'
                                      )

    # Account argument:
    parser.add_argument('--account',
                        help="The account to use.",
                        type=str
                        )

    return parser


def act_on_settings(args) -> None:
    """
    Act on the different program settings.
    :param args:
    :return:
    """
    # --noStartSignal:
    if args.noStartSignal:
        common.SETTINGS['startSignal'] = False
    common.out_debug("start signal = %s" % str(common.SETTINGS['startSignal']))

    # --signalConfigDir:
    common.SETTINGS['signalConfigDir'] = common.SIGNAL_CONFIG_DIR
    if args.signalConfigDir is not None:
        common.SETTINGS['signalConfigDir'] = args.signalConfigPath
    common.out_debug("signal conf dir = %s" % str(common.SETTINGS['signalConfigDir']))

    # --signalSocketPath:
    if args.signalSocketPath is not None:
        common.SETTINGS['signalSocketPath'] = args.signalSocketFile
    common.out_debug("signal socket path = %s" % str(common.SETTINGS['signalSocketPath']))

    # --signalExecPath:
    if args.signalExecPath is not None:
        common.SETTINGS['signalExecPath'] = args.signalExecPath
    common.out_debug("signal exec path = %s" % str(common.SETTINGS['signalExecPath']))

    # --theme:
    if args.theme is not None:
        common.SETTINGS['theme'] = args.theme
    common.out_debug('theme = %s' % common.SETTINGS['theme'])

    # --themePath:
    if args.themePath is not None:
        common.SETTINGS['themePath'] = args.themePath
    common.out_debug('theme path = %s' % str(common.SETTINGS['themePath']))
    # --useMouse / --noUseMouse:
    if args.useMouse is not None:
        common.SETTINGS['useMouse'] = args.useMouse
    common.out_debug("useMouse = %s" % str(common.SETTINGS['useMouse']))

    # --confirmQuit / --noConfirmQuit:
    if args.confirmQuit is not None:
        common.SETTINGS['quitConfirm'] = args.confirmQuit
    common.out_debug("quitConfirm = %s" % str(common.SETTINGS['quitConfirm']))

    if args.mouseFocus is not None:
        common.SETTINGS['mouseMoveFocus'] = args.mouseFocus
    common.out_debug("mouseMoveFocus = %s" % str(common.SETTINGS['mouseMoveFocus']))

    # Use sounds:
    if args.useSound is not None:
        common.SETTINGS['useSound'] = args.useSound
    common.out_debug('useSound = %s' % str(common.SETTINGS['useSound']))

    # Flash screen:
    if args.flashScreen is not None:
        common.SETTINGS['flashScreen'] = args.flashScreen
    common.out_debug('flashScreen = %s' % str(common.SETTINGS['flashScreen']))

    # Hide unknown contacts:
    if args.hideUnknownContacts is not None:
        common.SETTINGS['hideUnknownContacts'] = args.hideUnknownContacts
    common.out_debug("Hide unknown contacts = %s" % str(common.SETTINGS['hideUnknownContacts']))
