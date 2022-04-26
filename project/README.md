# Final Project - Tetris in Python

## Introduction
This is my final project in the CS50 Introduction to CS course and it is where I
made Tetris in Python. (Disclaimer: I don't own Tetris)

## What is Tetris?
Tetris is a game where you are given a grid and there are pieces that fall to the bottom and you are tasked to survive as long as possible, clearing lines as you do so.

In the game, you are able to score points, and you do this via clearing lines, from one all the wy to four, which is called a Tetris and provides you with the most amount of points. The pieces are genearated in a way that you are guaranteed to get each piece once and you are able to hold one piece and are able to switch between pieces once until you drop the piece that is falling.

In addition, you are able to perform 'Soft Drops' and 'Hard Drops', the 'Soft Drop' making the piece drop faster and the 'Hard Drop' making the piece drop almost immediately.

## Features
The main features that are included in my version of the game are as follows:
- **Two game modes:**
	- **infinte:** where you make as many lines as possible
	- **Sprint:** where you must get to 40 lines as fast as possible
- Stores the top five highest scores and fastest times with their names
- Includes a Leaderboard to display the highest scores and fastest times
- Controller Support

## Controls
There are two control schemes, one for the keyboard and the other for the controller (Note that I will refer to the Playstation Control Scheme):
### Keyboard Controls:
*In the Main Menu:*
- Up/Down/Left/Right navigates you in the main menu (Left and Right for the Leaderboard)
- Enter To Confirm your option
- Right Shift to go back

*In either Infinte of Sprint gamemodes:*
- left/right moves the piece left/right
- Down performs a 'Soft Drop'
- Space performs a 'Hard Drop'
- Up or 'x' rotates the piece clockwise
- Ctrl or 'z' rotates the piece counter-clockwise
- 'c' holds the current piece
- 'p' pauses the game

Most of the controls are similar to the controller in the main menu but there is a different control scheme when in one of the gamemodes:
- Left/Right moves the pieces Left/Right
- Circle rotates the piece clockwise
- X rotates the piece counter-clockwise
- Down performs the 'Soft Drop'
- UP performas the 'Hard Drop'
- R1 Holds the current piece

## Important Notes
Note that this was made in Python 3.8 (32bit) and uses Pygame v2.0.0.dev7, so you will need to install them if you want to play the game.