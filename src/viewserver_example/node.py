"""
ViewServer Python Node — connects to a ReportingEngine and registers
Python-driven operators.

Run with:
    poetry run python -m viewserver_example.node
    poetry run python -m viewserver_example.node --config my_config.json
"""

import argparse
import json
import logging
import signal
import sys
import time
from pathlib import Path

from viewserver_example.transforms import (
    identity,
    add_total,
    filter_active,
    moving_average,
    z_score,
    rank_by,
    squared,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("ExampleNode")

DEFAULT_CONFIG = Path(__file__).parent.parent.parent.parent / "config.json"


def main():
    parser = argparse.ArgumentParser(description="Start an example ViewServer Python node")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to config JSON")
    args = parser.parse_args()

    try:
        from viewserver_python import ViewServerEngine
    except ImportError:
        logger.error(
            "Cannot import viewserver_python. Install it first:\n"
            "  pip install viewserver_python  (from GitHub Packages)\n"
            "  or: pip install /path/to/viewserver_python-*.whl  (local wheel)"
        )
        sys.exit(1)

    if not args.config.exists():
        logger.error("Config not found: %s", args.config)
        logger.info("Create a config.json — see viewserver-python/python_node_config.json for reference")
        sys.exit(1)

    config_json = args.config.read_text()
    cfg = json.loads(config_json)
    node_name = cfg["serviceConfig"]["name"]

    logger.info("Starting %s", node_name)

    engine = ViewServerEngine(config_json)
    engine.start()
    logger.info("%s started", node_name)

    # Register named operators — each wraps a transform function
    engine.register_python_operator("identity", identity)
    engine.register_python_operator("addTotal", add_total)
    engine.register_python_operator("filterActive", filter_active)
    engine.register_python_operator("squared", squared)

    # Register the generic script operator (transform defined in graph node config)
    engine.register_script_operator("pythonScript")

    logger.info("Registered operators: identity, addTotal, filterActive, squared, pythonScript")

    # Keep alive
    shutdown = False

    def on_signal(sig, _frame):
        nonlocal shutdown
        logger.info("Signal %s received, shutting down", sig)
        shutdown = True

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    logger.info("%s running. Ctrl+C to stop.", node_name)
    try:
        while not shutdown:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    engine.stop()
    logger.info("%s stopped", node_name)


if __name__ == "__main__":
    main()
