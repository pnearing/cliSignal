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

#####################################
# Constants:
#####################################
_VERSION: Final[str] = '1.1.2'
"""typeError.py Version."""

#####################################
# Variables:
#####################################
_USE_SYSLOG: bool = True
"""Use the syslog module to log the TypeError, True enables logging, False disables; Overridden by a ModuleError or an
   ImportError of the syslog module."""
_USE_LOGGING: bool = False
"""Use the logging module to log the TypeError, True enables logging, False disables; Overridden by a ModuleError or an
   ImportError on import of the logging module."""
_SUPPRESS_ERROR: bool = False
"""Return the TypeError object, instead of raising it."""


#####################################
# Properties:
#####################################
def version() -> str:
    """
    The current version of typeError.py.
    :returns: str: The current version.
    """
    global _VERSION
    return _VERSION


def use_syslog() -> bool:
    """
    Use syslog to log the error?
    :returns: bool: The current state.
    """
    global _USE_SYSLOG
    return _USE_SYSLOG


def set_use_syslog(value: bool) -> None:
    """
    Use syslog to log the error?
    Setter.
    :returns: None.
    :raises TypeError: If value is not a bool.
    """
    global _USE_SYSLOG
    if not isinstance(value, bool):
        raise TypeError("'use_syslog' value must be a bool.")
    _USE_SYSLOG = value
    return


def use_logging() -> bool:
    """
    Use the logging module to log the error?
    :returns: bool: The current state.
    """
    global _USE_LOGGING
    return _USE_LOGGING


def set_use_logging(value: bool) -> None:
    """
    Use the logging module to log the error?
    Setter.
    :returns: None.
    :raises TypeError: If value is not a bool.
    """
    global _USE_LOGGING
    if not isinstance(value, bool):
        raise TypeError("'use_logging' must be a bool.")
    _USE_LOGGING = value
    return


def suppress_error() -> bool:
    """
    Should we suppress the error and return it, or should we raise the error?
    :returns: bool: The current state.
    """
    global _SUPPRESS_ERROR
    return _SUPPRESS_ERROR


def set_suppress_error(value: bool) -> None:
    """
    Should we suppress the error and return it, or should we raise the error?
    Setter.
    :returns: None.
    :raises TypeError: If value is not a bool.
    """
    global _SUPPRESS_ERROR
    if not isinstance(value, bool):
        raise TypeError("'suppress_error' must be a bool.")
    _SUPPRESS_ERROR = value
    return


#####################################
# Type error function:
#####################################
def __type_error__(argument_name: str,
                   desired_types: str,
                   received_obj: Any,
                   *args
                   ) -> NoReturn:
    """
    Raise a TypeError with a good message.
    :param argument_name: Str: String of the variable name.
    :param desired_types: Str: String of desired type(s).
    :param received_obj: Any: The var which was received, note: type() will be called on it.
    :param args: tuple[Any, ...]: Any additional arguments to pass on to the type error.
    :return: NoReturn
    """
    # Pull in vars:
    global _HAVE_SYSLOG, _HAVE_LOGGING, _USE_LOGGING, _USE_SYSLOG, _SUPPRESS_ERROR
    # Create the error message:
    error_message: str = "TypeError: Argument: '%s', received '%s' type, expected type(s): '%s'." \
                         % (argument_name, str(type(received_obj)), desired_types)
    # Log to logging:
    if _HAVE_LOGGING and _USE_LOGGING:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + __type_error__.__name__)
        logger.critical(error_message)
    # Log to syslog:
    if _HAVE_SYSLOG and _USE_SYSLOG:
        syslog(LOG_CRIT, error_message)
    # Create the error and return / raise it:
    error: TypeError = TypeError(error_message, *args)
    if _SUPPRESS_ERROR:
        return error
    raise error
