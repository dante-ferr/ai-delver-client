# AI Delver

**AI Delver** is a simulation framework where an AI agent learns to navigate 2D environments filled with obstacles, traps, and goals. It combines procedural level design, reinforcement learning, and custom visualization to explore how agents adapt to dynamic dungeon-like environments.

## Features

- 🧠 **AI Integration**: Reinforcement learning support for training agents to solve complex spatial challenges.
- 🧱 **Level Editor**: (Coming soon) A GUI tool for designing levels using a tile-based system powered by Pytiling.
- 📊 **Replay System**: Save and review agent behaviors across different environments (NOT AVAILABLE YET).

## Subprojects

- [`pytiling`](./pytiling): Autotiling engine for procedural and user-defined map generation.
- [`pyglet_dragonbones`](./pyglet_dragonbones): Renderer for DragonBones animation assets in `pyglet`.

### Setup (Local)

To setup the project, you must:

- Git clone Ai Delver with its submodules: `git clone --recurse-submodules -j8 https://github.com/dante-ferr/ai-delver.git`
- Run `make build`
- Run `make run`

### COMMANDS

- `make update-submodules`  
  Initializes and updates git submodules without overwriting local changes.

- `make ensure-env`  
  Creates a .env file in the ai_delver_intelligence directory with your UID and GID if it doesn't exist.

- `make build`  
  Builds and starts the Docker containers in detached mode. Automatically runs update-submodules and ensure-env first.

- `make run`  
  Runs the main application. Automatically runs update-submodules and ensure-env first.  
  You can specify an entry point by setting ENTRYPOINT:
  - `make run ENTRYPOINT=game` runs the game application
  - `make run ENTRYPOINT=ai` runs the AI application
  - Default (no ENTRYPOINT) runs main.py

The run script performs these steps:

1. Starts the AI module using Docker Compose
2. Runs the specified application (game/ai/main)
3. Stops the AI module containers when done

```

```
