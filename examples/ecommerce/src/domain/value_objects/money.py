"""Money value object for currency amounts."""

from decimal import Decimal
from typing import Self


class Money:
    """Money value object representing a currency amount.
    
    Money is immutable and ensures amounts are always positive.
    Uses Decimal for precise decimal arithmetic.
    """

    def __init__(self, amount: Decimal | float | str, currency: str = "USD") -> None:
        """Initialize money value object.
        
        Args:
            amount: Monetary amount (Decimal, float, or string)
            currency: Currency code (default: USD)
            
        Raises:
            ValueError: If amount is negative or invalid
        """
        if isinstance(amount, str):
            amount = Decimal(amount)
        elif isinstance(amount, float):
            amount = Decimal(str(amount))
        elif not isinstance(amount, Decimal):
            raise ValueError("Amount must be Decimal, float, or string")
        
        if amount < 0:
            raise ValueError("Money amount cannot be negative")
        
        # Round to 2 decimal places for currency
        self._amount = amount.quantize(Decimal('0.01'))
        self._currency = currency.upper()

    @property
    def amount(self) -> Decimal:
        """Get the monetary amount.
        
        Returns:
            Decimal amount
        """
        return self._amount

    @property
    def currency(self) -> str:
        """Get the currency code.
        
        Returns:
            Currency code string
        """
        return self._currency

    def add(self, other: Self) -> Self:
        """Add another money amount.
        
        Args:
            other: Other money object to add
            
        Returns:
            New Money object with sum
            
        Raises:
            ValueError: If currencies don't match
        """
        if self._currency != other._currency:
            raise ValueError(f"Cannot add {self._currency} and {other._currency}")
        
        return Money(self._amount + other._amount, self._currency)

    def multiply(self, multiplier: Decimal | float | int) -> Self:
        """Multiply money by a multiplier.
        
        Args:
            multiplier: Multiplier value
            
        Returns:
            New Money object with multiplied amount
        """
        if isinstance(multiplier, float):
            multiplier = Decimal(str(multiplier))
        elif isinstance(multiplier, int):
            multiplier = Decimal(multiplier)
        
        return Money(self._amount * multiplier, self._currency)

    def __eq__(self, other: object) -> bool:
        """Equality comparison by value.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if amounts and currencies are equal
        """
        if not isinstance(other, Money):
            return False
        return self._amount == other._amount and self._currency == other._currency

    def __hash__(self) -> int:
        """Hash based on amount and currency.
        
        Returns:
            Hash value
        """
        return hash((self._amount, self._currency))

    def __str__(self) -> str:
        """String representation.
        
        Returns:
            Formatted money string
        """
        return f"{self._currency} {self._amount:.2f}"

    def __repr__(self) -> str:
        """Developer representation.
        
        Returns:
            Developer-friendly string representation
        """
        return f"Money({self._amount}, '{self._currency}')"
