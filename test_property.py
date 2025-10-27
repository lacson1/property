"""
Unit tests for the Property class and PropertyManager.
"""

import unittest
from io import StringIO
import sys
from property import Property, PropertyManager


class TestProperty(unittest.TestCase):
    """Test cases for the Property class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Redirect stdout to capture debug output
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
    
    def tearDown(self):
        """Clean up after tests."""
        sys.stdout = self.original_stdout
    
    def test_init_with_initial_value(self):
        """Test property initialization with an initial value."""
        prop = Property("test_prop", 42, debug=False)
        self.assertEqual(prop.get(), 42)
    
    def test_init_without_initial_value(self):
        """Test property initialization without an initial value."""
        prop = Property("test_prop", debug=False)
        self.assertIsNone(prop.get())
    
    def test_set_and_get(self):
        """Test setting and getting property values."""
        prop = Property("test_prop", debug=False)
        prop.set(100)
        self.assertEqual(prop.get(), 100)
        
        prop.set("hello")
        self.assertEqual(prop.get(), "hello")
    
    def test_debug_logging(self):
        """Test debug logging functionality."""
        sys.stdout = self.held_output
        prop = Property("debug_prop", 10, debug=True)
        prop.set(20)
        output = self.held_output.getvalue()
        
        self.assertIn("Property 'debug_prop' initialized", output)
        self.assertIn("Value changed from 10 to 20", output)
    
    def test_history_tracking(self):
        """Test change history tracking."""
        prop = Property("history_prop", 1, debug=False)
        prop.set(2)
        prop.set(3)
        
        history = prop.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['old_value'], 1)
        self.assertEqual(history[0]['new_value'], 2)
        self.assertEqual(history[1]['old_value'], 2)
        self.assertEqual(history[1]['new_value'], 3)
    
    def test_validator(self):
        """Test property validation."""
        prop = Property("validated_prop", debug=False)
        
        # Add a validator that only allows positive numbers
        prop.add_validator(lambda x: isinstance(x, (int, float)) and x > 0)
        
        # Valid value should work
        prop.set(10)
        self.assertEqual(prop.get(), 10)
        
        # Invalid value should raise ValueError
        with self.assertRaises(ValueError):
            prop.set(-5)
    
    def test_multiple_validators(self):
        """Test multiple validators on a property."""
        prop = Property("multi_validated", debug=False)
        
        # Add validators
        prop.add_validator(lambda x: isinstance(x, int))
        prop.add_validator(lambda x: x >= 0)
        prop.add_validator(lambda x: x <= 100)
        
        # Valid value
        prop.set(50)
        self.assertEqual(prop.get(), 50)
        
        # Invalid values
        with self.assertRaises(ValueError):
            prop.set(150)  # Too large
        
        with self.assertRaises(ValueError):
            prop.set(-10)  # Negative
        
        with self.assertRaises(ValueError):
            prop.set("invalid")  # Wrong type
    
    def test_enable_disable_debug(self):
        """Test enabling and disabling debug mode."""
        sys.stdout = self.held_output
        prop = Property("toggle_debug", debug=False)
        
        # Enable debug
        prop.enable_debug()
        prop.set(10)
        output = self.held_output.getvalue()
        self.assertIn("Debug mode enabled", output)
        self.assertIn("Value changed", output)
        
        # Clear output
        self.held_output.truncate(0)
        self.held_output.seek(0)
        
        # Disable debug
        prop.disable_debug()
        prop.set(20)
        output = self.held_output.getvalue()
        self.assertIn("Debug mode disabled", output)
        # After disabling, no "Value changed" message
        self.assertEqual(output.count("Value changed"), 0)
    
    def test_str_and_repr(self):
        """Test string representations."""
        prop = Property("str_prop", 42, debug=False)
        
        str_repr = str(prop)
        self.assertIn("str_prop", str_repr)
        self.assertIn("42", str_repr)
        
        repr_str = repr(prop)
        self.assertIn("str_prop", repr_str)
        self.assertIn("42", repr_str)
        self.assertIn("debug=False", repr_str)
    
    def test_is_debug_enabled(self):
        """Test checking debug status."""
        prop = Property("test_prop", debug=False)
        self.assertFalse(prop.is_debug_enabled())
        
        prop.enable_debug()
        self.assertTrue(prop.is_debug_enabled())
        
        prop.disable_debug()
        self.assertFalse(prop.is_debug_enabled())


class TestPropertyManager(unittest.TestCase):
    """Test cases for the PropertyManager class."""
    
    def test_add_property(self):
        """Test adding properties to the manager."""
        manager = PropertyManager(debug=False)
        prop = manager.add_property("prop1", 100)
        
        self.assertIsInstance(prop, Property)
        self.assertEqual(prop.get(), 100)
    
    def test_get_property(self):
        """Test retrieving properties from the manager."""
        manager = PropertyManager(debug=False)
        manager.add_property("prop1", 42)
        
        prop = manager.get_property("prop1")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.get(), 42)
        
        # Non-existent property
        prop = manager.get_property("nonexistent")
        self.assertIsNone(prop)
    
    def test_set_and_get_value(self):
        """Test setting and getting values through the manager."""
        manager = PropertyManager(debug=False)
        manager.add_property("prop1", 0)
        
        manager.set_value("prop1", 99)
        self.assertEqual(manager.get_value("prop1"), 99)
    
    def test_set_value_nonexistent(self):
        """Test setting value for nonexistent property."""
        manager = PropertyManager(debug=False)
        
        with self.assertRaises(KeyError):
            manager.set_value("nonexistent", 123)
    
    def test_get_value_nonexistent(self):
        """Test getting value for nonexistent property."""
        manager = PropertyManager(debug=False)
        
        with self.assertRaises(KeyError):
            manager.get_value("nonexistent")
    
    def test_list_properties(self):
        """Test listing all properties."""
        manager = PropertyManager(debug=False)
        manager.add_property("prop1")
        manager.add_property("prop2")
        manager.add_property("prop3")
        
        props = manager.list_properties()
        self.assertEqual(len(props), 3)
        self.assertIn("prop1", props)
        self.assertIn("prop2", props)
        self.assertIn("prop3", props)
    
    def test_debug_inheritance(self):
        """Test that debug setting is inherited by properties."""
        manager = PropertyManager(debug=True)
        prop = manager.add_property("debug_prop", 10)
        
        # The property should have debug enabled
        self.assertTrue(prop.is_debug_enabled())
    
    def test_enable_disable_debug_all(self):
        """Test enabling/disabling debug for all properties."""
        manager = PropertyManager(debug=False)
        prop1 = manager.add_property("prop1")
        prop2 = manager.add_property("prop2")
        
        # Enable debug for all
        manager.enable_debug_all()
        self.assertTrue(prop1.is_debug_enabled())
        self.assertTrue(prop2.is_debug_enabled())
        
        # Disable debug for all
        manager.disable_debug_all()
        self.assertFalse(prop1.is_debug_enabled())
        self.assertFalse(prop2.is_debug_enabled())


if __name__ == '__main__':
    unittest.main()
