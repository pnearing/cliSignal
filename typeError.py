#!/usr/bin/env python3
"""
File: typeError.py
    Add __type_error__ to programs.
"""
from typing import Any, NoReturn, Final, Optional

# Try and load logging:
_HAVE_LOGGING: bool = True
try:
    import logging
except (ModuleNotFoundError, ImportError):
    _HAVE_LOGGING = False

# Try and load syslog
_HAVE_SYSLOG: bool = True
try:
    from syslog import syslog, LOG_CRIT
except (ModuleNotFoundError, ImportError):
    _HAVE_SYSLOG = False

# Version:
VERSION: Final[float] = 1.1
"""typeError.py Version."""
USE_SYSLOG: bool = True
"""Use the syslog module to log the TypeError, True enables logging, False disables; Overridden by a ModuleError or an
   ImportError of the syslog module."""
USE_LOGGING: bool = True
"""Use the logging module to log the TypeError, True enables logging, False disables; Overridden by a ModuleError or an
   ImportError on import of the logging module."""


def __type_error__(argument_name: str, desired_types: str, received_obj: Any) -> NoReturn:
    """
    Raise a TypeError with a good message.
    :param argument_name: Str: String of the variable name.
    :param desired_types: Str: String of desired type(s).
    :param received_obj: The var which was received, note: type() will be called on it.
    :return: NoReturn
    """
    error_message: str = "TypeError: Argument: '%s', got '%s' type, expected type : '%s'" \
                         % (argument_name, str(type(received_obj)), desired_types)
    if _HAVE_LOGGING and USE_LOGGING:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + __type_error__.__name__)
        logger.critical(error_message)
    if _HAVE_SYSLOG and USE_SYSLOG:
        syslog(LOG_CRIT, error_message)
    raise TypeError(error_message)
