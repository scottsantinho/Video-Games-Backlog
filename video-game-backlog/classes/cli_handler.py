# -*- coding: utf-8 -*-
# This class handles all CLI interactions with the user.
# It uses BacklogManager and GameSearcher to perform actions.
# It also guides the user through menus and sub-menus.
# It is the "controller" between the user and the data logic.

from .utilities import clear_screen, print_backlog_list, print_game_list
from .game_searcher import GameSearcher

class CLIHandler:
    def __init__(self, backlog_manager, api_key):
        self.backlog_manager = backlog_manager
        self.game_searcher = GameSearcher(api_key)

    def handle_create_backlog(self):
        # Stage 1: Create a new backlog
        while True:
            clear_screen()
            name = input("Enter a name for the new backlog (or 'qu1t' to go back): ").strip()
            if name.lower() == "qu1t":
                return
            if self.backlog_manager.backlog_exists(name):
                print("Backlog name already exists. Please choose another name.")
                input("Press Enter to try again...")
            else:
                self.backlog_manager.create_backlog(name)
                print(f"Backlog '{name}' created successfully!")
                input("Press Enter to continue...")
                self._prompt_add_game_to_backlog(name)
                return

    def handle_edit_backlog(self):
        # Stage 2: Edit an existing backlog
        while True:
            clear_screen()
            backlogs = self.backlog_manager.list_backlogs()
            if len(backlogs) == 0:
                print("No existing backlog. Returning to main menu.")
                input("Press Enter...")
                return

            print("Existing Backlogs:")
            print_backlog_list(backlogs)

            if len(backlogs) == 1:
                # If there is a single backlog, choose it by default
                choice = 1
            else:
                choice = input("Enter the backlog index or 'qu1t' to return: ").strip()
                if choice.lower() == "qu1t":
                    return
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(backlogs):
                    print("Invalid choice.")
                    input("Press Enter to continue...")
                    continue
                choice = int(choice)

            selected_backlog = backlogs[choice - 1]
            selected_name = selected_backlog[:-4].replace("_", " ")  # Reconstructing name from filename
            self._edit_backlog_submenu(selected_name)
            return

    def handle_delete_backlog(self):
        # Stage 3: Delete an existing backlog
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

    def _prompt_add_game_to_backlog(self, backlog_name):
        # Prompt user to add a game or return to main menu
        while True:
            clear_screen()
            print(f"Editing backlog: {backlog_name}")
            print("1. Add a game")
            print("2. Return to main menu")
            choice = input("Your choice: ").strip()
            if choice.lower() == "qu1t":
                # qu1t always goes back to previous stage
                return
            if choice == "1":
                self._add_game_flow(backlog_name)
            elif choice == "2":
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def _add_game_flow(self, backlog_name):
        # Steps for adding a game to the backlog
        while True:
            clear_screen()
            query = input("Enter the name (or partial name) of the game to search (or 'qu1t' to return): ").strip()
            if query.lower() == "qu1t":
                return

            # Ask user to select platform
            print("Select a platform (or 'qu1t' to return):")
            print("1. PC (ID: 4)")
            print("2. PlayStation 5 (ID: 187)")
            print("3. PlayStation 4 (ID: 18)")
            print("4. Xbox One (ID: 1)")
            print("5. Xbox Series S/X (ID: 186)")
            print("6. Nintendo Switch (ID: 7)")
            p_choice = input("Your choice: ").strip()
            if p_choice.lower() == "qu1t":
                return

            platform_map = {
                "1": 4,
                "2": 187,
                "3": 18,
                "4": 1,
                "5": 186,
                "6": 7
            }

            if p_choice not in platform_map:
                print("Invalid platform choice.")
                input("Press Enter to try again...")
                continue

            platform_id = platform_map[p_choice]

            results = self.game_searcher.search_games(query=query, platform_id=platform_id, page_size=30)
            if not results:
                print("No results found. Try another search.")
                input("Press Enter to continue...")
                continue

            # Print results
            print_game_list(results)
            game_index = input("Enter the game index to add to backlog (or 'qu1t' to return): ").strip()
            if game_index.lower() == "qu1t":
                return

            if not game_index.isdigit() or int(game_index) < 1 or int(game_index) > len(results):
                print("Invalid index.")
                input("Press Enter to continue...")
                continue

            chosen_game = results[int(game_index) - 1]
            game_data = self.game_searcher.get_game_data_row(chosen_game)
            self.backlog_manager.add_game_to_backlog(backlog_name, game_data)
            print(f"Added '{game_data[0]}' to '{backlog_name}'.")
            input("Press Enter to continue...")

            # Ask if user wants to add another game
            again = input("Add another game? (y/n or 'qu1t' to return): ").strip().lower()
            if again == "qu1t":
                return
            if again == "y":
                continue
            else:
                return

    def _edit_backlog_submenu(self, backlog_name):
        # Display games and allow user to add, rename, delete or go back
        while True:
            clear_screen()
            games = self.backlog_manager.read_backlog_games(backlog_name)
            print(f"Backlog: {backlog_name}")
            print_game_list(games, is_full_game_list=True)
            print("Options:")
            print("a. Add a game")
            print("b. Change backlog name")
            print("c. Delete a game")
            print("d. Go back to main menu")
            choice = input("Your choice (or 'qu1t' to go back): ").strip().lower()

            if choice == "qu1t":
                return
            if choice == "a":
                self._add_game_flow(backlog_name)
            elif choice == "b":
                self._rename_backlog_flow(backlog_name)
                # If renamed, the backlog_name changes
                return
            elif choice == "c":
                self._delete_game_flow(backlog_name)
            elif choice == "d":
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def _rename_backlog_flow(self, backlog_name):
        while True:
            new_name = input("Enter new backlog name (or 'qu1t' to return): ").strip()
            if new_name.lower() == "qu1t":
                return
            if self.backlog_manager.backlog_exists(new_name):
                print("Name already exists. Please choose another name.")
                input("Press Enter to continue...")
            else:
                self.backlog_manager.rename_backlog(backlog_name, new_name)
                print(f"Renamed backlog '{backlog_name}' to '{new_name}'.")
                input("Press Enter to continue...")
                return

    def _delete_game_flow(self, backlog_name):
        while True:
            games = self.backlog_manager.read_backlog_games(backlog_name)
            if not games:
                print("No games to delete.")
                input("Press Enter to continue...")
                return
            print_game_list(games, is_full_game_list=True)
            choice = input("Enter the game index to delete or 'qu1t' to return: ").strip()
            if choice.lower() == "qu1t":
                return
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(games):
                print("Invalid choice.")
                input("Press Enter to continue...")
                continue
            confirm = input("Confirm deletion? (y/n or 'qu1t' to return): ").strip().lower()
            if confirm == "qu1t":
                return
            if confirm == "y":
                self.backlog_manager.delete_game_from_backlog(backlog_name, int(choice))
                print("Game deleted.")
                input("Press Enter to continue...")
            # Continue asking if user wants to delete more games
    
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