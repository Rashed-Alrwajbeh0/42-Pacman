# Pacman Game

## Configuration

First, we start by building the configuration of the game.

There is a configuration JSON file that the user provides as an argument in the terminal. We read this file and store the information in it to use throughout the game.

This part was made by **Rashed Alrwajbeh**.

## Main and Menu Page

Then, we build the main and menu page.

The main page contains buttons to:

* Start the game
* Show the high scores
* Change Pacman's controls
* Show the game instructions
* Exit the game

This page was made by **Rashed Alrwajbeh** and **Aeah Oqaily**.

## Pacman, Ghosts, Pacgums, and Maze

Then, we build Pacman, the ghosts, and the pacgums, create their classes, and make their graphics.

### Pacman

The `Pacman` class controls Pacman and contains all of his settings.

The person who built this class and made its graphics is **Rashed Alrwajbeh**.

### Ghosts

The `Ghost` class contains the main settings for each ghost.

There are four ghosts that inherit from this class, and each ghost has its own behavior.

This part was made by **Aeah Oqaily**, who also made the graphics for the ghosts.

### Maze

The `Maze` class contains all the settings for the maze and includes a function to generate it using the external `MazeGenerator` class.

This part was made by **Rashed Alrwajbeh** and **Aeah Oqaily**.

### Pacgums

The `Pacgum` class represents the pacgums in the game.

This part was made by **Rashed Alrwajbeh** and **Aeah Oqaily**.

## Scores and Controls Pages

Then, we build the scores and controls pages.

### Scores Page

The scores page contains the top 10 players with the highest scores.

This page and its graphics were made by **Aeah Oqaily**.

### Controls Page

The controls page contains a table showing the controls used to move Pacman, and the user can change them.

This page was made by **Rashed Alrwajbeh**.

## Cheat Mode, Makefile, and README

Then, we build the cheat mode.

Finally, we create the `Makefile` and the `README.md`.

These parts were made by **Rashed Alrwajbeh** and **Aeah Oqaily**.

## Testing

As an additional step, we tested several test cases to make sure that the game works correctly and that its different features behave as expected.

## Contributors

* **Rashed Alrwajbeh**
* **Aeah Oqaily**
