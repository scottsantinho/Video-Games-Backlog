#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py
import sys
from classes.cli_handler import CLIHandler
from classes.backlog_manager import BacklogManager
from classes.utilities import clear_screen
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def main():
    # Retrieve the API key from environment variables
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API key not found. Please set it in your .env file.")
        sys.exit(1)
        
    backlog_manager = BacklogManager(data_dir="./data")
    cli_handler = CLIHandler(backlog_manager=backlog_manager, api_key=api_key)

    while True:
        clear_screen()
        print("=== Welcome to the Video Game Backlog Manager ===")
        print("1. Create a new Backlog")
        print("2. Edit an existing Backlog")
        print("3. Delete an existing Backlog")
        print("4. View the content of an existing Backlog")
        print("Type 'qu1t' to exit.")
        choice = input("Enter your choice: ").strip()

        if choice.lower() == "qu1t":
            print("Goodbye!")
            sys.exit(0)
        elif choice == "1":
            cli_handler.handle_create_backlog()
        elif choice == "2":
            cli_handler.handle_edit_backlog()
        elif choice == "3":
            cli_handler.handle_delete_backlog()
        elif choice == "4":
            cli_handler.handle_view_backlog()
        else:
            print("Invalid choice, please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()