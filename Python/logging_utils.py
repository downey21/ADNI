
# -*- coding: utf-8 -*-

import logging

def setup_logging(log_file="output.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def log_print(message):
    """Print to console and write to log file."""
    print(message)
    logging.info(message)
