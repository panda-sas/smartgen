"""User entity representing a customer or admin user."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.domain.value_objects.email import Email


class UserRole(Enum):
    """User role enumeration."""

    CUSTOMER = "customer"
    ADMIN = "admin"
    VENDOR = "vendor"


@dataclass(frozen=True)
class UserId:
    """User ID value object."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value


class User:
    """User entity representing a registered user.
    
    Users can be customers, admins, or vendors. Each user has
    a unique identity and can have a profile with personal information.
    """

    def __init__(
        self,
        user_id: UserId,
        email: Email,
        password_hash: str,
        role: UserRole = UserRole.CUSTOMER,
    ) -> None:
        """Initialize user entity.
        
        Args:
            user_id: Unique user identifier
            email: User email address
            password_hash: Hashed password (never store plain text)
            role: User role (default: CUSTOMER)
            
        Raises:
            ValueError: If password hash is empty
        """
        if not password_hash or not password_hash.strip():
            raise ValueError("Password hash is required")
        
        self._id = user_id
        self._email = email
        self._password_hash = password_hash.strip()
        self._role = role
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None
        self._phone_number: Optional[str] = None

    @property
    def id(self) -> UserId:
        """Get user ID.
        
        Returns:
            User ID value object
        """
        return self._id

    @property
    def email(self) -> Email:
        """Get user email.
        
        Returns:
            Email value object
        """
        return self._email

    @property
    def role(self) -> UserRole:
        """Get user role.
        
        Returns:
            User role enumeration
        """
        return self._role

    @property
    def first_name(self) -> Optional[str]:
        """Get first name.
        
        Returns:
            First name or None
        """
        return self._first_name

    @property
    def last_name(self) -> Optional[str]:
        """Get last name.
        
        Returns:
            Last name or None
        """
        return self._last_name

    @property
    def phone_number(self) -> Optional[str]:
        """Get phone number.
        
        Returns:
            Phone number or None
        """
        return self._phone_number

    def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> None:
        """Update user profile information.
        
        Args:
            first_name: New first name (optional)
            last_name: New last name (optional)
            phone_number: New phone number (optional)
        """
        if first_name is not None:
            self._first_name = first_name.strip() if first_name else None
        if last_name is not None:
            self._last_name = last_name.strip() if last_name else None
        if phone_number is not None:
            self._phone_number = phone_number.strip() if phone_number else None

    def change_role(self, new_role: UserRole) -> None:
        """Change user role.
        
        Args:
            new_role: New role to assign
            
        Raises:
            ValueError: If role change is invalid
        """
        # Business rule: Only admins can change roles (enforced in application layer)
        self._role = new_role

    def __eq__(self, other: object) -> bool:
        """Equality comparison by identity.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if user IDs are equal
        """
        if not isinstance(other, User):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash based on user ID.
        
        Returns:
            Hash value
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """Developer representation.
        
        Returns:
            Developer-friendly string representation
        """
        return f"User(id={self._id}, email={self._email}, role={self._role.value})"
