# SmartGen Examples

This document provides examples and use cases for SmartGen, showing how to generate DDD-compliant domain code from requirements.

## Quick Start Examples

### Example 1: Simple User Domain

**SRS (`srs.md`):**
```markdown
# User Management Domain

## User Registration
- Users register with email and password
- Email must be valid format
- Password must be at least 8 characters

## User Profile
- Users have first name and last name
- Users can update their profile
```

**Generated Code:**
- `src/domain/value_objects/email.py` - Email validation
- `src/domain/entities/user.py` - User entity with profile management

**Command:**
```bash
smartgen generate domain
```

### Example 2: Product Catalog

**SRS (`srs.md`):**
```markdown
# Product Catalog Domain

## Products
- Products have name, description, and price
- Products have stock quantity
- Products can be active or inactive
- Price must be positive
```

**Generated Code:**
- `src/domain/value_objects/money.py` - Money value object
- `src/domain/entities/product.py` - Product entity with stock management

**Command:**
```bash
smartgen generate domain
```

## Complete Examples

### E-Commerce Domain

A full-featured e-commerce domain demonstrating:
- User management with roles
- Product catalog with categories
- Shopping cart functionality
- Order processing

**Location**: [`examples/ecommerce/`](examples/ecommerce/)

**Features:**
- Multiple value objects (Email, Money, Address)
- Entities (User, Product)
- Aggregate (Order with OrderItems)
- Business rule enforcement

**See**: [`examples/ecommerce/readme.md`](examples/ecommerce/readme.md) for full documentation

## Real-World Use Cases

### Use Case 1: Starting a New Project

**Scenario**: You're starting a new microservice and need to establish the domain layer quickly.

**Steps:**
1. Write your domain requirements in `srs.md`
2. Run `smartgen init` to set up the project
3. Run `smartgen generate domain` to generate domain code
4. Review and refine the generated code
5. Generate application layout with `smartgen generate layout`

**Benefits:**
- Saves hours of manual scaffolding
- Ensures DDD compliance from the start
- Provides learning examples for your team

### Use Case 2: Learning DDD

**Scenario**: You're learning Domain-Driven Design and want to see how patterns are applied.

**Steps:**
1. Review example SRS files
2. Generate domain code
3. Study the generated code structure
4. Compare with DDD principles
5. Experiment with different requirements

**Benefits:**
- See DDD patterns in practice
- Understand value objects vs entities
- Learn aggregate design
- See invariant enforcement

### Use Case 3: Team Onboarding

**Scenario**: New team members need to understand your domain architecture.

**Steps:**
1. Show them example domains
2. Explain the SRS format
3. Demonstrate code generation
4. Review generated code together
5. Let them generate their own examples

**Benefits:**
- Consistent understanding of DDD patterns
- Faster onboarding
- Clear examples to reference

## Example Patterns

### Value Object Pattern

**When to use**: Attributes that have no identity and are defined by their values.

**Example**: Email, Money, Address

```python
# Generated value object
class Email:
    def __init__(self, value: str):
        # Validation logic
        ...
    
    def __eq__(self, other):
        # Equality by value
        ...
```

### Entity Pattern

**When to use**: Objects with identity that change over time.

**Example**: User, Product

```python
# Generated entity
class User:
    def __init__(self, user_id: UserId, email: Email, ...):
        # Identity and initial state
        ...
    
    def update_profile(self, ...):
        # State-changing methods
        ...
```

### Aggregate Pattern

**When to use**: Clusters of entities and value objects with consistency boundaries.

**Example**: Order with OrderItems

```python
# Generated aggregate root
class Order:
    def __init__(self, order_id: OrderId, items: list[OrderItem], ...):
        # Enforce invariants
        ...
    
    def confirm(self):
        # State transitions
        ...
```

## Tips for Writing Good SRS

1. **Be Specific**: Clearly define entities, attributes, and relationships
2. **Include Business Rules**: State validation rules and constraints
3. **Describe Behavior**: Explain what entities can do, not just what they are
4. **Use Domain Language**: Use terms from your business domain
5. **Separate Concerns**: Focus on domain logic, not infrastructure

## Common Patterns in Generated Code

### Validation in Value Objects

All value objects validate their data on creation:

```python
class Email:
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError("Invalid email")
        self._value = value
```

### Invariant Enforcement in Aggregates

Aggregates enforce business rules:

```python
class Order:
    def __init__(self, items: list[OrderItem]):
        if not items:
            raise ValueError("Order must have items")
        self._items = items
```

### Identity-Based Equality

Entities compare by identity:

```python
class User:
    def __eq__(self, other):
        return self._id == other._id
```

## Next Steps

1. **Try Examples**: Run through the examples in this directory
2. **Create Your Own**: Write an SRS for your domain
3. **Generate Code**: Use SmartGen to generate domain code
4. **Review and Refine**: Review generated code and make adjustments
5. **Generate Layout**: Create application structure with `smartgen generate layout`

## Resources

- [Examples Directory](examples/) - Complete example projects
- [Main readme](readme.md) - SmartGen documentation
- [Contributing Guide](contributing.md) - How to contribute examples
