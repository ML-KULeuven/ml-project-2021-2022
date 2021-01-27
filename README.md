
# ML Project 2021

This repository contains the code to setup the final evaluation of the course "[Machine Learning: Project](https://onderwijsaanbod.kuleuven.be/syllabi/e/H0T25AE.htm)" (KU Leuven, Faculty of engineering, Department of Computer Science, [DTAI research group](https://dtai.cs.kuleuven.be)).

## Installation

You will need `openspiel` version 2 or higher (and its dependencies).

It is recommended to install from source because you need the version with ACPC included to have access to the poker game. Follow the instructions on https://openspiel.readthedocs.io/en/latest/install.html#installation-from-source and make sure to set the following environment variable to true before compiling:

```sh
export BUILD_WITH_ACPC="ON"
```

After compilation, you should have access to the `universal_poker` game:

```sh
cd /path/to/openspiel/
. ./venv/bin/activate
python3 open_spiel/python/examples/example.py --game=universal_poker
```


## Tournament

The tournament will be played with agents that are available on the departmental computers. This will allow you to try your agent in the identical environment that is used by the tournament script. For this to work, you have to adhere to the following setup:

- Your agent extends the `Agent` class provided in the file `fcpa_agent/fcpa_agent.py`.
- The tournament code will scrape the directory provided for you on the departmental computers for the `fcpa_agent.py` file and call the `get_agent_for_tournament` method. If multiple matching files are found, a random one will be used.
- Your agent should be ready to play in a few seconds, thus use a pre-trained policy. An agent that is not responsding after 10 seconds will forfait the game.


## Submission

To submit your agent, your code needs to be available on the departmental computers in a directory assigned to you (only your custom code, openspiel and other libraries are provided). Also the code to train your agent should be included.


