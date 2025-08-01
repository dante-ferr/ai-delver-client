# AI Delver

**AI Delver** is a simulation framework where an AI agent learns to navigate 2D environments filled with obstacles, traps, and goals.

## Features

- 🧠 **AI Integration**: Reinforcement learning support for training agents to solve complex spatial challenges.
- 🧱 **Level Editor**: A GUI tool for designing levels using a tile-based system powered by Pytiling.
- 📊 **Replay System**: Save and review agent behaviors across different environments (NOT AVAILABLE YET).

## Subprojects

- [`pytiling`](https://github.com/dante-ferr/pytiling.git): Autotiling library for handling tilemaps.
- [`pyglet_dragonbones`](https://github.com/dante-ferr/pyglet-dragonbones.git): Renderer for DragonBones animation assets in `pyglet`.

## Requirements

- A decent NVIDIA GPU
- NVIDIA Gpu Drivers
- NVIDIA Container Toolkit
- docker
- docker compose
- docker buildx
- python poetry

## Setup (Local)
            
To setup the project, you must:

- Git clone Ai Delver with its submodules: `git clone --recurse-submodules -j8 https://github.com/dante-ferr/ai-delver.git`
- Run `make build`
- Run `make run`

Note that this project requires proper GPU driver setup: you must have NVIDIA drivers and NVIDIA Container Toolkit installed in your system.

If you want to see the logs of ai_delver_intelligence's container, you need to:

- Run `make run-ai` first
- Once the intelligence api is up and running, open another terminal then run `make run-main`

## COMMANDS

- `make update-submodules`  
  Initializes and updates git submodules without overwriting local changes.

- `make ensure-env`  
  Creates a .env file in the intelligence directory with your UID and GID if it doesn't exist.

- `make build`  
  Builds and starts the Docker containers in detached mode. Automatically runs update-submodules and ensure-env first.

- `make run`  
  Runs the full application. Automatically runs update-submodules and ensure-env first.  
  You can specify an entry point by setting ENTRYPOINT:

  - `make run ENTRYPOINT=game` runs the game application
  - `make run ENTRYPOINT=ai` runs the AI application directly on the default level (My custom level.dill). It's been used for testing purposes only.
  - `make run ENTRYPOINT=editor` runs the editor application
  - Default (no ENTRYPOINT) runs main.py, which executes the editor app and the AI Docker container

- `make run-ai`
  Only runs the intelligence container, without making it detached. Mainly used in a separate terminal to allow the developer to see the container's internal logs.

- `make run-main`
  Only runs the main application, without executing the docker container.

```

```
