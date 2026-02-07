"""
decorators.py - Advanced Decorators in Python

This file demonstrates various advanced concepts and uses of decorators in Python.
Decorators are a powerful feature that allows you to modify or enhance a function or method
without changing its source code. They are essentially functions that take another function
as an argument, add some functionality, and return the modified function.
"""

import time
import functools

# --- 1. Simple Decorator ---
# A basic decorator that logs function calls.
def log_function_call(func):
    """
    A simple decorator that prints a message before and after a function call.
    """
    @functools.wraps(func)  # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        print(f"--- Calling function: {func.__name__} ---")
        result = func(*args, **kwargs)
        print(f"--- Finished function: {func.__name__} ---")
        return result
    return wrapper

@log_function_call
def greet(name):
    """A simple function to greet someone."""
    return f"Hello, {name}!"

# print(greet("Alice"))
# Expected output:
# --- Calling function: greet ---
# --- Finished function: greet ---
# Hello, Alice!

# --- 2. Decorator with Arguments ---
# Decorators can also accept arguments, which requires an extra nested function.
def repeat(num_times):
    """
    A decorator that repeats the decorated function's execution N times.
    """
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                print(f"Repeating {func.__name__}...")
                func(*args, **kwargs)
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def say_hello():
    """A function that simply prints 'Hello!'"""
    print("Hello!")

# say_hello()
# Expected output:
# Repeating say_hello...
# Hello!
# Repeating say_hello...
# Hello!
# Repeating say_hello...
# Hello!

# --- 3. Class-Based Decorators ---
# Decorators can also be implemented as classes, especially useful when you need
# to maintain state. A class-based decorator needs to implement __init__ and __call__.
class TimerDecorator:
    """
    A class-based decorator that measures the execution time of a function.
    """
    def __init__(self, func):
        functools.update_wrapper(self, func) # Copy func's metadata to the instance
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {self.func.__name__} executed in {end_time - start_time:.4f} seconds.")
        print(f"Call count for {self.func.__name__}: {self.call_count}")
        return result

@TimerDecorator
def long_running_task(duration):
    """Simulates a task that takes a certain duration."""
    time.sleep(duration)
    return f"Task completed in {duration} seconds."

# print(long_running_task(0.5))
# print(long_running_task(0.2))
# Expected output:
# Function long_running_task executed in X.XXXX seconds.
# Call count for long_running_task: 1
# Task completed in 0.5 seconds.
# Function long_running_task executed in Y.YYYY seconds.
# Call count for long_running_task: 2
# Task completed in 0.2 seconds.

# --- 4. Stacking Decorators ---
# You can apply multiple decorators to a single function.
# Decorators are applied from bottom to top (closest to the function first).
@log_function_call
@TimerDecorator # This decorator is applied first (to the 'power' function)
def power(base, exp):
    """Calculates base raised to the power of exp."""
    print(f"Calculating {base} raised to {exp}...")
    time.sleep(0.1) # Simulate some work
    return base ** exp

# print(power(2, 3))
# Expected output:
# --- Calling function: power ---
# Calculating 2 raised to 3...
# Function power executed in X.XXXX seconds.
# Call count for power: 1
# --- Finished function: power ---
# 8

# --- 5. Decorators for Type Checking/Validation (Advanced Use Case) ---
def enforce_types(**types):
    """
    A decorator that enforces type hints for function arguments.
    Raises TypeError if arguments do not match the specified types.
    """
    def decorator_enforce_types(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Bind arguments to parameter names for type checking
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            for name, value in bound_args.arguments.items():
                if name in types and not isinstance(value, types[name]):
                    raise TypeError(f"Argument '{name}' must be of type {types[name].__name__}, "
                                    f"but got {type(value).__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator_enforce_types

import inspect

@enforce_types(a=int, b=int)
def add_numbers(a, b):
    """Adds two numbers, enforcing integer types."""
    return a + b

# print(add_numbers(10, 20)) # Works fine
# try:
#     print(add_numbers(10, "20")) # Raises TypeError
# except TypeError as e:
#     print(f"Error: {e}")

# Conclusion:
# Decorators are a powerful and elegant way to extend or modify the behavior
# of functions and methods. They promote code reusability and separation of concerns.
