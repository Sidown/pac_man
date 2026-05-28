*This project has been created as part of the 42 curriculum by cjeannin and clefrere.*

# Pac-Man Game

## Description

This project is a complete implementation of the classic Pac-Man game in Python. Players navigate through procedurally generated mazes, collecting Pac-gums while avoiding four intelligent AI-controlled ghosts (Blinky, Pinky, Inky, and Clyde). The game features a full graphical user interface with menus, a persistent high-score system, configurable difficulty levels, and modern Python practices including type hints and comprehensive architecture.

The goal of the project is to demonstrates core game development concepts including:
- AI pathfinding algorithms for non-player characters
- Collision detection and game state management
- Event-driven architecture with scene management
- Asset loading and sprite animation
- Configuration management and data persistence

## Instructions

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Installation and Setup

**Install dependencies:**
   ```bash
   make install
   ```
   This command syncs all dependencies via `uv` and installs the required `mazegenerator` wheel package.


### Running the Game

Start the game with:
```bash
make run
```

Or directly with Python:
```bash
uv run pac-man.py
```

### Game Controls

- **Arrow Keys**: Move Pac-Man
- **SPACE**: Pause game
- **Mouse**: Interact with menu buttons

### Development Commands

- **Lint code:** `make lint` (runs flake8 and mypy)
- **Debug:** `make debug` (starts Python debugger)
- **Clean:** `make clean` (removes cache and build artifacts)

## Configuration

Game behavior is controlled via [`json_file/config.json`](json_file/config.json). The configuration file uses a JSON format and supports comment lines (lines beginning with `#`).

### Configuration Structure

```json
{
  "highscore_filename": "./json_file/highscore.json",
  "lives": 3,
  "level_max_time": 90,
  "seed": 42,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "levels": [
    { "width": 15, "height": 15 },
    { "width": 15, "height": 15 }
  ]
}
```

### Configuration Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `highscore_filename` | string | Path to the JSON file storing persistent high scores |
| `lives` | int | Number of lives the player starts with |
| `level_max_time` | int | Time limit per level in seconds |
| `seed` | int | Random seed for initial maze generation (affects reproducibility) |
| `points_per_pacgum` | int | Points awarded when collecting a regular Pac-gum |
| `points_per_super_pacgum` | int | Points awarded when collecting a power-up (big Pac-gum) |
| `points_per_ghost` | int | Points awarded when eating a vulnerable ghost |
| `levels` | array | Array of level objects, each with `width` and `height` defining maze dimensions |

### Default Values

The default configuration provides a balanced game experience:
- 3 lives per game
- 90 seconds per level
- Standard 15x15 maze size for all 10 levels
- Scoring multipliers that reward skilled play

Modify these values to customize difficulty and game balance.

## Highscore System

The game implements a persistent high-score system that tracks player achievements across multiple game sessions.

### Implementation Details

- **Storage:** High scores are stored in [`json_file/highscore.json`](json_file/highscore.json) as a JSON file
- **Persistence:** Scores are automatically saved after each game completion
- **Display:** High scores are displayed in a dedicated GUI screen accessible from the main menu
- **Player Names:** When a player achieves score, they are prompted to enter their name
- **Ranking:** High scores are sorted in descending order with the highest score at the top

### Why This Implementation?

We chose a JSON-based approach for several reasons:
1. **Simplicity:** JSON is human-readable and easy to debug
2. **No database required:** Eliminates external dependencies for score storage
3. **Portability:** The JSON file can be easily shared or backed up

The `HighScore` class in [`GUI/score.py`](GUI/score.py) manages all highscore operations including loading, saving, and ranking.

## Maze Generation

This project uses the **A-Maze-ing** (`mazegenerator`) package to procedurally generate mazes. This package is provided as a wheel file (`mazegenerator-00001-py3-none-any.whl`).

### How It Works

1. **Maze Generation:** For each level, a new maze is generated using the `MazeGenerator` class with configurable dimensions and a random seed
2. **Seed Control:** The seed parameter ensures reproducible mazes while varying across levels
3. **Collision Detection:** The maze's wall data is used for collision detection between the player, ghosts, and walls
4. **Pac-gum Placement:** Regular and super Pac-gums are placed in all non-wall of the maze

### Integration in Code

The `Level` class in [`game_class/game.py`](game_class/game.py) demonstrates the usage:

```python
from mazegenerator.mazegenerator import MazeGenerator

maze = MazeGenerator(size=(15, 15), seed=42)
# Access maze data with: maze.maze (2D array where 15 = wall, other values = paths)
```

### Technical Details

- Mazes are represented as 2D arrays.
- Each cell in the maze grid contains wall information stored in an int using the 4 low significant bits:
- **North wall**: Blocks movement to the cell above. Encoded with the bit 0.
- **East wall**: Blocks movement to the cell on the right. Encoded with the bit 1.
- **South wall**: Blocks movement to the cell below. Encoded with the bit 2.
- **West wall**: Blocks movement to the cell on the left. Encoded with the bit 3.
- Path cells contain other values allowing for pathfinding algorithms
- The maze remains constant throughout a level but changes when advancing to the next level
- Each level's seed is deterministic for testing and consistency

## Implementation

### Technical Summary

This Pac-Man implementation uses a modular, object-oriented architecture written in Python 3.13 with full type hints. The project is organized into three main layers:

1. **Game Logic Layer** (`game_class/`): Handles core gameplay mechanics including player movement, ghost AI, collision detection, and level management
2. **GUI Layer** (`GUI/`): Manages all visual elements using Pygame, including the main loop, scene transitions, and UI components
3. **Utility Layer** (`utils/`): Provides helper functions for common operations

### Key Design Decisions

- **Abstract Base Classes:** The `Ghost` class is abstract, allowing four concrete implementations (Blinky, Pinky, Inky, Clyde) with different AI behaviors
- **Scene-Based GUI:** The GUI uses a scene pattern (`Scene` base class) for clean separation between different screens (menu, game, high scores, etc.)
- **Configuration-Driven:** Game parameters are loaded from JSON, making the game easily configurable without code changes
- **Type Safety:** Comprehensive type hints throughout enable static analysis and reduce runtime errors
- **Pydantic Validation:** Configuration files are validated using Pydantic models to ensure data integrity

### Project Structure

```
pac_man/
├── pac-man.py                      # Entry point and theme initialization
├── parser.py                    # Configuration loading and validation
├── Makefile                     # Build automation
├── pyproject.toml              # Project metadata and dependencies
├── game_class/                 # Core game logic
│   ├── __init__.py
│   ├── game.py                # Level management and game state
│   ├── player.py              # Pac-Man controller and animation
│   ├── ghost.py               # Ghost AI base class and pathfinding
│   ├── pacgum.py              # Collectible items
│   └── cheat.py               # Debug/cheat utilities
├── GUI/                        # User interface and rendering
│   ├── __init__.py
│   ├── gui_main_loop.py       # Main game loop (Visualizer class)
│   ├── gui_main_menu.py       # Main menu scene
│   ├── gui_game.py            # In-game HUD and rendering
│   ├── gui_game_over.py       # Game over screen
│   ├── gui_victory.py         # Level completion screen
│   ├── gui_highscore.py       # High score display
│   ├── gui_instruction.py     # Instructions/tutorial screen
│   ├── scene.py               # Scene base class
│   ├── score.py               # HighScore manager class
│   └── ui_elements/           # Reusable UI components
│       ├── __init__.py
│       ├── button.py          # Clickable button widget
│       ├── text.py            # Text rendering widget
│       ├── theme.py           # Theme configuration and colors
│       └── highscore_input.py # Name input widget
├── assets/                     # Game resources
│   ├── fonts/                 # TrueType font files
│   └── skin/                  # Sprite sheets and images
│       ├── ghosts/            # Ghost sprites
│       ├── pacman-up/         # Pac-Man animation frames
│       ├── pacman-down/
│       ├── pacman-left/
│       ├── pacman-right/
│       └── other/             # Pac-gums and other items
├── json_file/                 # Data files
│   ├── config.json           # Game configuration
│   └── highscore.json        # Persistent high scores
└── utils/                     # Utility functions
    ├── __init__.py
    └── not_corner.py         # Maze corner detection
```

## General Software Architecture

### High-Level Overview

The application follows a **three-layer architecture** with clean separation of concerns:

#### 1. Game Logic Layer (`game_class/`)

**Purpose:** Implements the core game mechanics independent of rendering.

**Key Classes:**

- **`Level`:** Manages a single game level including:
  - Maze generation and collision detection
  - Pac-gum and super Pac-gum placement
  - Ghost instantiation and initialization
  - Time management

- **`Player`:** Represents Pac-Man with:
  - Position and movement state
  - Directional animation management
  - Collision detection with Pac-gums and ghosts
  - Lives tracking

- **`Ghost` (Abstract Base):** Base class for all ghosts providing:
  - Movement and animation system
  - Collision detection
  - State management (normal/vulnerable/respawning)
  - Abstract `next_move()` method for AI

- **Ghost Implementations:** Four concrete classes with different pathfinding:
  - **`Blinky`:** Direct pursuit algorithm
  - **`Pinky`:** Predictive targeting (ahead of player)
  - **`Inky`:** Complex behavior using other ghosts' positions
  - **`Clyde`:** Scatter/chase alternation

#### 2. GUI Layer (`GUI/`)

**Purpose:** Handles all visual rendering and user interaction using Pygame.

**Architecture:**

- **`Visualizer` (Main Loop):** Central coordinator that:
  - Initializes Pygame and the display window
  - Manages the event loop
  - Transitions between scenes
  - Handles input events

- **`Scene` (Base Class):** Abstract base for all screens providing:
  - Common rendering interface
  - Event handling hooks
  - Transition management

- **Scene Implementations:**
  - `MainMenuScene`: Start screen with navigation
  - `GameScene`: In-game rendering with HUD
  - `GameOverScene`: Defeat screen
  - `VictoryScene`: Level completion screen
  - `HighScoreScene`: High score display and ranking
  - `InstructionScene`: Game rules and controls

- **UI Elements** (`ui_elements/`):
  - `Button`: Interactive menu button with hover effects
  - `Text`: Rendered text with customizable styling
  - `Theme`: Centralized color and font configuration
  - `HighScoreInput`: Name input widget for new high scores

#### 3. Utility Layer (`utils/`)

**Purpose:** Provides helper functions for common operations.

**Functions:**

- `not_corner()`: Determines if a maze cell is not in a corner (used for Pac-gum placement)

### Module Relationships

```
pac-man.py
  └─> Theme configuration
  └─> Visualizer (GUI/gui_main_loop.py)
        ├─> MainMenuScene
        ├─> GameScene
        │   └─> Level (game_class/game.py)
        │        ├─> Player
        │        ├─> Ghost subclasses
        │        └─> Pac-gum/SuperPac-gum
        ├─> GameOverScene
        ├─> VictoryScene
        ├─> HighScoreScene
        └─> InstructionScene

Parser (parser.py)
  └─> Config validation (pydantic)
  └─> Configuration loading
```

### Data Flow

1. **Startup:** `pac-man.py` loads theme → creates `Visualizer` → renders `MainMenuScene`
2. **Game Start:** Player selects "New Game" → `GameScene` created → `Level` initialized
3. **Game Loop:** `Visualizer.run()` continuously:
   - Processes input events
   - Updates game state (player, ghosts, collisions)
   - Renders current scene
4. **Scene Transitions:** Game events trigger transitions (e.g., level complete → victory screen)
5. **Persistence:** High scores saved to JSON after game completion


## Resources

### Classic Pac-Man References

- [Pac-Man Wikipedia](https://en.wikipedia.org/wiki/Pac-Man): Comprehensive history and mechanics
- [Ghost AI Behavior Documentation](https://pacman.fandom.com/wiki/Ghosts): Fan documentation of ghost behaviors
- Pygame Official Documentation: https://www.pygame.org/docs/
- pygame tuto: https://medium.com/@fulton_shaun/main-menus-to-cutscenes-building-game-screens-with-pygame-7415065c9fb9

### AI Usage in This Project

- AI was used to help us on the Readme generation.
- None of the code was generated by AI.


## Project Management
