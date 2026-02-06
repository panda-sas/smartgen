"""Order aggregate root representing a customer order."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from src.domain.value_objects.address import Address
from src.domain.value_objects.money import Money


class OrderStatus(Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderId:
    """Order ID value object."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value


@dataclass(frozen=True)
class UserId:
    """User ID value object."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value


@dataclass(frozen=True)
class ProductId:
    """Product ID value object."""

    value: str

    def __str__(self) -> str:
        """String representation."""
        return self.value


@dataclass(frozen=True)
class OrderItem:
    """Order item value object (immutable snapshot).
    
    Order items are snapshots of product information at the time
    of order creation. They cannot be modified after order creation.
    """

    product_id: ProductId
    product_name: str
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        """Validate order item after initialization."""
        if self.quantity <= 0:
            raise ValueError("Order item quantity must be positive")
        if not self.product_name or not self.product_name.strip():
            raise ValueError("Product name is required")

    @property
    def subtotal(self) -> Money:
        """Calculate item subtotal.
        
        Returns:
            Subtotal (quantity * unit_price)
        """
        return self.unit_price.multiply(self.quantity)

    def __eq__(self, other: object) -> bool:
        """Equality comparison by value."""
        if not isinstance(other, OrderItem):
            return False
        return (
            self.product_id == other.product_id
            and self.product_name == other.product_name
            and self.quantity == other.quantity
            and self.unit_price == other.unit_price
        )

    def __hash__(self) -> int:
        """Hash based on all fields."""
        return hash((
            self.product_id,
            self.product_name,
            self.quantity,
            self.unit_price,
        ))


class Order:
    """Order aggregate root.
    
    Orders represent customer purchases. An order contains order items,
    shipping/billing addresses, and tracks order status through its lifecycle.
    
    Business Rules:
    - Orders must contain at least one item
    - Order total must equal sum of items plus shipping and tax
    - Orders can only be cancelled if not yet shipped
    - Order status transitions follow: PENDING -> CONFIRMED -> SHIPPED -> DELIVERED
    """

    def __init__(
        self,
        order_id: OrderId,
        customer_id: UserId,
        shipping_address: Address,
        billing_address: Address,
        items: list[OrderItem],
        shipping_cost: Money,
        tax_amount: Money,
    ) -> None:
        """Initialize order aggregate.
        
        Args:
            order_id: Unique order identifier
            customer_id: Customer user ID
            shipping_address: Shipping address
            billing_address: Billing address
            items: List of order items
            shipping_cost: Shipping cost
            tax_amount: Tax amount
            
        Raises:
            ValueError: If order is invalid (no items, invalid total)
        """
        if not items:
            raise ValueError("Order must contain at least one item")
        
        self._id = order_id
        self._customer_id = customer_id
        self._shipping_address = shipping_address
        self._billing_address = billing_address
        self._items = items.copy()  # Defensive copy
        self._shipping_cost = shipping_cost
        self._tax_amount = tax_amount
        self._status = OrderStatus.PENDING
        self._order_date = datetime.utcnow()
        self._tracking_number: Optional[str] = None
        
        # Validate order total
        self._validate_order_total()

    def _validate_order_total(self) -> None:
        """Validate that order total matches items plus shipping and tax."""
        items_subtotal = sum(
            item.subtotal.amount for item in self._items
        )
        expected_total = (
            items_subtotal
            + self._shipping_cost.amount
            + self._tax_amount.amount
        )
        # Allow small floating point differences
        if abs(self.total.amount - expected_total) > 0.01:
            raise ValueError(
                f"Order total mismatch: expected {expected_total}, "
                f"got {self.total.amount}"
            )

    @property
    def id(self) -> OrderId:
        """Get order ID.
        
        Returns:
            Order ID value object
        """
        return self._id

    @property
    def customer_id(self) -> UserId:
        """Get customer ID.
        
        Returns:
            Customer user ID
        """
        return self._customer_id

    @property
    def shipping_address(self) -> Address:
        """Get shipping address.
        
        Returns:
            Shipping address value object
        """
        return self._shipping_address

    @property
    def billing_address(self) -> Address:
        """Get billing address.
        
        Returns:
            Billing address value object
        """
        return self._billing_address

    @property
    def items(self) -> list[OrderItem]:
        """Get order items (defensive copy).
        
        Returns:
            Copy of order items list
        """
        return self._items.copy()

    @property
    def status(self) -> OrderStatus:
        """Get order status.
        
        Returns:
            Order status enumeration
        """
        return self._status

    @property
    def order_date(self) -> datetime:
        """Get order date.
        
        Returns:
            Order creation datetime
        """
        return self._order_date

    @property
    def tracking_number(self) -> Optional[str]:
        """Get tracking number.
        
        Returns:
            Tracking number or None
        """
        return self._tracking_number

    @property
    def items_subtotal(self) -> Money:
        """Calculate items subtotal.
        
        Returns:
            Sum of all order items
        """
        total = Money(0)
        for item in self._items:
            total = total.add(item.subtotal)
        return total

    @property
    def total(self) -> Money:
        """Calculate order total.
        
        Returns:
            Total (items + shipping + tax)
        """
        return (
            self.items_subtotal
            .add(self._shipping_cost)
            .add(self._tax_amount)
        )

    def confirm(self) -> None:
        """Confirm the order (payment received).
        
        Raises:
            ValueError: If order cannot be confirmed
        """
        if self._status != OrderStatus.PENDING:
            raise ValueError(
                f"Cannot confirm order in {self._status.value} status"
            )
        self._status = OrderStatus.CONFIRMED

    def ship(self, tracking_number: str) -> None:
        """Ship the order.
        
        Args:
            tracking_number: Shipping tracking number
            
        Raises:
            ValueError: If order cannot be shipped
        """
        if self._status != OrderStatus.CONFIRMED:
            raise ValueError(
                f"Cannot ship order in {self._status.value} status"
            )
        if not tracking_number or not tracking_number.strip():
            raise ValueError("Tracking number is required")
        
        self._status = OrderStatus.SHIPPED
        self._tracking_number = tracking_number.strip()

    def mark_delivered(self) -> None:
        """Mark order as delivered.
        
        Raises:
            ValueError: If order cannot be marked as delivered
        """
        if self._status != OrderStatus.SHIPPED:
            raise ValueError(
                f"Cannot mark order as delivered in {self._status.value} status"
            )
        self._status = OrderStatus.DELIVERED

    def cancel(self) -> None:
        """Cancel the order.
        
        Raises:
            ValueError: If order cannot be cancelled
        """
        if self._status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise ValueError(
                f"Cannot cancel order in {self._status.value} status"
            )
        self._status = OrderStatus.CANCELLED

    def __eq__(self, other: object) -> bool:
        """Equality comparison by identity.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if order IDs are equal
        """
        if not isinstance(other, Order):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash based on order ID.
        
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
            f"Order(id={self._id}, customer_id={self._customer_id}, "
            f"status={self._status.value}, total={self.total})"
        )
