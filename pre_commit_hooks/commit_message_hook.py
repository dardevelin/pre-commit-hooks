#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import Sequence


"""The commit-msg Git hook for the project to validate the commit message."""
import sys
from enum import Enum

class Bcolors(str, Enum):
    """A Enum for colors using ANSI escape sequences.
    Reference:
    - https://stackoverflow.com/questions/287871
    """

    OK = "\033[92m"
    INFO = "\033[94m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    BOLD = "\033[1m"
    ENDC = "\033[0m"

class Level(str, Enum):
    """An Enum for notification levels."""

    OK = "OK"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def print_with_color(message: str, level: Level) -> None:
    """Print the message with a color for the corresponding level."""
    print(
        Bcolors[level]
        + Bcolors.BOLD
        + f"{level}: [Policy] "
        + message
        + Bcolors.ENDC
    )

def check_commit_msg_pattern():
    """Check the format of the commit message.
    The argument passed to the "commit-msg" hook is the path to a
    temporary file that contains the commit message written by the
    developer.
    """

    msg_temp_file = sys.argv[1]

    commit_message = None
    with open(msg_temp_file, "r", encoding="utf-8") as f_msg:
        commit_message = f_msg.readlines()
    
    # Remove the comment lines in the commit message.
    commit_message = [line for line in commit_message if not line.strip().startswith("#")]


    # commit message has at least 4 lines, title, empty line, body, empty line.
    has_warning = False
    if len(commit_message) < 4:
        message = "There should at least 4 lines in your commit message."
        print_with_color(message, Level.ERROR)
        sys.exit(1)

    title = commit_message[0]
    if len(title) > 50:
        has_warning = True
        message = (
            "There should be less then 50 characters in the commit title."
        )
        print_with_color(message, Level.WARNING)
        sys.exit(1)
    
    valid_commit_types = ["feat", "fix", "refactor", "style", "docs", "test", "chore", "revert"]
    if not any(title.startswith(commit_type) for commit_type in valid_commit_types):
        has_warning = True
        message = "The commit title needs to have a commit type: " + ", ".join(valid_commit_types)
        print_with_color(message, Level.WARNING)
        sys.exit(1)

    valid_issue_tracker_tools = ['jira', 'github', 'gitlab', 'bitbucket', 'launchpad', 'zendesk']
    valid_issue_tracker_tools_short_names = ['jr', 'gh', 'gl', 'bb', 'lp', 'zd']
    valid_issue_tracker_suffixes = [':', '/', '#', '-', ' ']

    # check if title has an issue tracker tool code after the commit type
    for valid_issue_tracker_tool in valid_issue_tracker_tools:
        if title.startswith(valid_issue_tracker_tool):
            has_warning = True
            message = "The commit title needs to have a commit type: " + ", ".join(valid_commit_types)
            print_with_color(message, Level.WARNING)
            sys.exit(1)
    
    # create a list of all valid issue tracker tools with all possible suffixes per tool
    valid_issue_tracker_tools_with_suffixes = []
    for valid_issue_tracker_tool in valid_issue_tracker_tools:
        for valid_issue_tracker_suffix in valid_issue_tracker_suffixes:
            valid_issue_tracker_tools_with_suffixes.append(valid_issue_tracker_tool + valid_issue_tracker_suffix)
    
    # add all valid issue tracker tools with short names to the list with all possible suffixes to valid issue tracker tools with all possible suffixes
    for valid_issue_tracker_tool_short_name in valid_issue_tracker_tools_short_names:
        for valid_issue_tracker_suffix in valid_issue_tracker_suffixes:
            valid_issue_tracker_tools_with_suffixes.append(valid_issue_tracker_tool_short_name + valid_issue_tracker_suffix)
    
    # check if the title has an issue tracker tool code with a suffix after the commit type and check if it is followed by a number
    valid_issue_tracker_tool_with_suffix = None
    for valid_issue_tracker_tool_with_suffix in valid_issue_tracker_tools_with_suffixes:
        if title.startswith(valid_issue_tracker_tool_with_suffix):
            if not title[len(valid_issue_tracker_tool_with_suffix):].isdigit():
                has_warning = True
                message = "The commit title needs to have a issue track tool code and number type: " + ", ".join(valid_commit_types)
                print_with_color(message, Level.WARNING)
                sys.exit(1)
    
    print(valid_issue_tracker_tool_with_suffix)
    sys.exit(1)


    

    

    
    if commit_message[1].strip() != "":
        has_warning = True
        message = (
            "There should be an empty line between the commit title and body."
        )
        print_with_color(message, Level.WARNING)
        sys.exit(1)

    has_story_id = False
    for line in commit_message[2:]:
        if len(line) > 72:
            has_warning = True
            message = "The commit body should wrap at 72 characters."
            print_with_color(message, Level.WARNING)
            sys.exit(1)

        if "[#" in line:
            has_story_id = True

    if not has_story_id:
        message = "Please add a Story ID in the commit message."
        print_with_color(message, Level.WARNING)
        sys.exit(1)

    if not has_warning:
        message = "The commit message has the required pattern."
        print_with_color(message, Level.OK)


def main(argv: Sequence[str] | None = None) -> int:
    """The main function."""
    check_commit_msg_pattern()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())