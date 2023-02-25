# Quantictactoe

<img src="https://i.imgur.com/NUVqTyi.png" width="453" height="629">

Quantum Tic Tac Toe is a variation of the classic game of Tic Tac Toe, where players use quantum mechanics concepts to create a more complex game with more strategic possibilities. This repository provides a Python implementation of the game created for the Zayed University Quantum Computing Hackathon, using Pygame and Qiskit.

# Getting Started
To run the game, you will need to have Python installed on your system. The code has been tested with Python 3.11.1. Additionally, the following packages need to be installed:

- Pygame
- Qiskit
You can install these packages using pip:

```
pip install pygame, qiskit
```
Once you have the required packages installed, clone the repository to your local machine:
```
git clone https://github.com/sohazur/Quantictactoe.git
```
# How to Play
To play Quantum Tic Tac Toe in a simulator (demo), run the main.py script in the root of the repository:

```
python main.py
```

To play in an IBM quantum computer, get your API token at https://quantum-computing.ibm.com/, and find a server with a minimum of 9 qubits. Replace the API token and the server name in the IBM.py file, and run it. 

```
python IBM.py
```


Players take turns placing their symbol (X or O) on the board until one of the following conditions is met:

- One player has made a line of three of their symbols in a row, column, or diagonal.
- The board is completely filled with symbols and no player has won.
- In addition to placing their symbol, players can also use superposition to manipulate the qubits on the board. These operation allow players to create more complex strategies and increase their chances of winning.

Symbols in superposition are colorful, while fixed symbols are white.

<img src="https://i.imgur.com/xNkDvFV.png" width="453" height="629">
<img src="https://i.imgur.com/ssmVBSx.png" width="453" height="629">

# Hotkeys

- C - Classical operation (place symbol)
- Q - Quantum operation (place symbol in superposition)
- M - Measure / Collapse

# 

# License
This repository is licensed under the MIT license. See the LICENSE file for more details.
