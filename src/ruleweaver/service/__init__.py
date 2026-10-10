"""The calculation service: approved rules over HTTP, with API keys and usage metering.

Needs the `service` extra. Nothing in the core imports this package.
"""

from .api import NOTICE, create_api
from .keys import ApiKey, KeyStore

__all__ = ["NOTICE", "ApiKey", "KeyStore", "create_api"]
