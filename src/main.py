#!/usr/bin/env python3
"""
Main entry point for the Data Pipeline application
"""
import sys
from src.presentation.cli.commands import cli

if __name__ == "__main__":
    sys.exit(cli())