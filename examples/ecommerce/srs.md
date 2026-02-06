# E-Commerce Domain

## Overview
An e-commerce platform that allows customers to browse products, add them to a cart, and place orders.

## User Management

### User Registration and Authentication
- Users can register with email and password
- Users must provide a valid email address
- Passwords must meet security requirements (minimum 8 characters)
- Users can have one of the following roles: Customer, Admin, Vendor

### User Profile
- Users have profiles containing:
  - Full name (first name and last name)
  - Shipping address (street, city, state, postal code, country)
  - Billing address (can be same as shipping)
  - Phone number
- Users can update their profile information
- Users can have multiple addresses saved

## Product Catalog

### Products
- Products have the following attributes:
  - Unique product ID
  - Name (required, max 200 characters)
  - Description (optional, max 2000 characters)
  - Price (must be positive, stored as decimal with 2 decimal places)
  - Stock quantity (non-negative integer)
  - SKU (Stock Keeping Unit, unique identifier)
  - Status: Active or Inactive
- Products belong to one or more categories
- Products can have multiple images (URLs)
- Products have a creation date and last update date

### Categories
- Categories form a hierarchical structure (parent-child relationships)
- Categories have:
  - Name (required, unique within parent)
  - Description (optional)
  - Display order (for sorting)

## Shopping Cart

### Cart Management
- Each customer has one active shopping cart
- Cart contains cart items (product + quantity)
- Cart items can be added, updated, or removed
- Cart calculates subtotal (sum of item prices * quantities)
- Cart can be cleared (all items removed)
- Cart expires after 30 days of inactivity

### Cart Items
- Each cart item contains:
  - Product reference (by product ID)
  - Quantity (positive integer, minimum 1)
  - Unit price at time of addition (snapshot, may differ from current product price)
- Cart items cannot exceed product stock availability

## Orders

### Order Creation
- Orders are created from a shopping cart
- Order must contain at least one item
- Order captures:
  - Order ID (unique)
  - Customer ID
  - Order date and time
  - Shipping address (copied from user profile or custom)
  - Billing address
  - Order status: Pending, Confirmed, Shipped, Delivered, Cancelled
  - Order total (sum of all order items)
  - Shipping cost
  - Tax amount

### Order Items
- Order items are snapshots of cart items at time of order
- Each order item contains:
  - Product ID
  - Product name (snapshot)
  - Quantity
  - Unit price (snapshot)
  - Subtotal (quantity * unit price)

### Order Processing
- Orders start in "Pending" status
- Orders can be confirmed (payment received)
- Orders can be shipped (tracking number added)
- Orders can be marked as delivered
- Orders can be cancelled (only if not yet shipped)

## Business Rules

### Inventory Management
- When an order is confirmed, product stock must be decremented
- Products cannot be added to cart if stock is 0
- Cart quantities cannot exceed available stock

### Pricing
- Product prices can change, but order prices are fixed at time of order
- Cart shows current product prices, but order captures prices at checkout

### Order Validation
- Orders can only be created by authenticated customers
- Orders must have valid shipping and billing addresses
- Order total must match sum of order items plus shipping and tax
