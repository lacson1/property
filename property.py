"""
Property class with debugging and change tracking capabilities.
"""

from typing import Any, Optional, Callable
from datetime import datetime


class Property:
    """
    A property class that provides getter/setter functionality with debugging support.
    Tracks property changes and provides logging capabilities.
    """
    
    def __init__(self, name: str, initial_value: Any = None, debug: bool = False):
        """
        Initialize a Property instance.
        
        Args:
            name: The name of the property
            initial_value: The initial value of the property
            debug: Whether to enable debug logging
        """
        self._name = name
        self._value = initial_value
        self._debug = debug
        self._history = []
        self._validators = []
        
        if self._debug:
            self._log(f"Property '{self._name}' initialized with value: {self._value}")
    
    def _log(self, message: str):
        """Log a debug message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [Property:{self._name}] {message}")
    
    def get(self) -> Any:
        """
        Get the current value of the property.
        
        Returns:
            The current property value
        """
        if self._debug:
            self._log(f"Getting value: {self._value}")
        return self._value
    
    def set(self, value: Any):
        """
        Set a new value for the property.
        
        Args:
            value: The new value to set
        
        Raises:
            ValueError: If validation fails
        """
        # Run validators
        for validator in self._validators:
            if not validator(value):
                raise ValueError(f"Validation failed for value: {value}")
        
        old_value = self._value
        self._value = value
        
        # Track history
        self._history.append({
            'timestamp': datetime.now(),
            'old_value': old_value,
            'new_value': value
        })
        
        if self._debug:
            self._log(f"Value changed from {old_value} to {value}")
    
    def add_validator(self, validator: Callable[[Any], bool]):
        """
        Add a validation function for the property.
        
        Args:
            validator: A function that takes a value and returns True if valid
        """
        self._validators.append(validator)
        if self._debug:
            self._log(f"Validator added")
    
    def get_history(self) -> list:
        """
        Get the change history of the property.
        
        Returns:
            A list of change records
        """
        if self._debug:
            self._log(f"Getting history ({len(self._history)} entries)")
        return self._history.copy()
    
    def enable_debug(self):
        """Enable debug logging."""
        self._debug = True
        self._log("Debug mode enabled")
    
    def disable_debug(self):
        """Disable debug logging."""
        self._log("Debug mode disabled")
        self._debug = False
    
    def __str__(self) -> str:
        """String representation of the property."""
        return f"Property(name='{self._name}', value={self._value})"
    
    def __repr__(self) -> str:
        """Detailed representation of the property."""
        return f"Property(name='{self._name}', value={self._value}, debug={self._debug})"


class PropertyManager:
    """
    Manages multiple properties with debugging capabilities.
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize a PropertyManager instance.
        
        Args:
            debug: Whether to enable debug logging for all properties
        """
        self._properties = {}
        self._debug = debug
    
    def add_property(self, name: str, initial_value: Any = None) -> Property:
        """
        Add a new property to the manager.
        
        Args:
            name: The name of the property
            initial_value: The initial value
        
        Returns:
            The created Property instance
        """
        prop = Property(name, initial_value, debug=self._debug)
        self._properties[name] = prop
        return prop
    
    def get_property(self, name: str) -> Optional[Property]:
        """
        Get a property by name.
        
        Args:
            name: The name of the property
        
        Returns:
            The Property instance or None if not found
        """
        return self._properties.get(name)
    
    def set_value(self, name: str, value: Any):
        """
        Set the value of a property by name.
        
        Args:
            name: The name of the property
            value: The new value
        
        Raises:
            KeyError: If property doesn't exist
        """
        if name not in self._properties:
            raise KeyError(f"Property '{name}' not found")
        self._properties[name].set(value)
    
    def get_value(self, name: str) -> Any:
        """
        Get the value of a property by name.
        
        Args:
            name: The name of the property
        
        Returns:
            The property value
        
        Raises:
            KeyError: If property doesn't exist
        """
        if name not in self._properties:
            raise KeyError(f"Property '{name}' not found")
        return self._properties[name].get()
    
    def list_properties(self) -> list:
        """
        List all property names.
        
        Returns:
            A list of property names
        """
        return list(self._properties.keys())
    
    def enable_debug_all(self):
        """Enable debug mode for all properties."""
        self._debug = True
        for prop in self._properties.values():
            prop.enable_debug()
    
    def disable_debug_all(self):
        """Disable debug mode for all properties."""
        self._debug = False
        for prop in self._properties.values():
            prop.disable_debug()
