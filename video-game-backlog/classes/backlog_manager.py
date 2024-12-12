# -*- coding: utf-8 -*-
# This class handles the creation, reading, editing, and deletion of backlogs.
# It interacts directly with CSV files to store and retrieve data.

import os
import csv

class BacklogManager:
    def __init__(self, data_dir="./data"):
        # Store the directory where we put all backlog CSVs
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def list_backlogs(self):
        # List all CSV files in the data directory
        files = [f for f in os.listdir(self.data_dir) if f.endswith(".csv")]
        return files

    def backlog_exists(self, name):
        # Check if a backlog with a given name exists
        filename = self._format_filename(name)
        return os.path.exists(os.path.join(self.data_dir, filename))

    def create_backlog(self, name):
        # Create a new empty backlog as a CSV file
        filename = self._format_filename(name)
        path = os.path.join(self.data_dir, filename)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(["Name", "Release Date", "Metacritic", "Playtime (hrs)"])

    def add_game_to_backlog(self, backlog_name, game_data):
        # Append a game row to the backlog CSV
        filename = self._format_filename(backlog_name)
        path = os.path.join(self.data_dir, filename)
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(game_data)

    def read_backlog_games(self, backlog_name):
        # Read all games from a given backlog
        filename = self._format_filename(backlog_name)
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            return []
        games = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                games.append(row)
        return games

    def rename_backlog(self, old_name, new_name):
        # Rename the CSV file representing the backlog
        old_file = os.path.join(self.data_dir, self._format_filename(old_name))
        new_file = os.path.join(self.data_dir, self._format_filename(new_name))
        os.rename(old_file, new_file)

    def delete_backlog(self, name):
        # Delete the backlog CSV file
        filename = self._format_filename(name)
        path = os.path.join(self.data_dir, filename)
        if os.path.exists(path):
            os.remove(path)

    def delete_game_from_backlog(self, backlog_name, game_index):
        # Delete a game by its index (1-based)
        games = self.read_backlog_games(backlog_name)
        if 1 <= game_index <= len(games):
            del games[game_index - 1]
            # Rewrite CSV
            filename = self._format_filename(backlog_name)
            path = os.path.join(self.data_dir, filename)
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Release Date", "Metacritic", "Playtime (hrs)"])
                for g in games:
                    writer.writerow(g)
            return True
        return False

    def _format_filename(self, name):
        # Convert backlog name to a filename-safe format
        # e.g., "My PS5 Backlog" -> "My_PS5_Backlog.csv"
        safe_name = name.replace(" ", "_")
        return f"{safe_name}.csv"