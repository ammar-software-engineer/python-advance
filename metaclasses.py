"""
metaclasses.py - Advanced Metaclasses in Python

This file delves into the advanced topic of metaclasses in Python.
A metaclass is the class of a class. Just as an ordinary class defines the behavior
of its instances, a metaclass defines the behavior of classes themselves.
In Python, `type` is the default metaclass for all classes.

Understanding metaclasses is crucial for advanced framework development,
API design, and understanding how Python objects are constructed at a deeper level.
"""

# --- 1. What is a Metaclass? ---
# In Python, everything is an object. Classes are objects too.
# The type of a class object is its metaclass.
# print(type(int))    # <class 'type'>
# print(type(list))   # <class 'type'>
# print(type(type))   # <class 'type'> - `type` is its own metaclass!

# When you define a class:
class MyClass:
    pass
# print(type(MyClass)) # <class 'type'>

# So, `type` is the default metaclass.
# We can create classes dynamically using `type()` function:
# type(name, bases, dict) -> class
# name: name of the class
# bases: tuple of base classes (for inheritance)
# dict: dictionary of class attributes and methods

# Example: Dynamically creating a class equivalent to `class MyClass: x = 10`
DynamicClass = type('DynamicClass', (), {'x': 10})
# print(DynamicClass.x) # Output: 10
# dynamic_instance = DynamicClass()
# print(dynamic_instance.x) # Output: 10

# --- 2. Custom Metaclass Creation ---
# To create a custom metaclass, you typically subclass `type`.
# The `__new__` method of the metaclass is responsible for creating the class object.
# The `__init__` method of the metaclass is responsible for initializing the class object.

class CustomMetaclass(type):
    """
    A custom metaclass that adds a specific attribute to all classes it creates.
    It also prints messages during class creation.
    """
    def __new__(mcs, name, bases, dct):
        # mcs: The metaclass itself (CustomMetaclass)
        # name: The name of the class being created (e.g., 'MySpecialClass')
        # bases: A tuple of base classes (e.g., (object,))
        # dct: A dictionary of attributes and methods of the class being created
        print(f"CustomMetaclass __new__ called for class: {name}")
        dct['added_by_metaclass'] = "This attribute was added by CustomMetaclass!"
        # Call the original type.__new__ to actually create the class object
        return super().__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        # cls: The newly created class object (e.g., MySpecialClass)
        print(f"CustomMetaclass __init__ called for class: {name}")
        super().__init__(cls, name, bases, dct)

# To use a metaclass, specify it with the `metaclass` argument in the class definition.
class MySpecialClass(metaclass=CustomMetaclass):
    """
    A class that uses CustomMetaclass.
    """
    def __init__(self, value):
        self.value = value

    def display(self):
        print(f"Value: {self.value}, Metaclass added: {self.added_by_metaclass}")

# my_instance = MySpecialClass(100)
# my_instance.display()
# print(MySpecialClass.added_by_metaclass)
# Expected output:
# CustomMetaclass __new__ called for class: MySpecialClass
# CustomMetaclass __init__ called for class: MySpecialClass
# Value: 100, Metaclass added: This attribute was added by CustomMetaclass!
# This attribute was added by CustomMetaclass!

# --- 3. Use Cases for Metaclasses ---

# A. Automatic Registration of Classes:
# A common pattern is to automatically register classes into a central registry
# when they are defined.
class PluginManager(type):
    """
    Metaclass to automatically register subclasses into a registry.
    """
    registry = {}

    def __new__(mcs, name, bases, dct):
        new_class = super().__new__(mcs, name, bases, dct)
        if name != 'BasePlugin': # Avoid registering the base class itself
            mcs.registry[name] = new_class
        return new_class

class BasePlugin(metaclass=PluginManager):
    """Base class for plugins."""
    pass

class MyPlugin1(BasePlugin):
    def run(self):
        return "MyPlugin1 is running."

class MyPlugin2(BasePlugin):
    def run(self):
        return "MyPlugin2 is executing."

# print(PluginManager.registry)
# {
#   'MyPlugin1': <class '__main__.MyPlugin1'>,
#   'MyPlugin2': <class '__main__.MyPlugin2'>
# }

# plugin1 = PluginManager.registry['MyPlugin1']()
# print(plugin1.run()) # Output: MyPlugin1 is running.

# B. Enforcing Interface/Abstract Methods:
# Similar to `abc.ABCMeta`, but can be custom-tailored.
# This example is simplified; `abc` module is generally preferred for this.
class InterfaceEnforcer(type):
    """
    Metaclass that ensures subclasses implement a specific method.
    """
    def __init__(cls, name, bases, dct):
        super().__init__(cls, name, bases, dct)
        if 'my_interface_method' not in dct:
            # Check if method is inherited from a non-Abstract Base Class
            # For simplicity, we only check the immediate class dictionary
            # A more robust check would involve iterating through bases
            if not any('my_interface_method' in b.__dict__ for b in bases):
                 raise TypeError(f"Class {name} must implement 'my_interface_method'")

# Uncommenting the following will raise a TypeError:
# class RequiresInterface(metaclass=InterfaceEnforcer):
#     pass

# class ImplementsInterface(metaclass=InterfaceEnforcer):
#     def my_interface_method(self):
#         return "Implemented!"

# print(ImplementsInterface().my_interface_method())

# C. Modifying Class Attributes or Methods at Definition Time:
# Metaclasses can inspect and modify the `dct` (dictionary of class attributes)
# before the class is fully created.

class AttributeModifier(type):
    """
    Metaclass to automatically add a prefix to all method names.
    (This is a complex example and might not be practical in all scenarios.)
    """
    def __new__(mcs, name, bases, dct):
        new_dct = {}
        for key, value in dct.items():
            if callable(value) and not key.startswith('__'): # Only modify user-defined methods
                new_dct[f"prefixed_{key}"] = value
            else:
                new_dct[key] = value
        return super().__new__(mcs, name, bases, new_dct)

# class MyClassWithPrefixedMethods(metaclass=AttributeModifier):
#     def original_method(self):
#         return "This is the original method."

#     def another_method(self):
#         return "This is another method."

# instance = MyClassWithPrefixedMethods()
# # print(instance.prefixed_original_method()) # Output: This is the original method.
# # print(instance.prefixed_another_method())  # Output: This is another method.
# # try:
# #     instance.original_method() # This will raise an AttributeError
# # except AttributeError as e:
# #     print(f"Error: {e}")

# Conclusion:
# Metaclasses are a highly advanced feature in Python, allowing for deep control
# over class creation. They are typically used in frameworks or libraries
# to enforce conventions, register components, or perform complex transformations
# on classes during their definition. For most day-to-day programming,
# decorators or simpler class inheritance patterns are sufficient.
