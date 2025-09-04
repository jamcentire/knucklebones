# Knucklebones

Knucklebones is a dice game of skill and chance created for the video game Cult of the Lamb. This project comprises a statistical analysis of various strategies for the game, to determine what strategies are optimal. If you would like to read the full rules and play a game, check out the link below to find a beautiful website (not my work) that does just that. I will also give a brief explanation below.

https://knucklebones.io/en/

## Rules of the Game

Knucklebones is a two-player game, where each player's board comprises 3 columns that hold up to 3 dice each. Each column is aligned with its corresponding column on the other player's board. Each players score is determined by the dice in their columns.

On your turn, you roll a die, and then choose a column in which to place it. If you have multiples of one number in a column, that earns you extra points. If you place a die in a column, it removes every die from your opponent's corresponding column with the same number.

The game ends when a player completely fills their board, and whoever has the highest score is the winner!

## Heuristics

The meat of this software is testing different strategies. Strategies comprise an ordered list of heuristics, each of which takes in the board state and the die roll, and returns the optimal column (according to that heuristic) in which to place the die. If multiple columns are equally good solutions, the heuristic passes them to the next heuristic in the strategy, continuing until one placement is resolved.

## How to Play

To test a strategy, simply construct a player in main.py with an ordered list of heuristics, and run a series against another player. You can test strategies against each other, or against a baseline "dumb" strategy that chooses all columns randomly.

## Key Classes and Functions

PlayerBoard: The board of a single player. Manages board state and score.
GameBoard: All player boards in a Match. Manages PlayerBoard states, and delivering overall board state to heuristics.
Heuristics: Given the board state and die roll of a game round, determine the column in which to place the die. Each heuristic has its own rule for determining placement.
Player: An entity, containing an ordered list of heuristics, that can play a Match. This is the main vehicle for testing different strategies.
Match: Given multiple Players, manages playing one complete game of knucklebones. Contains most of the logging functionality used in debugging.
run_series: runs a series of Matches between two players, and displays win percentages.