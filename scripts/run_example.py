#!/usr/bin/env python3
"""Run a specific example in Deephaven."""

import argparse
import os
import sys
import glob


def list_examples(examples_dir: str) -> list[str]:
    """List all available examples.

    Args:
        examples_dir: Path to the examples directory.

    Returns:
        List of example names.
    """
    examples = []
    if os.path.isdir(examples_dir):
        for item in os.listdir(examples_dir):
            item_path = os.path.join(examples_dir, item)
            if os.path.isdir(item_path) and not item.startswith("."):
                # Check if it has Python files
                py_files = glob.glob(os.path.join(item_path, "*.py"))
                if py_files:
                    examples.append(item)
    return sorted(examples)


def find_main_file(example_dir: str) -> str | None:
    """Find the main Python file for an example.

    Args:
        example_dir: Path to the example directory.

    Returns:
        Path to the main Python file, or None if not found.
    """
    # Look for common main file patterns
    patterns = [
        "main.py",
        "app.py",
        "__init__.py",
    ]

    for pattern in patterns:
        main_file = os.path.join(example_dir, pattern)
        if os.path.isfile(main_file):
            return main_file

    # Fall back to the first .py file that's not a test
    py_files = glob.glob(os.path.join(example_dir, "*.py"))
    for py_file in sorted(py_files):
        basename = os.path.basename(py_file)
        if not basename.startswith("test_") and basename != "conftest.py":
            return py_file

    return None


def run_example(
    example_name: str, port: int = 10000, examples_dir: str | None = None
) -> None:
    """Run a specific example.

    Args:
        example_name: Name of the example to run.
        port: Port the Deephaven server is running on.
        examples_dir: Path to the examples directory.
    """
    import secrets
    
    try:
        from deephaven_server import Server
    except ImportError:
        print("Error: deephaven-server is not installed.")
        print("Run: pip install deephaven-server")
        sys.exit(1)

    # Determine examples directory
    if examples_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        examples_dir = os.path.join(os.path.dirname(script_dir), "examples")

    example_dir = os.path.join(examples_dir, example_name)

    if not os.path.isdir(example_dir):
        print(f"Error: Example '{example_name}' not found.")
        print()
        available = list_examples(examples_dir)
        if available:
            print("Available examples:")
            for ex in available:
                print(f"  - {ex}")
        else:
            print("No examples found in:", examples_dir)
        sys.exit(1)

    main_file = find_main_file(example_dir)
    if main_file is None:
        print(f"Error: No Python file found in example '{example_name}'")
        sys.exit(1)

    # Generate a PSK token for authentication
    psk_token = secrets.token_urlsafe(12)

    print(f"Starting Deephaven server on port {port}...")
    server = Server(port=port, jvm_args=[f"-Dauthentication.psk={psk_token}"])
    server.start()

    print(f"Running example: {example_name}")
    print(f"  File: {main_file}")
    print()

    # Execute the example
    with open(main_file, "r") as f:
        code = f.read()

    # Execute in Deephaven context
    from deephaven import empty_table
    exec(code, {"__name__": "__main__", "__file__": main_file})

    print()
    print(f"Example is running!")
    print(f"  Web UI: http://localhost:{port}/?psk={psk_token}")
    print()
    print("Press Ctrl+C to stop.")

    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


def main() -> None:
    """Main entry point."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_examples_dir = os.path.join(os.path.dirname(script_dir), "examples")

    parser = argparse.ArgumentParser(
        description="Run a Deephaven UI example.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "example",
        nargs="?",
        help="Name of the example to run (omit to list available examples)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=10000,
        help="Port to run the server on (default: 10000)",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available examples",
    )
    parser.add_argument(
        "--examples-dir",
        "-e",
        type=str,
        default=default_examples_dir,
        help="Path to examples directory",
    )

    args = parser.parse_args()

    if args.list or args.example is None:
        examples = list_examples(args.examples_dir)
        if examples:
            print("Available examples:")
            for ex in examples:
                print(f"  - {ex}")
        else:
            print("No examples found.")
            print(f"Examples directory: {args.examples_dir}")
        return

    run_example(args.example, port=args.port, examples_dir=args.examples_dir)


if __name__ == "__main__":
    main()
