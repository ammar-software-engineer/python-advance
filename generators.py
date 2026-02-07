"""
generators.py - Advanced Generators in Python

This file explores advanced aspects of Python generators, including generator functions,
generator expressions, and their use cases for memory-efficient iteration.
Generators are iterators, but unlike normal iterators, they don't store all their
values in memory. They generate values on the fly, one at a time, making them ideal
for handling large datasets or infinite sequences.
"""

# --- 1. Basic Generator Function ---
# A generator function uses the `yield` keyword instead of `return` to produce a sequence of values.
# When `yield` is encountered, the function's state is saved, and it can be resumed later.
def simple_generator():
    """A simple generator that yields numbers from 1 to 3."""
    print("Starting simple_generator")
    yield 1
    print("Yielded 1")
    yield 2
    print("Yielded 2")
    yield 3
    print("Yielded 3")
    print("Finishing simple_generator")

# Using the generator:
# gen = simple_generator()
# print(next(gen)) # Output: Starting simple_generator, Yielded 1, 1
# print(next(gen)) # Output: Yielded 2, 2
# print(next(gen)) # Output: Yielded 3, 3
# try:
#     print(next(gen)) # Output: Finishing simple_generator, raises StopIteration
# except StopIteration:
#     print("Generator exhausted.")

# Iterating with a for loop (handles StopIteration automatically):
# for value in simple_generator():
#     print(f"Received: {value}")

# --- 2. Generator Expressions ---
# Similar to list comprehensions, but they create generators instead of lists.
# They are more memory-efficient than list comprehensions for large sequences
# because they don't construct the entire sequence in memory.
my_list = [1, 2, 3, 4, 5]

# List comprehension (creates a list in memory)
list_comprehension_squares = [x*x for x in my_list]
# print(f"List comprehension squares: {list_comprehension_squares}")

# Generator expression (creates a generator object)
generator_expression_squares = (x*x for x in my_list)
# print(f"Generator expression object: {generator_expression_squares}")
# print(f"First square from generator expression: {next(generator_expression_squares)}")
# print(f"Remaining squares from generator expression: {list(generator_expression_squares)}")

# Generator expressions are often used directly within functions that accept iterables:
# print(f"Sum of squares (generator expression): {sum(x*x for x in range(10))}")

# --- 3. Infinite Generators ---
# Generators can be used to create infinite sequences, which is impossible with lists.
def fibonacci_generator():
    """Generates an infinite sequence of Fibonacci numbers."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# fib_gen = fibonacci_generator()
# for _ in range(10):
#     print(next(fib_gen))
# Expected output (first 10 Fibonacci numbers):
# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

# --- 4. Chaining Generators (Delegating with `yield from`) ---
# `yield from` is used to delegate iteration to a sub-generator or any iterable.
# It simplifies generator composition and error handling.
def generator_a():
    yield "A1"
    yield "A2"

def generator_b():
    yield "B1"
    yield "B2"

def chained_generator():
    yield from generator_a()
    yield from generator_b()
    yield "C1"

# for item in chained_generator():
#     print(item)
# Expected output: A1, A2, B1, B2, C1

# --- 5. Generators for File Processing (Memory Efficiency) ---
# Reading large files line by line using a generator prevents loading the entire file into memory.
def read_large_file_generator(filepath):
    """
    A generator to read a large file line by line, yielding each line.
    """
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip() # .strip() to remove newline characters

# To demonstrate, let's create a dummy large file:
# with open("large_data.txt", "w") as f:
#     for i in range(100000):
#         f.write(f"This is line {i}\n")

# Process the file using the generator:
# count = 0
# for line in read_large_file_generator("large_data.txt"):
#     # print(line) # Process each line
#     count += 1
#     if count >= 5: # Just process first 5 lines for example
#         break
# print(f"Processed {count} lines.")
# (Remember to delete large_data.txt if created for testing)

# --- 6. Sending Values into Generators (`send()` method) ---
# Generators can not only yield values but also receive values using the `send()` method.
# This makes them more powerful for co-routine-like behavior.
def echo_and_process():
    """
    A generator that echoes received values and performs a simple calculation.
    """
    value = None
    while True:
        received = yield value # Yields 'value' and waits for 'send()' to provide 'received'
        if received is None:
            print("Generator received None, stopping.")
            break
        value = f"Processed: {received * 2}"
        print(f"Generator received: {received}, yielding: {value}")

# gen_echo = echo_and_process()
# next(gen_echo) # Start the generator, runs until the first yield
# print(gen_echo.send(10)) # Send 10, receive "Processed: 20"
# print(gen_echo.send(5))  # Send 5, receive "Processed: 10"
# try:
#     gen_echo.send(None) # Send None to stop the generator
# except StopIteration:
#     print("Generator stopped by StopIteration.")
# Expected output:
# Generator received: 10, yielding: Processed: 20
# Processed: 20
# Generator received: 5, yielding: Processed: 10
# Processed: 10
# Generator received None, stopping.
# Generator stopped by StopIteration.

# Conclusion:
# Generators are a cornerstone of memory-efficient and elegant Python programming,
# especially when dealing with large data streams or infinite sequences.
# They are essential for understanding asynchronous programming patterns as well.
