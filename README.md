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
* **num_guesses**: The number of guesses it took to solve the puzzle.  Misses are stored as 7 to help with determining daily winners.
* **solved**:  A boolean whether the player solved the puzzle or not.
* **hard_mode**: A boolean whether the player enabled hard mode or not (denoted by an asterisk after the score in the wordle result).
* **puzzle**:  An object with the following fields:
  * **type**: Type of word game, for now only "Wordle" is supported.
  * **number**: The number of the puzzle (for example '500' for Wordle puzzle 500)
* **channel**: The unique discord ID for the channel in which the wordle result was posted.

If a user posts the same wordle result to multiple channels, a new entry will be appended to this list.  This way, daily rankings can be separated into servers (results in one server/channel won't affect another)

### Player All-Time Stats (TODO)

* **\_id**: A unique identifier
* **player**: An object with the following fields:
  * **name**: The player's Discord username.
  * **discriminator**:  The player's four digit Discord discriminator (the numbers after the #).
* **guess_totals**:  An object that tracks the number of times a puzzle has been solved with a certain number of guesses.
* **last_puzzle**:  An object that indicates the last puzzle the user played:
  * **0**: This field contains the **puzzle** object detailed above (type and number).
  * **1**: This field is the timestamp for when it was solved.
* **n_played**: An integer with the number of puzzles the person has played.
* **streak**: An object with the following fields:
  * **current**: The player's current active streak (calculated lazily upon a new puzzle addition).
  * **max**: The user's longest ever streak.
