# -*- coding: utf-8 -*-
# Utility functions for clearing the screen, printing lists, etc.
import os

def clear_screen():
    # Clear the terminal screen (UNIX way)
    os.system("clear")

def print_backlog_list(backlogs):
    # Print a list of backlog files with indices
    for i, f in enumerate(backlogs, start=1):
        name = f[:-4].replace("_", " ")
        print(f"{i}. {name}")

def print_game_list(games, is_full_game_list=False):
    # Print games with indices
    # If games is from RAWG search results, it's a list of dict
    # If from backlog CSV, it's a list of lists (Name, Release Date, ...)
    if is_full_game_list:
        # Games is a list of lists from CSV
        for i, g in enumerate(games, start=1):
            print(f"{i}. {g[0]} (Release: {g[1]}, Metacritic: {g[2]}, Playtime: {g[3]}h)")
    else:
        # Games is a list of dict from RAWG
        for i, g in enumerate(games, start=1):
            print(f"{i}. {g.get('name', 'N/A')} (Released: {g.get('released', 'N/A')}, Metacritic: {g.get('metacritic', 'N/A')}, Playtime: {g.get('playtime', 'N/A')}h)")

def prompt_for_int(message):
    # Prompt user for integer input, return None if invalid
    val = input(message).strip()
    if val.lower() == "qu1t":
        return None
    if not val.isdigit():
        return None
    return int(val)