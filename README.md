
# ML Project 2021

This repository contains the code to setup the final evaluation of the course "[Machine Learning: Project](https://onderwijsaanbod.kuleuven.be/syllabi/e/H0T25AE.htm)" (KU Leuven, Faculty of engineering, Department of Computer Science, [DTAI research group](https://dtai.cs.kuleuven.be)).

## Use on departmental computeres

OpenSpiel is pre-installed in the following virtual environment:

```
/cw/ml-project/venv
```

## Local installation

This section describes how get started with using FCPA in OpenSpiel.

First, install OpenSpiel as [described on the github site](https://openspiel.readthedocs.io/en/latest/install.html#installation-from-source). Importantly, you must prepend a flag that will ensure it compiles the optional dependency on the [ACPC poker engine](http://www.computerpokercompetition.org/).

```
cd /path/to/open_spiel
BUILD_WITH_ACPC=ON ./install.sh
BUILD_WITH_ACPC=ON ./open_spiel/scripts/build_and_run_tests.sh

# Fix to PYTHONPATH, reload shell if necessary, etc.
. ./venv/bin/activate
python3 open_spiel/python/examples/poker_fcpa_example.py
```

This will run two random players in FCPA poker. You can also play fixed policies like always-call and always-fold, in addition to playing against them yourself on the keyboard by passing flags:

```
python3 python/examples/poker_fcpa_example.py \ 
    --player0=random --player1=human
```


## Tournament

The tournament will be played with agents that are available on the departmental computers. This will allow you to try your agent in the identical environment that is used by the tournament script. For this to work, you have to adhere to the following setup:

- Your agent extends the `Agent` class provided in the file `fcpa_agent/fcpa_agent.py`.
- The tournament code will scrape the directory provided for you on the departmental computers for the `fcpa_agent.py` file and call the `get_agent_for_tournament` method. If multiple matching files are found, a random one will be used.
- Your agent should be ready to play in a few seconds, thus use a pre-trained policy. An agent that is not responsding after 10 seconds will forfait the game.


## Submission using the Departmental Computers

To submit your agent, a copy of you code and agent needs to be available on the departmental computers in a directory assigned to you (only your own code, openspiel and other libraries are provided). Also the code to train your agent should be included.

The departmental computers have openspiel and its dependencies installed such that you can verify that your agent works. During the semester the tournament script will be run to play games between the (preliminary) agents that are already available. A tentative ranking will be shared.




