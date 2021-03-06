# prolog-tic-tac-toe
A full-stack tic-tac-toe game where the game logic is implemented in Prolog (SWI-Prolog specifically), the backend in Python3 and the frontend using Vue.js 3.\
The game logic uses [minimax](https://en.wikipedia.org/wiki/Minimax) + [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) to find the best move the computer can make.\
This was developed for educational purposes.\
\
![screenshot](https://user-images.githubusercontent.com/3015856/95652473-c5681800-0af9-11eb-9c2f-b211b965ca8b.png)

## How to run
There are 2 options for running the game server:

### Docker
Definitely the prefered way. Make sure you have Docker installed and running, `cd` directory and run:
- `docker build -t prolog-tic-tac-toe .`
- `docker run --rm -it -p 5000:5000 prolog-tic-tac-toe`
- Go to [http://localhost:5000/](http://localhost:5000/)

### Localy
- Make sure you have Python3 (3.6+) + SWIProlog installed locally (see [guide](https://github.com/yuce/pyswip/blob/master/INSTALL.md))
- Install Python dependencies - `python3 -m pip install requirements.txt`
- Run server - `python3 server/server.py`
- Go to [http://localhost:5000/](http://localhost:5000/)
