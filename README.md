# Color Fill Puzzle Game

A **Color Fill Puzzle Game** built with Python and Pygame. The objective is to color a 5x5 grid such that no two adjacent squares have the same color. You have four colors to choose from: Red, Green, Blue, and Yellow.

## Game Features

- **Grid-Based Puzzle**: The game board consists of a 5x5 grid of squares. All squares start as white, and the player colors them by clicking.
- **Color Selection**: Click on any color in the color selection panel to choose it, then click on a grid square to fill it with that color.
- **Valid Move Checks**: The game ensures no two neighboring squares share the same color.
- **Winning Condition**: You win when all squares are filled with colors, and no two adjacent squares have the same color.
- **Endgame Display**: Upon winning, a message displays "You won!" along with a "Start Over" button, allowing you to reset the board and play again.

## How to Play

1. **Choose a Color**: Use the color selection panel at the bottom of the screen to choose a color.
2. **Fill Squares**: Click on any white square in the grid to color it with the selected color.
3. **Avoid Repeating Colors**: Make sure no two adjacent squares have the same color.
4. **Win the Game**: Once all squares are colored without any adjacent duplicates, you’ll see a “You won!” message. Click "Start Over" to reset the board and try again.

## Controls

- **Left Click on Color Panel**: Select a color for filling squares.
- **Left Click on Grid Square**: Fill the clicked square with the selected color if the move is valid.

## Getting Started

To run the game, you’ll need to install Python and Pygame.

1. **Clone the repository**:
    ```bash
    https://github.com/tamara-kostova/Color-Fill-Puzzle-Game.git
    ```

2. **Install Pygame**:
    ```bash
    pip install pygame
    ```

3. **Run the game**:
    ```bash
    python main.py
    ```

## Dependencies

- **Python 3.x**
- **Pygame**

## Future Improvements

- Additional color themes or levels of difficulty.
- Timer to challenge players to complete the puzzle faster.
- Hint system to assist players if they’re stuck.
