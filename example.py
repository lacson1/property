"""
Example usage of the Property class and PropertyManager.
"""

from property import Property, PropertyManager


def example_basic_usage():
    """Demonstrate basic property usage."""
    print("=== Basic Property Usage ===")
    
    # Create a property with debug enabled
    price = Property("price", 100.0, debug=True)
    
    # Get the value
    print(f"Initial price: ${price.get()}")
    
    # Set a new value
    price.set(150.0)
    print(f"Updated price: ${price.get()}")
    
    # View history
    print(f"Change history: {len(price.get_history())} changes")
    print()


def example_with_validation():
    """Demonstrate property validation."""
    print("=== Property with Validation ===")
    
    # Create a property with validation
    age = Property("age", 25, debug=True)
    
    # Add validators
    age.add_validator(lambda x: isinstance(x, int))
    age.add_validator(lambda x: x >= 0)
    age.add_validator(lambda x: x <= 150)
    
    # Set valid value
    age.set(30)
    print(f"Valid age set: {age.get()}")
    
    # Try to set invalid value
    try:
        age.set(200)
    except ValueError as e:
        print(f"Validation error: {e}")
    
    print()


def example_property_manager():
    """Demonstrate PropertyManager usage."""
    print("=== PropertyManager Usage ===")
    
    # Create a manager
    manager = PropertyManager(debug=True)
    
    # Add multiple properties
    manager.add_property("name", "John Doe")
    manager.add_property("age", 30)
    manager.add_property("email", "john@example.com")
    
    # List all properties
    print(f"Properties: {manager.list_properties()}")
    
    # Get and set values through manager
    print(f"Name: {manager.get_value('name')}")
    manager.set_value("age", 31)
    print(f"Updated age: {manager.get_value('age')}")
    
    # Disable debug for all
    print("\nDisabling debug for all properties...")
    manager.disable_debug_all()
    
    manager.set_value("email", "newemail@example.com")
    print(f"Updated email (no debug): {manager.get_value('email')}")
    print()


def example_history_tracking():
    """Demonstrate change history tracking."""
    print("=== History Tracking ===")
    
    status = Property("status", "pending", debug=False)
    
    # Make several changes
    status.set("in_progress")
    status.set("completed")
    status.set("archived")
    
    # View history
    history = status.get_history()
    print(f"Total changes: {len(history)}")
    for i, change in enumerate(history, 1):
        print(f"  Change {i}: {change['old_value']} -> {change['new_value']}")
    print()


if __name__ == "__main__":
    example_basic_usage()
    example_with_validation()
    example_property_manager()
    example_history_tracking()
    
    print("=== All examples completed ===")
