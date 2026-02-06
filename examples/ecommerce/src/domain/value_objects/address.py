"""Address value object for shipping and billing addresses."""

from typing import Self


class Address:
    """Address value object representing a physical address.
    
    Addresses are immutable and validated on creation.
    Used for both shipping and billing addresses.
    """

    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
    ) -> None:
        """Initialize address value object.
        
        Args:
            street: Street address
            city: City name
            state: State or province
            postal_code: Postal or ZIP code
            country: Country code or name
            
        Raises:
            ValueError: If any required field is empty
        """
        if not street or not street.strip():
            raise ValueError("Street address is required")
        if not city or not city.strip():
            raise ValueError("City is required")
        if not state or not state.strip():
            raise ValueError("State is required")
        if not postal_code or not postal_code.strip():
            raise ValueError("Postal code is required")
        if not country or not country.strip():
            raise ValueError("Country is required")
        
        self._street = street.strip()
        self._city = city.strip()
        self._state = state.strip()
        self._postal_code = postal_code.strip()
        self._country = country.strip()

    @property
    def street(self) -> str:
        """Get street address.
        
        Returns:
            Street address string
        """
        return self._street

    @property
    def city(self) -> str:
        """Get city name.
        
        Returns:
            City name string
        """
        return self._city

    @property
    def state(self) -> str:
        """Get state or province.
        
        Returns:
            State string
        """
        return self._state

    @property
    def postal_code(self) -> str:
        """Get postal code.
        
        Returns:
            Postal code string
        """
        return self._postal_code

    @property
    def country(self) -> str:
        """Get country.
        
        Returns:
            Country string
        """
        return self._country

    def __eq__(self, other: object) -> bool:
        """Equality comparison by value.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if all address fields are equal
        """
        if not isinstance(other, Address):
            return False
        return (
            self._street == other._street
            and self._city == other._city
            and self._state == other._state
            and self._postal_code == other._postal_code
            and self._country == other._country
        )

    def __hash__(self) -> int:
        """Hash based on all address fields.
        
        Returns:
            Hash value
        """
        return hash((
            self._street,
            self._city,
            self._state,
            self._postal_code,
            self._country,
        ))

    def __str__(self) -> str:
        """String representation.
        
        Returns:
            Formatted address string
        """
        return (
            f"{self._street}, {self._city}, {self._state} "
            f"{self._postal_code}, {self._country}"
        )

    def __repr__(self) -> str:
        """Developer representation.
        
        Returns:
            Developer-friendly string representation
        """
        return (
            f"Address('{self._street}', '{self._city}', '{self._state}', "
            f"'{self._postal_code}', '{self._country}')"
        )
