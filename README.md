# property

A Python property management library with debugging and change tracking capabilities.

## Features

- **Property Class**: Flexible property management with getter/setter functionality
- **Debug Logging**: Built-in debugging support with timestamped logs
- **Change History**: Automatic tracking of all property value changes
- **Validation**: Support for custom validation functions
- **Property Manager**: Centralized management of multiple properties

## Installation

No external dependencies required. Simply copy `property.py` to your project.

## Usage

### Basic Property Usage

```python
from property import Property

# Create a property with debug enabled
price = Property("price", 100.0, debug=True)

# Get and set values
print(price.get())  # 100.0
price.set(150.0)
print(price.get())  # 150.0
```

### Property with Validation

```python
from property import Property

# Create a property
age = Property("age", 25, debug=True)

# Add validators
age.add_validator(lambda x: isinstance(x, int))
age.add_validator(lambda x: x >= 0)
age.add_validator(lambda x: x <= 150)

# Valid value
age.set(30)  # Works fine

# Invalid value
age.set(200)  # Raises ValueError
```

### Using PropertyManager

```python
from property import PropertyManager

# Create a manager
manager = PropertyManager(debug=True)

# Add properties
manager.add_property("name", "John Doe")
manager.add_property("age", 30)

# Get and set values
print(manager.get_value("name"))
manager.set_value("age", 31)

# List all properties
print(manager.list_properties())
```

### Change History Tracking

```python
from property import Property

status = Property("status", "pending", debug=False)

# Make changes
status.set("in_progress")
status.set("completed")

# View history
history = status.get_history()
for change in history:
    print(f"{change['old_value']} -> {change['new_value']}")
```

## Running Examples

```bash
python example.py
```

## Running Tests

```bash
python -m unittest test_property.py
```

## API Reference

### Property Class

#### `__init__(name: str, initial_value: Any = None, debug: bool = False)`
Initialize a new property.

#### `get() -> Any`
Get the current value of the property.

#### `set(value: Any)`
Set a new value for the property.

#### `add_validator(validator: Callable[[Any], bool])`
Add a validation function for the property.

#### `get_history() -> list`
Get the change history of the property.

#### `enable_debug()` / `disable_debug()`
Enable or disable debug logging.

### PropertyManager Class

#### `__init__(debug: bool = False)`
Initialize a new property manager.

#### `add_property(name: str, initial_value: Any = None) -> Property`
Add a new property to the manager.

#### `get_property(name: str) -> Optional[Property]`
Get a property by name.

#### `set_value(name: str, value: Any)`
Set the value of a property by name.

#### `get_value(name: str) -> Any`
Get the value of a property by name.

#### `list_properties() -> list`
List all property names.

#### `enable_debug_all()` / `disable_debug_all()`
Enable or disable debug mode for all properties.

## License

MIT