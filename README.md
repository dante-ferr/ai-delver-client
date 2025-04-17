# AI Delver

**AI Delver** is a simulation framework where an AI agent learns to navigate 2D environments filled with obstacles, traps, and goals.

## Features

- 🧠 **AI Integration**: Reinforcement learning support for training agents to solve complex spatial challenges.
- 🧱 **Level Editor**: (Coming soon) A GUI tool for designing levels using a tile-based system powered by Pytiling.
- 📊 **Replay System**: Save and review agent behaviors across different environments (NOT AVAILABLE YET).

## Subprojects

- [`pytiling`](https://github.com/dante-ferr/pytiling.git): Autotiling library for handling tilemaps.
- [`pyglet_dragonbones`](https://github.com/dante-ferr/pyglet-dragonbones.git): Renderer for DragonBones animation assets in `pyglet`.
- [`ai_delver_intelligence`](https://github.com/dante-ferr/ai_delver_intelligence.git): Subproject that handles Ai Delver's Ai.

## Setup (Local)

To setup the project, you must:

- Git clone Ai Delver with its submodules: `git clone --recurse-submodules -j8 https://github.com/dante-ferr/ai-delver.git`
- Run `make build`
- Run `make run`

## COMMANDS

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

- `make run-ai`
  Only runs the ai_delver_intelligence container, without making it detached.

- `make run-main`
  Only runs the main application, without executing the docker container.

The run script performs these steps:

1. Starts the AI module using Docker Compose
2. Runs the specified application (game/ai/main)
3. Stops the AI module containers when done

```

```
