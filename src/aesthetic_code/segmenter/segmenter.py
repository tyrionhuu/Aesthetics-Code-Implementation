# from typing import TypeAlias, Union

# from asthetic_code.utils import unit_conversion
# from pptx.shapes.autoshape import Shape as AutoShape
# from pptx.shapes.base import BaseShape
# from pptx.shapes.connector import Connector
# from pptx.shapes.graphfrm import GraphicFrame
# from pptx.shapes.group import GroupShape
# from pptx.shapes.picture import Movie, Picture
# from pptx.shapes.placeholder import BasePlaceholder
# from pptx.util import Length

# Shape: TypeAlias = Union[
#     BaseShape,
#     AutoShape,
#     Connector,
#     GraphicFrame,
#     GroupShape,
#     Picture,
#     Movie,
#     BasePlaceholder,
# ]

# class SegmentTreeNode:
#     def __init__(self, shapes: list[Shape], subregions=None):
#         self._shapes = shapes      # List of shapes in this region
#         self._subregions = subregions if subregions is not None else []

#     def is_leaf(self):
#         return len(self._subregions) == 0

# class Segmenter:
#     def __init__(self, shapes: list[Shape], slide_width: Length, slide_height: Length, measurement_unit: str = "pt"):
#         self._shapes = shapes
#         self._measurement_unit = measurement_unit
#         self._slide_width = unit_conversion(slide_width, self._measurement_unit)
#         self._slide_height = unit_conversion(slide_height, self._measurement_unit)

#     def segment(self) -> SegmentTreeNode:
#         return self._segment_region(self._shapes)

#     def _segment_region(self, shapes: list[Shape]) -> SegmentTreeNode:
#         # Try to split with horizontal line
#         subregions = self._try_split(shapes, "horizontal")
#         if subregions:
#             return SegmentTreeNode(shapes, [self._segment_region(subregion) for subregion in subregions])

#         # If horizontal split is not possible, try vertical grid lines
#         subregions = self._try_split(shapes, "vertical")
#         if subregions:
#             return SegmentTreeNode(shapes, [self._segment_region(subregion) for subregion in subregions])

#         # No further division possible, return a leaf node
#         return SegmentTreeNode(shapes)

#     def _try_split(self, shapes: list[Shape], direction: str) -> list:
#         # Define grid lines based on direction
#         grid_lines = self._define_grid_lines(direction)

#         for line in grid_lines:
#             if direction == "horizontal":
#                 top, bottom = self._split_by_line(shapes, line, direction)
#                 if top and bottom:
#                     return [top, bottom]
#             elif direction == "vertical":
#                 left, right = self._split_by_line(shapes, line, direction)
#                 if left and right:
#                     return [left, right]

#         return []

#     def _define_grid_lines(self, shapes: list, direction: str) -> list:
#         if direction == "horizontal":
#             # Collect unique y-positions (top and bottom boundaries) of each element
#             y_positions = set()
#             for shape in shapes:
#                 y_positions.add(

#             return sorted(y_positions)

#         elif direction == "vertical":
#             # Collect unique x-positions (left and right boundaries) of each element
#             x_positions = set()
#             for element in shapes:
#                 x_positions.add(element["x"])  # Left boundary
#                 x_positions.add(element["x"] + element["width"])  # Right boundary
#             return sorted(x_positions)
