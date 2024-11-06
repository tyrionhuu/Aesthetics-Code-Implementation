from typing import List, Optional, TypeAlias, Union

from pptx.presentation import Presentation
from pptx.shapes.autoshape import Shape as AutoShape
from pptx.shapes.base import BaseShape
from pptx.shapes.connector import Connector
from pptx.shapes.graphfrm import GraphicFrame
from pptx.shapes.group import GroupShape
from pptx.shapes.picture import Movie, Picture
from pptx.shapes.placeholder import BasePlaceholder
from pptx.util import Length

from aesthetic_code.utils import unit_conversion

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
    def __init__(
        self,
        shapes: Optional[List[Shape]] = None,
        subregions: Optional[List["SegmentTreeNode"]] = None,
    ):
        self.shapes = (
            shapes if shapes is not None else []
        )  # List of shapes in this region
        self.subregions = subregions if subregions is not None else []

    def is_leaf(self):
        return len(self.subregions) == 0


class Segmenter:
    def __init__(
        self,
        shapes: List[Shape],
        slide_width: Length | None,
        slide_height: Length | None,
        measurement_unit: str = "pt",
    ):
        self._shapes = shapes
        self._measurement_unit = measurement_unit
        self._slide_width = unit_conversion(slide_width, self._measurement_unit)
        self._slide_height = unit_conversion(slide_height, self._measurement_unit)

    def __call__(self, *args, **kwds):
        return self.segment()

    def segment(self) -> SegmentTreeNode:
        return self._segment_region(self._shapes)

    def _segment_region(self, shapes: List[Shape]) -> SegmentTreeNode:
        if not shapes:  # If shapes list is empty, return a leaf node
            return SegmentTreeNode()

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

    def _try_split(self, shapes: List[Shape], direction: str) -> List[List[Shape]]:
        if not shapes:
            return []  # Return empty if no shapes to split

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

        return []  # Return empty if no valid split found

    def _define_grid_lines(self, shapes: List[Shape], direction: str) -> List[float]:
        if not shapes:
            return []  # Return empty list if no shapes to define grid lines

        if direction == "horizontal":
            y_positions = set()
            for shape in shapes:
                top = unit_conversion(shape.top, self._measurement_unit)
                height = unit_conversion(shape.height, self._measurement_unit)
                y_positions.add(top)
                y_positions.add(top + height)
            return sorted(y_positions)

        elif direction == "vertical":
            x_positions = set()
            for shape in shapes:
                left = unit_conversion(shape.left, self._measurement_unit)
                width = unit_conversion(shape.width, self._measurement_unit)
                x_positions.add(left)
                x_positions.add(left + width)
            return sorted(x_positions)

        else:
            raise ValueError(f"Invalid direction: {direction}")

    def _valid_split(self, group1: List[Shape], group2: List[Shape]) -> bool:
        if not group1 or not group2:
            return False

        for shape1 in group1:
            if shape1 in group2:
                return False

        # Ensure no shape is left out
        if len(group1) + len(group2) != len(self._shapes):
            return False

        return True

    def _split_by_line(self, shapes: List[Shape], line: float, direction: str) -> tuple:
        if direction == "horizontal":
            top = [
                shape
                for shape in shapes
                if unit_conversion(shape.top, self._measurement_unit) < line
            ]
            bottom = [
                shape
                for shape in shapes
                if unit_conversion(
                    Length(shape.top + shape.height), self._measurement_unit
                )
                >= line
            ]
            return top, bottom
        elif direction == "vertical":
            left = [
                shape
                for shape in shapes
                if unit_conversion(shape.left, self._measurement_unit) < line
            ]
            right = [
                shape
                for shape in shapes
                if unit_conversion(
                    Length(shape.left + shape.width), self._measurement_unit
                )
                >= line
            ]
            return left, right
        else:
            raise ValueError(f"Invalid direction: {direction}")


class PowerPointSegmenter:
    def __init__(self, presentation: Presentation, measurement_unit: str = "pt"):
        self._presentation = presentation
        self._measurement_unit = measurement_unit
        self._slide_width = presentation.slide_width
        self._slide_height = presentation.slide_height

    def segment(self, slide_index: int) -> SegmentTreeNode:
        slide = self._presentation.slides[slide_index]
        shapes = slide.shapes
        return Segmenter(
            shapes, self._slide_width, self._slide_height, self._measurement_unit
        ).segment()

    def segment_all(self) -> dict:
        return {i: self.segment(i) for i in range(len(self._presentation.slides))}


class PowerPointSegmentPrinter:
    def __init__(
        self,
        segment_tree: SegmentTreeNode,
        measurement_unit: str = "pt",
        indent_char: str = " ",
    ):
        self._segment_tree = segment_tree
        self._measurement_unit = measurement_unit
        self._indent_char = indent_char

    def __call__(self):
        return self.print_segment_tree()

    def print_segment_tree(self):
        print("Segment Tree Structure:")
        self._print_segment_tree(self._segment_tree)

    def _format_node_info(self, node: SegmentTreeNode, depth: int) -> str:
        """
        Formats information about a node for printing.
        Includes the count of shapes and depth level for clarity.
        """
        indent = self._indent_char * depth
        shape_count = len(node.shapes)
        shape_types = set(type(shape).__name__ for shape in node.shapes)
        return f"{indent}Node at depth {depth} with {shape_count} shapes ({', '.join(shape_types)})"

    def _print_segment_tree(self, node: SegmentTreeNode, depth: int = 0):
        if not node.shapes:
            print(self._format_node_info(node, depth) + " [Empty]")
            return

        print(self._format_node_info(node, depth))

        if node.is_leaf():
            print(
                f"{self._indent_char * (depth + 1)}Leaf node with {len(node.shapes)} shapes"
            )
        else:
            for subregion in node.subregions:
                self._print_segment_tree(subregion, depth + 1)
