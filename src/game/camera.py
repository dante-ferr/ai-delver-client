from pyglet.window import Window
from pyglet.math import Vec3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entities.entity import Entity


class Camera:
    """A simple 2D camera that contains the speed and offset."""

    offset_x: float = 0
    offset_y: float = 0
    target_position: tuple[float, float] | None = None

    entity_being_followed: "Entity | None" = None
    follow_smoothing_factor = 0.05

    _zoom_target: float = 1.0
    zoom_smoothing_factor: float = 0.1

    def __init__(
        self,
        window: Window,
        scroll_speed=1.0,
        start_zoom=1.0,
        min_zoom=1.0,
        max_zoom=4.0,
    ):
        assert (
            min_zoom <= max_zoom
        ), "Minimum zoom must not be greater than maximum zoom"
        self._window = window
        self.scroll_speed = scroll_speed

        self.max_zoom = max_zoom
        self.min_zoom = min_zoom

        self.immediate_zoom(1.0)
        self.begin()
        self.immediate_zoom(start_zoom)
        self.end()

    def immediate_zoom(self, value: float):
        """Set the zoom value immediately."""
        clamped_value = self._clamp_zoom(value)
        self._zoom_target = clamped_value
        self._zoom = clamped_value

    @property
    def zoom(self):
        """ "Get the current zoom target value."""
        return self._zoom_target

    @zoom.setter
    def zoom(self, value):
        """Here we set zoom target, clamp value to minimum of min_zoom and max of max_zoom."""
        self._zoom_target = self._clamp_zoom(value)

    def _clamp_zoom(self, value: float):
        """Clamp zoom value to min and max zoom."""
        return max(min(value, self.max_zoom), self.min_zoom)

    @property
    def position(self):
        """Query the current offset."""
        return self.offset_x, self.offset_y

    @position.setter
    def position(self, value):
        """Set the scroll offset directly."""
        self.offset_x, self.offset_y = value

    def move(self, axis_x, axis_y):
        """Move axis direction with scroll_speed.
        Example: Move left -> move(-1, 0)
        """
        self.offset_x += self.scroll_speed * axis_x
        self.offset_y += self.scroll_speed * axis_y

    def start_following(self, entity: "Entity"):
        """Start following a given entity."""
        self.entity_being_followed = entity

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()

    def begin(self):
        self._apply_view_matrix_transformation()

        self._follow_entity()
        self._execute_zoom()

    def end(self):
        self._restore_view_matrix()

    def translate_mouse_coords(self, coords: tuple[float, float]):
        x, y = coords
        camera_x, camera_y = self.position

        translated_x = (-camera_x + x) * self._zoom + (self._window.width / 2) * (
            1 - self._zoom
        )
        translated_y = (-camera_y + y) * self._zoom + (self._window.height / 2) * (
            1 - self._zoom
        )

        return (translated_x, translated_y)

    def _apply_view_matrix_transformation(self):
        x = -self._window.width // 2 / self._zoom + self.offset_x
        y = -self._window.height // 2 / self._zoom + self.offset_y

        view_matrix = self._window.view.translate(
            Vec3(-x * self._zoom, -y * self._zoom, 0)
        )
        view_matrix = view_matrix.scale(Vec3(self._zoom, self._zoom, 1))
        self._window.view = view_matrix

    def _restore_view_matrix(self):
        x = -self._window.width // 2 / self._zoom + self.offset_x
        y = -self._window.height // 2 / self._zoom + self.offset_y

        view_matrix = self._window.view.scale(Vec3(1 / self._zoom, 1 / self._zoom, 1))
        view_matrix = view_matrix.translate(Vec3(x * self._zoom, y * self._zoom, 0))
        self._window.view = view_matrix

    def _execute_zoom(self):
        """Execute the zoom at each frame."""
        self._zoom += (self._zoom_target - self._zoom) * self.zoom_smoothing_factor

    def _follow_entity(self):
        """ "Set the camera position to follow a given entity."""
        if not self.entity_being_followed:
            return

        # self.target_position = (
        #     (
        #         -self.entity_being_followed.position[0] / self._zoom
        #         + (self._window.width / 2) / self._zoom
        #     ),
        #     (
        #         -self.entity_being_followed.position[1] / self._zoom
        #         + (self._window.height / 2) / self._zoom
        #     ),
        # )
        self.target_position = (
            (-self.entity_being_followed.position[0] + self._window.width / 2)
            / self._zoom,
            (-self.entity_being_followed.position[1] + self._window.height / 2)
            / self._zoom,
        )

        self.position = (
            self.position[0]
            + (self.target_position[0] - self.position[0])
            * self.follow_smoothing_factor,
            self.position[1]
            + (self.target_position[1] - self.position[1])
            * self.follow_smoothing_factor,
        )
