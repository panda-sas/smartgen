"""Email value object for user email addresses."""

import re
from typing import Self


class Email:
    """Email value object with validation.
    
    Email addresses must be valid according to RFC 5322 specification.
    This value object ensures email addresses are properly formatted and
    immutable once created.
    """

    # Basic email regex pattern (RFC 5322 compliant)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    def __init__(self, value: str) -> None:
        """Initialize email value object.
        
        Args:
            value: Email address string
            
        Raises:
            ValueError: If email format is invalid
        """
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string")
        
        value = value.strip().lower()
        
        if not self.EMAIL_PATTERN.match(value):
            raise ValueError(f"Invalid email format: {value}")
        
        self._value = value

    @property
    def value(self) -> str:
        """Get the email address value.
        
        Returns:
            Email address string
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """Equality comparison by value.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if emails are equal, False otherwise
        """
        if not isinstance(other, Email):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """Hash based on email value.
        
        Returns:
            Hash of email value
        """
        return hash(self._value)

    def __str__(self) -> str:
        """String representation.
        
        Returns:
            Email address string
        """
        return self._value

    def __repr__(self) -> str:
        """Developer representation.
        
        Returns:
            Developer-friendly string representation
        """
        return f"Email('{self._value}')"
