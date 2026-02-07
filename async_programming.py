"""
async_programming.py - Advanced Asynchronous Programming in Python

This file covers advanced concepts in asynchronous programming using Python's `asyncio` library.
Asynchronous programming allows for concurrent execution of operations without using threads,
making it efficient for I/O-bound tasks (like network requests, file operations, database queries).

Key concepts:
- `async`/`await` syntax
- Coroutines
- Event Loop
- Tasks
- Futures
"""

import asyncio
import time

# --- 1. Basic Coroutine with `async` and `await` ---
# A coroutine is a function defined with `async def`.
# It can pause its execution with `await` and resume later.
async def greet_async(name, delay):
    """
    A simple asynchronous function that waits for a delay and then greets.
    """
    print(f"Start greeting {name}...")
    await asyncio.sleep(delay) # `await` is used to pause execution until a Future or coroutine is done
    print(f"Hello, {name} after {delay} seconds!")
    return f"Greeting for {name} completed."

async def main_basic_coroutine():
    """Main function to run basic coroutines."""
    print("Main basic coroutine started.")
    # Run a single coroutine
    # result = await greet_async("Alice", 1)
    # print(result)

    # Run multiple coroutines concurrently using `asyncio.gather`
    # This will run `greet_async("Bob", 2)` and `greet_async("Charlie", 1)`
    # concurrently, not sequentially.
    results = await asyncio.gather(
        greet_async("Bob", 2),
        greet_async("Charlie", 1)
    )
    print(f"All greetings done: {results}")
    print("Main basic coroutine finished.")

# To run an async function, you need an event loop.
# asyncio.run(main_basic_coroutine())
# Expected output (order might vary slightly due to concurrency):
# Main basic coroutine started.
# Start greeting Bob...
# Start greeting Charlie...
# Hello, Charlie after 1 seconds!
# Hello, Bob after 2 seconds!
# All greetings done: ['Greeting for Bob completed.', 'Greeting for Charlie completed.']
# Main basic coroutine finished.

# --- 2. Tasks and the Event Loop ---
# Coroutines don't run by themselves; they must be scheduled on an event loop.
# `asyncio.create_task()` schedules a coroutine as a `Task`.
# A `Task` is a Future-like object that wraps a coroutine.

async def worker(name, delay):
    """A worker coroutine that performs some simulated work."""
    print(f"Worker {name}: Starting work...")
    await asyncio.sleep(delay)
    print(f"Worker {name}: Finished work after {delay} seconds.")
    return f"Worker {name} result"

async def main_tasks():
    """Main function to demonstrate asyncio Tasks."""
    print("Main tasks started.")

    # Create tasks (schedule coroutines to run)
    task1 = asyncio.create_task(worker("A", 3))
    task2 = asyncio.create_task(worker("B", 1))
    task3 = asyncio.create_task(worker("C", 2))

    # Await the tasks. `await` here means "wait for this task to complete".
    # Since tasks are already scheduled, they run concurrently.
    results = await asyncio.gather(task1, task2, task3)

    print(f"All workers finished: {results}")
    print("Main tasks finished.")

# asyncio.run(main_tasks())
# Expected output (order might vary, but all start roughly at the same time and finish based on delay):
# Main tasks started.
# Worker A: Starting work...
# Worker B: Starting work...
# Worker C: Starting work...
# Worker B: Finished work after 1 seconds.
# Worker C: Finished work after 2 seconds.
# Worker A: Finished work after 3 seconds.
# All workers finished: ['Worker A result', 'Worker B result', 'Worker C result']
# Main tasks finished.

# --- 3. `asyncio.wait()` vs `asyncio.gather()` ---
# `asyncio.gather()`: runs coroutines/tasks concurrently and aggregates their results.
# `asyncio.wait()`: waits for a collection of Futures/Tasks to complete,
#                   but does not return their results directly. It returns two sets:
#                   (done, pending).

async def fetch_data(url, delay):
    """Simulates fetching data from a URL with a delay."""
    print(f"Fetching {url}...")
    await asyncio.sleep(delay)
    print(f"Finished fetching {url}.")
    return f"Data from {url}"

async def main_wait_vs_gather():
    """Demonstrates asyncio.wait() and asyncio.gather()."""
    print("Main wait_vs_gather started.")

    tasks = [
        asyncio.create_task(fetch_data("google.com", 2)),
        asyncio.create_task(fetch_data("bing.com", 1)),
        asyncio.create_task(fetch_data("yahoo.com", 3)),
    ]

    # Using asyncio.gather (collects results)
    # results_gather = await asyncio.gather(*tasks)
    # print(f"Gather results: {results_gather}")

    # Using asyncio.wait (returns done/pending tasks)
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"
First completed task(s):")
    for task in done:
        print(f"  Result: {await task}") # You still need to await individual tasks to get results

    # If return_when=asyncio.ALL_COMPLETED (default), then pending will be empty.
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    # print(f"
All completed tasks:")
    # for task in done:
    #     print(f"  Result: {await task}")

    print("Main wait_vs_gather finished.")

# asyncio.run(main_wait_vs_gather())
# Expected output for FIRST_COMPLETED:
# Main wait_vs_gather started.
# Fetching google.com...
# Fetching bing.com...
# Fetching yahoo.com...
# Finished fetching bing.com.
# First completed task(s):
#   Result: Data from bing.com
# Finished fetching google.com.
# Finished fetching yahoo.com.
# Main wait_vs_gather finished.

# --- 4. Asynchronous Context Managers (`async with`) ---
# Similar to regular context managers (`with`), but for asynchronous operations.
# They require `__aenter__` and `__aexit__` methods.
class AsyncResource:
    """An asynchronous context manager."""
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print(f"Entering async resource: {self.name}")
        await asyncio.sleep(0.1) # Simulate async setup
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting async resource: {self.name}")
        await asyncio.sleep(0.1) # Simulate async teardown
        if exc_type:
            print(f"An exception {exc_type.__name__} occurred: {exc_val}")

    async def use_resource(self):
        print(f"Using resource: {self.name}")
        await asyncio.sleep(0.2)
        return "Resource used successfully"

async def main_async_context_manager():
    """Demonstrates asynchronous context managers."""
    print("Main async context manager started.")
    async with AsyncResource("DB_Connection") as db:
        result = await db.use_resource()
        print(result)
    print("Main async context manager finished.")

# asyncio.run(main_async_context_manager())
# Expected output:
# Main async context manager started.
# Entering async resource: DB_Connection
# Using resource: DB_Connection
# Resource used successfully
# Exiting async resource: DB_Connection
# Main async context manager finished.

# --- 5. Running CPU-bound tasks in `asyncio` (`run_in_executor`) ---
# `asyncio` is best for I/O-bound tasks. For CPU-bound tasks, it's better to
# offload them to a separate thread or process pool using `loop.run_in_executor()`.
# This prevents blocking the event loop.

def cpu_intensive_task(num):
    """A blocking, CPU-intensive function."""
    print(f"  CPU task {num}: Starting...")
    time.sleep(1) # Simulate heavy computation (blocking)
    result = sum(i*i for i in range(10**6)) # Actual CPU work
    print(f"  CPU task {num}: Finished.")
    return result

async def main_cpu_bound():
    """Demonstrates running CPU-bound tasks with run_in_executor."""
    print("Main CPU-bound started.")
    loop = asyncio.get_running_loop()

    # Run CPU-bound tasks in the default ThreadPoolExecutor
    # This offloads the blocking work to a separate thread.
    task1 = loop.run_in_executor(None, cpu_intensive_task, 1)
    task2 = loop.run_in_executor(None, cpu_intensive_task, 2)

    # We can still run I/O-bound tasks concurrently with CPU-bound tasks
    io_task = asyncio.create_task(greet_async("Developer", 0.5))

    results_cpu = await asyncio.gather(task1, task2)
    result_io = await io_task

    print(f"CPU results: {results_cpu}")
    print(f"I/O result: {result_io}")
    print("Main CPU-bound finished.")

# asyncio.run(main_cpu_bound())
# Expected output (CPU tasks will appear to run concurrently with I/O task):
# Main CPU-bound started.
#   CPU task 1: Starting...
#   CPU task 2: Starting...
# Start greeting Developer...
# Hello, Developer after 0.5 seconds!
#   CPU task 1: Finished.
#   CPU task 2: Finished.
# CPU results: [some_large_number, some_large_number]
# I/O result: Greeting for Developer completed.
# Main CPU-bound finished.

# Conclusion:
# Asynchronous programming with `asyncio` is powerful for building highly concurrent
# and scalable applications, especially for I/O-bound workloads.
# Understanding coroutines, tasks, the event loop, and how to offload CPU-bound work
# is essential for effective use of this paradigm.
