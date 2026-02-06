"""Product entity representing a catalog item."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from src.domain.value_objects.money import Money


class ProductStatus(Enum):
    """Product status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(frozen=True)
class ProductId:
    """Product ID value object."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value


@dataclass(frozen=True)
class CategoryId:
    """Category ID value object."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value


class Product:
    """Product entity representing a catalog item.
    
    Products have identity, price, stock, and belong to categories.
    Products can be active or inactive.
    """

    def __init__(
        self,
        product_id: ProductId,
        name: str,
        price: Money,
        sku: str,
        stock_quantity: int = 0,
        status: ProductStatus = ProductStatus.ACTIVE,
        description: Optional[str] = None,
        category_ids: Optional[list[CategoryId]] = None,
    ) -> None:
        """Initialize product entity.
        
        Args:
            product_id: Unique product identifier
            name: Product name
            price: Product price
            sku: Stock Keeping Unit (unique identifier)
            stock_quantity: Available stock quantity
            status: Product status (default: ACTIVE)
            description: Product description (optional)
            category_ids: List of category IDs (optional)
            
        Raises:
            ValueError: If name is empty, SKU is empty, or stock is negative
        """
        if not name or not name.strip():
            raise ValueError("Product name is required")
        if len(name) > 200:
            raise ValueError("Product name cannot exceed 200 characters")
        if not sku or not sku.strip():
            raise ValueError("SKU is required")
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        if description and len(description) > 2000:
            raise ValueError("Description cannot exceed 2000 characters")
        
        self._id = product_id
        self._name = name.strip()
        self._price = price
        self._sku = sku.strip()
        self._stock_quantity = stock_quantity
        self._status = status
        self._description = description.strip() if description else None
        self._category_ids = category_ids or []
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

    @property
    def id(self) -> ProductId:
        """Get product ID.
        
        Returns:
            Product ID value object
        """
        return self._id

    @property
    def name(self) -> str:
        """Get product name.
        
        Returns:
            Product name string
        """
        return self._name

    @property
    def price(self) -> Money:
        """Get product price.
        
        Returns:
            Money value object
        """
        return self._price

    @property
    def sku(self) -> str:
        """Get SKU.
        
        Returns:
            SKU string
        """
        return self._sku

    @property
    def stock_quantity(self) -> int:
        """Get stock quantity.
        
        Returns:
            Available stock quantity
        """
        return self._stock_quantity

    @property
    def status(self) -> ProductStatus:
        """Get product status.
        
        Returns:
            Product status enumeration
        """
        return self._status

    @property
    def description(self) -> Optional[str]:
        """Get product description.
        
        Returns:
            Description or None
        """
        return self._description

    @property
    def category_ids(self) -> list[CategoryId]:
        """Get category IDs.
        
        Returns:
            List of category IDs
        """
        return self._category_ids.copy()

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp.
        
        Returns:
            Creation datetime
        """
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get last update timestamp.
        
        Returns:
            Last update datetime
        """
        return self._updated_at

    def update_price(self, new_price: Money) -> None:
        """Update product price.
        
        Args:
            new_price: New price to set
        """
        self._price = new_price
        self._updated_at = datetime.utcnow()

    def update_stock(self, new_quantity: int) -> None:
        """Update stock quantity.
        
        Args:
            new_quantity: New stock quantity
            
        Raises:
            ValueError: If quantity is negative
        """
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self._stock_quantity = new_quantity
        self._updated_at = datetime.utcnow()

    def decrease_stock(self, quantity: int) -> None:
        """Decrease stock quantity.
        
        Args:
            quantity: Quantity to decrease
            
        Raises:
            ValueError: If quantity is negative or exceeds available stock
        """
        if quantity < 0:
            raise ValueError("Decrease quantity cannot be negative")
        if quantity > self._stock_quantity:
            raise ValueError("Insufficient stock")
        
        self._stock_quantity -= quantity
        self._updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the product."""
        self._status = ProductStatus.ACTIVE
        self._updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the product."""
        self._status = ProductStatus.INACTIVE
        self._updated_at = datetime.utcnow()

    def is_available(self) -> bool:
        """Check if product is available for purchase.
        
        Returns:
            True if product is active and has stock
        """
        return (
            self._status == ProductStatus.ACTIVE
            and self._stock_quantity > 0
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison by identity.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if product IDs are equal
        """
        if not isinstance(other, Product):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash based on product ID.
        
        Returns:
            Hash value
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """Developer representation.
        
        Returns:
            Developer-friendly string representation
        """
        return (
            f"Product(id={self._id}, name='{self._name}', "
            f"price={self._price}, stock={self._stock_quantity})"
        )
