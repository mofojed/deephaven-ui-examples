"""Unit test package for chart-builder.

This module initializes the Deephaven server before any tests run.
The server is required because importing deephaven modules requires the JVM.
"""

from deephaven_server.server import Server

# Create a Server instance to initialize the JVM
# We don't need to start the server, just create an instance.
# See: https://github.com/deephaven/deephaven-plugins/blob/main/plugins/plotly-express/test/__init__.py
if Server.instance is None:
    Server(port=10001, jvm_args=["-Xmx4g"])
