#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Scott, this is the main entry point of the CLI tool.
# This file orchestrates the menu and calls classes from the 'classes' directory.

import sys
from classes.cli_handler import CLIHandler
from classes.backlog_manager import BacklogManager
from classes.utilities import clear_screen

def main():
    # Initialize managers
    backlog_manager = BacklogManager(data_dir="./data")
    cli_handler = CLIHandler(backlog_manager=backlog_manager)

    # Infinite loop until user decides to exit
    while True:
        clear_screen()
        print("=== Welcome to the Video Game Backlog Manager ===")
        print("1. Create a new Backlog")
        print("2. Edit an existing Backlog")
        print("3. Delete an existing Backlog")
        print("Type 'qu1t' to exit.")
        choice = input("Enter your choice: ").strip()

        if choice.lower() == "qu1t":
            print("Goodbye!")
            sys.exit(0)

        if choice == "1":
            cli_handler.handle_create_backlog()
        elif choice == "2":
            cli_handler.handle_edit_backlog()
        elif choice == "3":
            cli_handler.handle_delete_backlog()
        else:
            print("Invalid choice, please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()