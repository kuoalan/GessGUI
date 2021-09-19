# GessGUI
 Two player GUI implementation of the board game <a href="https://en.wikipedia.org/wiki/Gess">Gess</a> in Python 3 using PyGame.

<p float="left">
  <img src="https://github.com/kuoalan/GessGUI/blob/main/screenshots/screenshot_1.gif" width="400">
</p>

## Features
### Fully playable two player mode
* Keeps track of game state
* Shows which player is currently active and the starting and ending coordinates of the current move.
* Checks for illegal moves and provides feedback to user when illegal moves are made.

## Requirements
### Python 3
Download the appropriate installer for Python 3 for your operating system.

For Linux: `$sudo apt-get install python3`
### PyGame
To install PyGame, run: `pip install pygame` from the command line.
## Instructions
* Run `python3 Gess.py`from the command line.
* To make a move, click on the square corresponding to the center of a 'piece', then click on the square corresponding to the desired destination of the center of the 'piece'
* To play a new game, close the game window and run `python3 Gess.py` again from the command line.
