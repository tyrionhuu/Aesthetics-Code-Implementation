from typing import TypeAlias, Union

from asthetic_code.utils import unit_conversion
from pptx.shapes.autoshape import Shape as AutoShape
from pptx.shapes.base import BaseShape
from pptx.shapes.connector import Connector
from pptx.shapes.graphfrm import GraphicFrame
from pptx.shapes.group import GroupShape
from pptx.shapes.picture import Movie, Picture
from pptx.shapes.placeholder import BasePlaceholder
from pptx.util import Length

Shape: TypeAlias = Union[
    BaseShape,
    AutoShape,
    Connector,
    GraphicFrame,
    GroupShape,
    Picture,
    Movie,
    BasePlaceholder,
]


class SegmentTreeNode:
    def __init__(self, shapes: list[Shape], subregions=None):
        self._shapes = shapes  # List of shapes in this region
        self._subregions = subregions if subregions is not None else []

    def is_leaf(self):
        return len(self._subregions) == 0


class Segmenter:
    def __init__(
        self,
        shapes: list[Shape],
        slide_width: Length,
        slide_height: Length,
        measurement_unit: str = "pt",
    ):
        self._shapes = shapes
        self._measurement_unit = measurement_unit
        self._slide_width = unit_conversion(slide_width, self._measurement_unit)
        self._slide_height = unit_conversion(slide_height, self._measurement_unit)

    def segment(self) -> SegmentTreeNode:
        return self._segment_region(self._shapes)

    def _segment_region(self, shapes: list[Shape]) -> SegmentTreeNode:
        # Try to split with horizontal line
        subregions = self._try_split(shapes, "horizontal")
        if subregions:
            return SegmentTreeNode(
                shapes, [self._segment_region(subregion) for subregion in subregions]
            )

        # If horizontal split is not possible, try vertical grid lines
        subregions = self._try_split(shapes, "vertical")
        if subregions:
            return SegmentTreeNode(
                shapes, [self._segment_region(subregion) for subregion in subregions]
            )

        # No further division possible, return a leaf node
        return SegmentTreeNode(shapes)

    def _try_split(self, shapes: list[Shape], direction: str) -> list:
        # Define grid lines based on direction
        grid_lines = self._define_grid_lines(shapes, direction)

        for line in grid_lines:
            if direction == "horizontal":
                top, bottom = self._split_by_line(shapes, line, direction)
                if top and bottom and self._valid_split(top, bottom):
                    return [top, bottom]
            elif direction == "vertical":
                left, right = self._split_by_line(shapes, line, direction)
                if left and right and self._valid_split(left, right):
                    return [left, right]

        return []

    def _define_grid_lines(self, shapes: list, direction: str) -> list:
        if direction == "horizontal":
            # Collect unique y-positions (top and bottom boundaries) of each element
            y_positions = set()
            for shape in shapes:
                y_positions.add(
                    unit_conversion(shape.top, self._measurement_unit)
                )  # Top boundary
                y_positions.add(
                    unit_conversion(shape.top + shape.height, self._measurement_unit)
                )  # Bottom boundary
            return sorted(y_positions)

        elif direction == "vertical":
            # Collect unique x-positions (left and right boundaries) of each element
            x_positions = set()
            for shape in shapes:
                x_positions.add(unit_conversion(shape.left, self._measurement_unit))
                x_positions.add(
                    unit_conversion(shape.left + shape.width, self._measurement_unit)
                )
            return sorted(x_positions)

        else:
            raise ValueError(f"Invalid direction: {direction}")

    def _valid_split(self, group1: list[Shape], group2: list[Shape]) -> bool:
        """
        Ensures that the split is meaningful, i.e., both groups are non-empty and
        do not contain any overlapping shapes with each other.
        """
        # Ensure that both groups are non-empty
        if not group1 or not group2:
            return False

        # Ensure there are no shapes overlapping between the groups
        for shape1 in group1:
            for shape2 in group2:
                if self._shapes_overlap(shape1, shape2):
                    return False

        return True

    def _shapes_overlap(self, shape1: Shape, shape2: Shape) -> bool:
        """
        Returns True if two shapes overlap, False otherwise.
        This can be defined as any type of intersection (e.g., bounding box overlap).
        """
        return not (
            shape1.left + shape1.width <= shape2.left
            or shape1.left >= shape2.left + shape2.width
            or shape1.top + shape1.height <= shape2.top
            or shape1.top >= shape2.top + shape2.height
        )

    def _split_by_line(self, shapes: list[Shape], line: float, direction: str) -> tuple:
        if direction == "horizontal":
            top = [
                shape
                for shape in shapes
                if unit_conversion(shape.top, self._measurement_unit) < line
            ]
            bottom = [
                shape
                for shape in shapes
                if unit_conversion(shape.top + shape.height, self._measurement_unit)
                >= line
            ]
            return top, bottom
        if direction == "vertical":
            left = [
                shape
                for shape in shapes
                if unit_conversion(shape.left, self._measurement_unit) < line
            ]
            right = [
                shape
                for shape in shapes
                if unit_conversion(shape.left + shape.width, self._measurement_unit)
                >= line
            ]
            return left, right
        raise ValueError(f"Invalid direction: {direction}")
