from .skeleton.skeleton import Skeleton
import game.groups as groups
from .skeleton.skeleton_body import SkeletonBody
import json

with open("game/config.json", "r") as file:
    config_data = json.load(file)

window_width = config_data["window_width"]
window_height = config_data["window_height"]


class Player(Skeleton):
    speed = 200

    def __init__(self, space):
        player_body = SkeletonBody(
            space=space,
            position=(
                window_width / 2,
                window_height / 2,
            ),
            damping=0.02,
        )
        super().__init__("assets/sprites/delver", groups.delver, player_body)

        self.body.set_damping(1)

    def animation_run(self, animation_name: str | None, starting_frame=0, speed=1):
        self.animation.run(animation_name, starting_frame, speed)

        # match animation_name:
        #     case "run":
        #         self.body.set_damping(1)
        #     case None:
        #         self.body.set_damping(1)
