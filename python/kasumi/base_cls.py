from __future__ import annotations

# This file contains the basement classes for the Kasumi SDK like Token
from enum import Enum

class TokenType(Enum):
    """
    This class is used to represent the type of a token.
    """
    PLAINTEXT = "plaintext"
    ENCRYPTION = "encryption"