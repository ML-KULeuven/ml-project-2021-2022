#!/usr/bin/env python3
# encoding: utf-8
"""
fcpa_agent.py

Extend this class to provide an agent that can participate in a tournament.

Created by Pieter Robberechts, Wannes Meert.
Copyright (c) 2021 KU Leuven. All rights reserved.
"""

import sys
import argparse
import logging

logger = logging.getLogger('be.kuleuven.cs.dtai.fcpa')


def get_agent_for_tournament():
    """Change this function to initialize your agent.
    This function is called by the tournament code at the beginning of the
    tournament.
    """
    my_player = Agent()
    return my_player


class Agent:
    def __init__(self):
        """Initialize an agent to play FCPA poker.

        Note: This agent should make use of a pre-trained policy to enter
        the tournament. Initializing the agent should thus take no more than
        a few seconds.
        """
        pass

    def start_game(self):
        """Starting a new game."""
        pass



def test_api_calls():
    """This method calls a number of API calls that are required for the
    tournament. It should not trigger any Exceptions.
    """
    agent = Agent()
    # TODO


def main(argv=None):
    test_api_calls()


if __name__ == "__main__":
    sys.exit(main())

