#!/usr/bin/env python3
# encoding: utf-8
"""
tournament.py

Code to play a round robin tournament between fcpa agents.

Created by Pieter Robberechts, Wannes Meert.
Copyright (c) 2021 KU Leuven. All rights reserved.
"""
import importlib.util
import itertools
import logging
import os
import sys
from pathlib import Path

import click
import pandas as pd
import numpy as np
from tqdm import tqdm

import pyspiel
from open_spiel.python.algorithms.evaluate_bots import evaluate_bots

logger = logging.getLogger('be.kuleuven.cs.dtai.fcpa.tournament')


def load_agent(path, player_id):
    """Inintialize an agent from a 'fcpa_agent.py' file.
    """
    spec = importlib.util.spec_from_file_location("fcpa_agent", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo.get_agent_for_tournament(player_id)


def load_agents_from_dir(path):
    """Scrapes a directory for fcpa agents.

    This function searches all subdirectories for an 'fcpa_agent.py' file and
    calls the 'get_agent_for_tournament' method. If multiple matching files
    are found, a random one will be used. The subdirectorie's name is used
    as the agent's ID.
    """
    agents = {}
    for agent_path in Path(path).glob('**/fcpa_agent.py'):
        agent_id = agent_path.parts[0]
        agents[agent_id] = {
            'id':  agent_id,
            'agent_p1': load_agent(agent_path, 0),
            'agent_p2': load_agent(agent_path, 1)
        }
    return agents


def play_tournament(game, agents, seed=1234, rounds=100):
    """Play a round robin tournament between multiple agents.
    """
    rng = np.random.RandomState(seed)
    # Load each team's agent
    results = []
    for _ in tqdm(range(rounds)):
        for (agent1, agent2) in list(itertools.permutations(agents.keys(), 2)):
            returns = evaluate_bots(
                    game.new_initial_state(), 
                    [agents[agent1]['agent_p1'], agents[agent2]['agent_p2']], 
                    rng)
            results.append({
                "agent_p1": agent1,
                "agent_p2": agent2,
                "return_p1": returns[0],
                "return_p2": returns[1]
            })
    return results


@click.command()
@click.argument('agentsdir', type=click.Path(exists=True))
@click.argument('outputdir', type=click.Path(exists=True))
@click.option('--rounds', default=20, help='Number of rounds to play.')
@click.option('--seed', default=1234, help='Random seed')
def cli(agentsdir, outputdir, rounds, seed):
    """Play a round robin tournament"""
    logging.basicConfig(level=logging.INFO)

    # Create the game
    fcpa_game_string = pyspiel.hunl_game_string("fcpa")
    logger.info("Creating game: {}".format(fcpa_game_string))
    game = pyspiel.load_game(fcpa_game_string)
    # Load the agents
    logger.info("Loading the agents")
    agents = load_agents_from_dir(agentsdir)
    # Play the tournament
    logger.info("Playing the tournament with {} agents in {} rounds".format(len(agents), rounds))
    results = play_tournament(game, agents, seed, rounds)
    # Process the results
    logger.info("Processing the results")
    results = pd.DataFrame(results)
    rankingH = results.groupby('agent_p1')['return_p1'].sum()
    rankingA = results.groupby('agent_p2')['return_p2'].sum()
    ranking = (rankingH + rankingA).to_frame().reset_index()
    ranking.columns = ['agent', 'return']
    ranking.sort_values(by='return', ascending=False, inplace=True)
    # Save the results
    results.to_csv(os.path.join(outputdir, 'results.csv'), index=False)
    ranking.to_csv(os.path.join(outputdir, 'ranking.csv'), index=False)
    logger.info("Done. Results saved to {}".format(outputdir))


if __name__ == '__main__':
    sys.exit(cli())
