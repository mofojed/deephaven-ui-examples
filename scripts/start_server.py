#!/usr/bin/env python3
"""Start a Deephaven server for running examples."""

import argparse
import os
import sys
import time


def start_server(port: int = 10000, examples_dir: str | None = None) -> None:
    """Start the Deephaven server.

    Args:
        port: The port to run the server on.
        examples_dir: Path to the examples directory to make available.
    """
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

    if not os.path.isdir(examples_dir):
        print(f"Warning: Examples directory not found: {examples_dir}")

    print(f"Starting Deephaven server on port {port}...")
    print(f"Examples directory: {examples_dir}")

    # Start the server
    server = Server(port=port)
    server.start()

    print()
    print(f"Deephaven server is running!")
    print(f"  Web UI: http://localhost:{port}/ide/")
    print(f"  Examples available at: /data/examples/")
    print()
    print("Press Ctrl+C to stop the server.")

    # Keep the server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start a Deephaven server for running examples."
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=10000,
        help="Port to run the server on (default: 10000)",
    )
    parser.add_argument(
        "--examples-dir",
        "-e",
        type=str,
        default=None,
        help="Path to examples directory",
    )

    args = parser.parse_args()
    start_server(port=args.port, examples_dir=args.examples_dir)


if __name__ == "__main__":
    main()
