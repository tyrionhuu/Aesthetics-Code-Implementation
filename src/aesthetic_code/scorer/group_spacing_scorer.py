from typing import TypeAlias, Union, cast

from pptx.shapes.autoshape import Shape as AutoShape
from pptx.shapes.base import BaseShape
from pptx.shapes.connector import Connector
from pptx.shapes.graphfrm import GraphicFrame
from pptx.shapes.group import GroupShape
from pptx.shapes.picture import Movie, Picture
from pptx.shapes.placeholder import BasePlaceholder

from aesthetic_code.segmenter.segmenter import SegmentTreeNode
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

Subregion: TypeAlias = Union[Shape, "SegmentTreeNode"]


class GroupSpacingScorer:
    """
    This class is responsible for scoring the white space between groups of shapes on a slide.
    It evaluates the vertical and horizontal spacing between groups of elements and assigns a score.
    """

    def __init__(
        self,
        segment_tree: SegmentTreeNode,
        spacing_threshold: list[float] = [0.1, 0.3],
        unit_measurement: str = "pt",
    ):
        self._segment_tree = segment_tree
        self._neighbor_pairs = self._get_all_neighbor_pairs(segment_tree)
        self._spacing_threshold = spacing_threshold
        self._unit_measurement = unit_measurement

    @property
    def spacing_threshold(self) -> list[float]:
        return self._spacing_threshold

    @spacing_threshold.setter
    def spacing_threshold(self, value: list[float]):
        self._spacing_threshold = value

    @property
    def unit_measurement(self) -> str:
        return self._unit_measurement

    @unit_measurement.setter
    def unit_measurement(self, value: str):
        self._unit_measurement = value

    def _get_all_neighbor_pairs(
        self,
        node: SegmentTreeNode,
    ) -> list[tuple[str, Subregion, Subregion]]:
        """
        Get all pairs of neighboring subregions in the segment tree.
        The segment tree is a binary tree.
        get all (left child, parent), (right child, parent), (left child, right child) pairs
        """
        directions = ["belongs_to", "horizontal", "vertical"]
        pairs: list[tuple[str, Subregion, Subregion]] = []
        if node.is_leaf():
            return pairs

        if node.subregions[0]:
            pairs.append((directions[0], node.subregions[0], node))
            if isinstance(node.subregions[0], SegmentTreeNode):
                pairs.extend(
                    self._get_all_neighbor_pairs(
                        cast(SegmentTreeNode, node.subregions[0])
                    )
                )
        if node.subregions[1]:
            pairs.append((directions[0], node.subregions[1], node))
            if isinstance(node.subregions[1], SegmentTreeNode):
                pairs.extend(
                    self._get_all_neighbor_pairs(
                        cast(SegmentTreeNode, node.subregions[1])
                    )
                )
        if node.subregions[0] and node.subregions[1]:
            pairs.append((node.direction, node.subregions[0], node.subregions[1]))

        return pairs

    def score(self) -> float:
        """
        Calculate the overall white space score for the segment tree.
        The score is based on the spacing between the groups of shapes.
        """
        scores = []
        for pair in self._neighbor_pairs:
            scores.append(self._score_pair(pair))

        return sum(scores) / len(scores)

    def _score_pair(self, pair: tuple[str, Subregion, Subregion]) -> float:
        """
        Calculate the white space score between two subregions.
        The score is based on the spacing between the two subregions.
        """
        direction, subregion1, subregion2 = pair
        if direction == "vertical":
            return self._score_horizontal_spacing(subregion1, subregion2)
        elif direction == "horizontal":
            return self._score_vertical_spacing(subregion1, subregion2)
        else:
            return self._score_segment_spacing(subregion1, subregion2)

    def _score_segment_spacing(
        self, subregion1: Subregion, subregion2: Subregion
    ) -> float:
        """
        Calculate the white space score between two subregions that are not directly adjacent.
        The score is based on the spacing between the two subregions.
        """

        assert isinstance(subregion2, SegmentTreeNode)
        if isinstance(subregion1, SegmentTreeNode):
            subregion = cast(SegmentTreeNode, subregion1)
            right_subregion1 = subregion.bounding_box["right"]
            left_subregion1 = subregion.bounding_box["left"]
        else:
            shape = cast(Shape, subregion1)
            right_subregion1 = unit_conversion(
                shape.left, self._unit_measurement
            ) + unit_conversion(shape.width, self._unit_measurement)
            left_subregion1 = unit_conversion(shape.left, self._unit_measurement)

        if right_subregion1 <= subregion2.bounding_box["left"]:
            spacing = subregion2.bounding_box["left"] - right_subregion1
        elif subregion2.bounding_box["right"] <= left_subregion1:
            spacing = left_subregion1 - subregion2.bounding_box["right"]
        else:
            return 0.0

        if (
            spacing <= self._spacing_threshold[0]
            or spacing >= self._spacing_threshold[1]
        ):
            return 0.0
        else:
            return 1.0

    def _score_horizontal_spacing(
        self, subregion1: Subregion, subregion2: Subregion
    ) -> float:
        """
        Calculate the white space score between two subregions in the horizontal direction.
        The score is based on the horizontal spacing between the two subregions.
        """
        if isinstance(subregion1, SegmentTreeNode):
            subregion = cast(SegmentTreeNode, subregion1)
            right_subregion1 = subregion.bounding_box["right"]
            left_subregion1 = subregion.bounding_box["left"]
        else:
            shape = cast(Shape, subregion1)
            right_subregion1 = unit_conversion(
                shape.left, self._unit_measurement
            ) + unit_conversion(shape.width, self._unit_measurement)
            left_subregion1 = unit_conversion(shape.left, self._unit_measurement)

        if isinstance(subregion2, SegmentTreeNode):
            subregion = cast(SegmentTreeNode, subregion2)
            right_subregion2 = subregion.bounding_box["right"]
            left_subregion2 = subregion.bounding_box["left"]
        else:
            shape = cast(Shape, subregion2)
            right_subregion2 = unit_conversion(
                shape.left, self._unit_measurement
            ) + unit_conversion(shape.width, self._unit_measurement)
            left_subregion2 = unit_conversion(shape.left, self._unit_measurement)

        if right_subregion1 <= left_subregion2:
            spacing = left_subregion2 - right_subregion1
        elif right_subregion2 <= left_subregion1:
            spacing = left_subregion1 - right_subregion2
        else:
            raise ValueError("Overlapping subregions in horizontal spacing calculation")

        if (
            spacing <= self._spacing_threshold[0]
            or spacing >= self._spacing_threshold[1]
        ):
            return 0.0
        else:
            return 1.0

    def _score_vertical_spacing(
        self, subregion1: Subregion, subregion2: Subregion
    ) -> float:
        """
        Calculate the white space score between two subregions in the vertical direction.
        The score is based on the vertical spacing between the two subregions.
        """
        if isinstance(subregion1, SegmentTreeNode):
            subregion = cast(SegmentTreeNode, subregion1)
            bottom_subregion1 = subregion.bounding_box["bottom"]
            top_subregion1 = subregion.bounding_box["top"]
        else:
            shape = cast(Shape, subregion1)
            bottom_subregion1 = unit_conversion(
                shape.top, self._unit_measurement
            ) + unit_conversion(shape.height, self._unit_measurement)
            top_subregion1 = unit_conversion(shape.top, self._unit_measurement)

        if isinstance(subregion2, SegmentTreeNode):
            subregion = cast(SegmentTreeNode, subregion2)
            bottom_subregion2 = subregion.bounding_box["bottom"]
            top_subregion2 = subregion.bounding_box["top"]
        else:
            shape = cast(Shape, subregion2)
            bottom_subregion2 = unit_conversion(
                shape.top, self._unit_measurement
            ) + unit_conversion(shape.height, self._unit_measurement)
            top_subregion2 = unit_conversion(shape.top, self._unit_measurement)

        if bottom_subregion1 <= top_subregion2:
            spacing = top_subregion2 - bottom_subregion1
        elif bottom_subregion2 <= top_subregion1:
            spacing = top_subregion1 - bottom_subregion2
        else:
            raise ValueError("Overlapping subregions in vertical spacing calculation")

        if (
            spacing <= self._spacing_threshold[0]
            or spacing >= self._spacing_threshold[1]
        ):
            return 0.0
        else:
            return 1.0
