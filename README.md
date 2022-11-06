# wordle_stats
discord bot to automatically parse wordle result messages

## Requirements
Requires Python 3.10 and packages in requirements.txt

## Database Schema

### Wordle Results
Wordle results are stored in MongoDB using the following document schema (one document per player per wordle)

* **\_id**: A string in the format **{username}\_{discriminator}\_wordle\_{Puzzle Number}**.  The database enforces unique IDs, so it is not possible for a player to send multiple results for the same wordle puzzle.
* **time**: UTC timestamp when the Discord message was received.
* **player**: An object with the following fields:
  * **name**: The player's Discord username.
  * **discriminator**:  The player's four digit Discord discriminator (the numbers after the #).
  * **num_guesses**: The number of guesses it took to solve the puzzle.  Currently misses are stored as 0, but this will soon be updated to 7 to help with determining daily winners.
* **solved**:  A boolean whether the player solved the puzzle or not.
* **hard_mode**: A boolean whether the player enabled hard mode or not (denoted by an asterisk after the score in the wordle result).
* **puzzle**:  An object with the following fields:
  * **type**: Type of word game, for now only "wordle" is supported.
  * **number**: The number of the puzzle (for example '500' for Wordle puzzle 500)

### Player All-Time Stats
  Description of how all-time stats are stored is to come
