from bootstrap import *

# pipenv run python3 src/simulation_test.py

if __name__ == "__main__":
    from level import level_loader

    level_loader.load_level("data/level_saves/My custom level.dill")

    from runtime.simulation import simulation_controller

    frame = 0
    while True:
        simulation_controller.current_simulation.update((1 / 60) * 3)
        simulation_controller.current_simulation.delver.move(1 / 60, 180)
        print(frame)
        frame += 1
