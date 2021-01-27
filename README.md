
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

TODO

## Submission

To submit your agent, your code needs to be available on the departmental computers in a directory assigned to you (only your custom code, openspiel and other libraries are provided).

TODO

