#!/usr/bin/env python3
from typing import Optional

# Settings for configFile:
SETTINGS: dict[str, Optional[str | bool]] = {
    'signalExecPath': None,
    'signalConfigDir': None,
    'signalLogFile': None,
    'signalSocketPath': None,
    'startSignal': True,
}
print("INIT", flush=True)
