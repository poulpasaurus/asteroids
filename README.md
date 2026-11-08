# Asteroids

Small asteroids-style game made with pygame. The base follows the [Boot.dev](https://www.boot.dev) tutorial, and I added extra features on top of it.

# Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.13 (uv downloads it automatically if needed)
- pygame 2.6.1 (installed automatically by uv)

# How to run

**1 - clone the repo**
```bash
git clone https://github.com/poulpasaurus/asteroids.git
cd asteroids
```

**2 - run the game**
```bash
uv run main.py
```

# Controls

Designed for **AZERTY** keyboards

| Key | Action |
|---|---|
| Z | thrust forward |
| Q / D | rotate left / right |
| Space | shoot |

Close the window to quit

# Features beyond the course

- **Screen wrap-around**: the ship and the asteroids leaving one side of the screen come back from the opposite side and shots are removed once off-screen
- **Lives and respawn**: getting hit costs a life and respawns the ship in the center, with a short invincibility window
- **Score and high scores**: smaller asteroids are worth more points, and the 10 best scores are saved locally between games
- **Momentum**: the ship keeps drifting after you release the thrust
- **New shapes**: a ship with back wings and irregular, randomly shaded asteroids
- **Particles**: thruster flames, shot trails and asteroid explosions
- **Forgiving hitboxes**: collision circles slightly smaller than the drawn shapes

# High scores

High scores are saved in `scores.txt`, one score per line, best first. The file is created **in the folder you launch the game from**, so run the game from the project folder to keep a single high score list.

# Debug

Set `SHOW_HITBOXES = True` in `constants.py` to draw the collision circles in red.
