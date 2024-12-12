# -*- coding: utf-8 -*-
# cli_handler.py
from .utilities import clear_screen, print_backlog_list, print_game_list
from .game_searcher import GameSearcher

class CLIHandler:
    def __init__(self, backlog_manager, api_key):
        self.backlog_manager = backlog_manager
        self.game_searcher = GameSearcher(api_key)

    # Existing methods...

    def handle_view_backlog(self):
        """Allow the user to view the games of an existing backlog."""
        while True:
            clear_screen()
            backlogs = self.backlog_manager.list_backlogs()
            if len(backlogs) == 0:
                print("No existing backlog.")
                input("Press Enter to return to main menu...")
                return  # Return to initial input stage

            print("Existing Backlogs:")
            print_backlog_list(backlogs)

            # If single backlog, select automatically
            if len(backlogs) == 1:
                choice = 1
            else:
                choice = input("Enter the backlog index to view or 'qu1t' to return: ").strip()
                if choice.lower() == "qu1t":
                    return
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(backlogs):
                    print("Invalid choice.")
                    input("Press Enter to continue...")
                    continue
                choice = int(choice)

            selected_backlog = backlogs[choice - 1]
            backlog_name = selected_backlog[:-4].replace("_", " ")

            # Show games in the selected backlog
            self._view_backlog_contents(backlog_name)
            return

    def _view_backlog_contents(self, backlog_name):
        """Display all games in the selected backlog."""
        clear_screen()
        games = self.backlog_manager.read_backlog_games(backlog_name)
        print(f"Backlog: {backlog_name}")
        if not games:
            print("No games in this backlog.")
        else:
            print_game_list(games, is_full_game_list=True)

        input("Press Enter to return to main menu...")

    def handle_delete_backlog(self):
        """Allow the user to delete an existing backlog."""
        while True:
            clear_screen()
            backlogs = self.backlog_manager.list_backlogs()
            if len(backlogs) == 0:
                print("No existing backlog.")
                input("Press Enter to return to main menu...")
                return

            print("Existing Backlogs:")
            print_backlog_list(backlogs)

            if len(backlogs) == 1:
                # If single backlog, select it by default
                choice = 1
            else:
                choice = input("Enter the backlog index to delete or 'qu1t' to return: ").strip()
                if choice.lower() == "qu1t":
                    return
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(backlogs):
                    print("Invalid choice.")
                    input("Press Enter to continue...")
                    continue
                choice = int(choice)

            selected_backlog = backlogs[choice - 1]
            selected_name = selected_backlog[:-4].replace("_", " ")

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete '{selected_name}'? (y/n or 'qu1t' to go back): ").strip().lower()
            if confirm == "qu1t":
                continue
            if confirm == "y":
                self.backlog_manager.delete_backlog(selected_name)
                print(f"Backlog '{selected_name}' deleted.")
                input("Press Enter to continue...")
            # After deletion, loop to allow deleting another backlog or returning