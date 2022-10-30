"""
Delta Seasonal Scorekeeper Driver Script

This script is designed to simplify the scorekeeping for the all-skiing yet somehow painfully
incompetent schkifreek, and allow Nitoxica and CD to rest assured that all is being
handled well with the Del Taco and related events.
"""

__author__ = "Nixotica"
__maintainer__ = "Nixotica"
__email__ = "nixotica@gmail.com"

import shutil
import sys
import os

WELCOME_MESSAGE_STR = "Welcome to the Delta Ultimate Scorekeeping Script!"

SEASONS_PATH = os.path.join(os.path.curdir, "Seasons")
RESOURCES_PATH = os.path.join(os.path.curdir, "resources")
SEASON_TEMPLATE_PATH = os.path.join(RESOURCES_PATH, "SeasonTemplate")

arg_map = {
    "ALL": 0,
    "-h": 0,
    "-n": 1,
    "-d": 2,
    "-l": 3,
    "-p": 4,
}

short_long_arg_map = {
    "-h": "--help",
    "-n": "--new_season",
    "-d": "--delete_season",
    "-l": "--list_seasons",
    "-p": "--points_repartition",
}


def fancy_bar(length: int = 32) -> str:
    return "=" * length


def print_usage(help_for: str = "ALL") -> None:
    h_str = "-h --help"
    n_str = "-n --new_season [name]"
    d_str = "-d --delete_season <name>"
    l_str = "-l --list_seasons"
    p_str = "-p --points_repartition <season> <type> <1st> [2nd] [3rd] ..."

    if help_for not in arg_map.keys():
        print(f"Invalid arg {help_for}, valid options:")
        print_usage()

    arg_strings = [h_str, n_str, d_str, l_str, p_str]
    max_argstrlen = max(len(arg_str) for arg_str in arg_strings)
    overflow_spacing = " " * (max_argstrlen + 4)

    h_note = "Prints this usage message for your assistance"
    n_note = "Generates all the necessary folders and files for a new season with optional name 'NAME'"
    d_note = "Deletes all the folders and files associated with a season with name 'NAME' (must type FULL name)"
    p_note = "Create a points repartition file with name corresponding to an existing season" \
             f", type (B: BRACKET | K: KO)\n{overflow_spacing}in order of 1st to the last position, " \
             "all other positions receive zero points"
    l_note = "Lists all the seasons currently created"

    arg_notes = [h_note, n_note, d_note, l_note, p_note]

    spacings = [" " * (max_argstrlen - len(arg_str)) for arg_str in arg_strings]

    delimiter = "|"

    if arg_map[help_for] == 0:
        for idx in range(len(arg_strings)):
            print(arg_strings[idx], spacings[idx], delimiter, arg_notes[idx])
    else:
        print(arg_strings[arg_map[help_for]], spacings[arg_map[help_for]], delimiter, arg_notes[arg_map[help_for]])


def print_help() -> None:
    print(fancy_bar(len(WELCOME_MESSAGE_STR)))
    print(WELCOME_MESSAGE_STR)
    print(fancy_bar(len(WELCOME_MESSAGE_STR)))
    print("")
    print_usage()


def print_all_seasons() -> None:
    if not os.path.exists(SEASONS_PATH):
        print("No seasons created yet!")
    for dir in os.listdir(SEASONS_PATH):
        print(dir)


def populate_season_with_template(name: str) -> None:
    """
    Populate a season with the default points repartition
    """
    path_to_populate = os.path.join(SEASONS_PATH, name)
    if not os.path.exists(path_to_populate):
        print(f"Season with name {name} does not exist!")
        return

    shutil.copytree(SEASON_TEMPLATE_PATH, path_to_populate)
    print(f"Successfully populated season {path_to_populate} with template!")


def handle_new_season(name: str) -> None:
    """
    Create a new season folder with the provided name if it doesn't exist.
    """
    if not os.path.exists(SEASONS_PATH):
        os.makedirs(SEASONS_PATH)

    path_to_make = os.path.join(SEASONS_PATH, name)
    if os.path.exists(path_to_make):
        print("Season with that name already exists!")
        return

    os.makedirs(path_to_make)
    populate_season_with_template(name)
    print(f"Successfully created {path_to_make}")


def handle_delete_season(name: str) -> None:
    """
    Delete a season and all its contents with the provided name if exists.
    """
    path_to_delete = os.path.join(SEASONS_PATH, name)
    if not os.path.exists(path_to_delete):
        print("Season with that name doesn't exist!")
        print_all_seasons()
        return

    shutil.rmtree(path_to_delete)
    print(f"Successfully deleted {path_to_delete}")


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        print_help()
    elif args[0] == "-h" or args[0] == "--help":
        print_usage("-h")
    elif args[0] == "-n" or args[0] == "--newseason":
        if len(args) != 2:
            print_usage("-n")
        else:
            handle_new_season(args[1])
    elif args[0] == "-d" or args[0] == "--deleteseason":
        if len(args) != 2:
            print_usage("-d")
        else:
            handle_delete_season(args[1])
    elif args[0] == "-l" or args[0] == "--listseasons":
        print_all_seasons()