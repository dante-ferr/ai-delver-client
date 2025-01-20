import pymunk
from ..tilemap_layer import TilemapLayer
import math
from typing import Literal, Callable
from ..tile.tile import Tile
from typing import TypedDict


class Line:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        orientation: Literal["horizontal", "vertical"],
    ):
        self.start = start
        self.end = end
        self.orientation = orientation

    @property
    def length(self):
        return math.sqrt(
            (self.end[0] - self.start[0]) ** 2 + (self.end[1] - self.start[1]) ** 2
        )


class Lines(TypedDict):
    horizontal: Line | None
    vertical: Line | None


class Node:
    lines: Lines = {
        "horizontal": None,
        "vertical": None,
    }

    def add_line(self, line: Line):
        self.lines[line.orientation] = line


class TilemapBorderTracer:
    def __init__(self, tilemap_layer: TilemapLayer):
        self.tilemap_layer = tilemap_layer
        self.nodes: dict[tuple[int, int], Node] = {}
        self.lines: set[Line] = set()
        self.debug_callbacks: list[Callable] = []

        for x in range(tilemap_layer.grid.shape[1]):
            for y in range(tilemap_layer.grid.shape[0]):
                tile = tilemap_layer.grid[y, x]
                if tile is None:
                    continue
                tile.add_format_callback(self._tile_format)

    def add_debug_callback(self, callback: Callable):
        self.debug_callbacks.append(callback)

    def _tile_format(self, tile: Tile):
        neighbors = self.tilemap_layer.get_neighbors_of(
            tile,
            same_autotile_object=True,
            output_type="tile_grid",
            adjacency_rule="four_neighbors",
        )
        if tile.position is None:
            return

        def handle_neighbor(
            pos: tuple[int, int],
            contact_line: tuple[tuple[int, int], tuple[int, int]],
            orientation: Literal["horizontal", "vertical"],
        ):
            pos_1, pos_2 = contact_line
            if neighbors[pos]:
                self._split_line_if_it_exists(pos_1, pos_2, orientation)
            else:
                self._create_node_pair(pos_1, pos_2, orientation)

        x, y = tile.position
        handle_neighbor((x + 1, y), ((x + 1, y), (x + 1, y + 1)), "vertical")
        handle_neighbor((x, y - 1), ((x, y), (x + 1, y)), "horizontal")
        handle_neighbor((x - 1, y), ((x, y), (x, y + 1)), "vertical")
        handle_neighbor((x, y + 1), ((x, y + 1), (x + 1, y + 1)), "horizontal")

        for callback in self.debug_callbacks:
            callback(tile)

    def _create_node_pair(
        self,
        pos1: tuple[int, int],
        pos2: tuple[int, int],
        orientation: Literal["horizontal", "vertical"],
    ):
        node_1, node_2 = (self.nodes.get(pos1), self.nodes.get(pos2))
        line_1, line_2 = (
            node_1.lines[orientation] if node_1 else None,
            node_2.lines[orientation] if node_2 else None,
        )
        if not node_1:
            node_1 = Node()
            self.nodes[pos1] = node_1
        if not node_2:
            node_2 = Node()
            self.nodes[pos2] = node_2

        if line_1 and line_2:
            self._merge_lines(line_1, line_2)
        elif line_1:
            node_2.add_line(line_1)
        elif line_2:
            node_1.add_line(line_2)
        else:
            line = Line(start=pos1, end=pos2, orientation=orientation)
            self.nodes[pos1].add_line(line)
            self.nodes[pos2].add_line(line)

    def _split_line_if_it_exists(
        self,
        pos1: tuple[int, int],
        pos2: tuple[int, int],
        orientation: Literal["horizontal", "vertical"],
    ):
        node_1, node_2 = (self.nodes.get(pos1), self.nodes.get(pos2))
        line_1, line_2 = (
            node_1.lines[orientation] if node_1 else None,
            node_2.lines[orientation] if node_2 else None,
        )
        if line_1 and line_2 and line_1 == line_2:
            line = line_1
            new_line_1 = Line(start=line.start, end=pos1, orientation=orientation)
            new_line_2 = Line(start=pos2, end=line.end, orientation=orientation)

            self.lines.add(new_line_1)
            self.lines.add(new_line_2)
            self.lines.remove(line)

    def _merge_lines(self, *lines):
        largest_line = max(lines, key=lambda line: line.length)
        largest_line.start = (
            min(lines, key=lambda line: line.start[0]).start[0],
            min(lines, key=lambda line: line.start[1]).start[1],
        )
        largest_line.end = (
            max(lines, key=lambda line: line.end[0]).end[0],
            max(lines, key=lambda line: line.end[1]).end[1],
        )

        for line in lines:
            if line == largest_line:
                continue
            self.lines.remove(line)

            for x in range(largest_line.start[0], largest_line.end[0]):
                for y in range(largest_line.start[1], largest_line.end[1]):
                    self.nodes[(x, y)] = largest_line
