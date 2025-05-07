"""
An example entrypoint.
"""

import logging
import argparse

logger = logging.getLogger(__name__)

def executable():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] (%(levelname)s) %(message)s")

    # Create an argument parser object.
    parser = argparse.ArgumentParser(description="Python Example Template")

    parser_group_1 = parser.add_argument_group("logging")
    parser_group_1.add_argument("--verbose", type=bool, help="toggle verbose output", metavar="")
    parser_group_1.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "ERROR"], metavar="LEVEL", help="the global logging level to display", required=False, default="INFO")

    # Parse arguments.
    namespace = parser.parse_args()

    arguments = vars(namespace)

if __name__ == "__main__":
    executable()
