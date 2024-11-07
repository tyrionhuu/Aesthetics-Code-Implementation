from typing import TypeAlias, Union, cast

from pptx.shapes.autoshape import Shape as AutoShape
from pptx.shapes.base import BaseShape
from pptx.shapes.connector import Connector
from pptx.shapes.graphfrm import GraphicFrame
from pptx.shapes.group import GroupShape
from pptx.shapes.picture import Movie, Picture
from pptx.shapes.placeholder import BasePlaceholder

from aesthetic_code.segmenter.segmenter import SegmentTreeNode

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
    ):
        self._segment_tree = segment_tree
        self._neighbor_pairs = self._get_all_neighbor_pairs(segment_tree)

    # def score(self) -> float:
    #     """
    #     Calculate the overall white space score for the segment tree.
    #     The score is based on the spacing between the groups of shapes.
    #     """
    #     return self._score_subregions(self._segment_tree)

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

    # def _score_subregions(self, node: SegmentTreeNode) -> float:
    #     """
    #     Recursively score the white space for each subregion of the segment tree.
    #     The score is calculated based on the distances between groups of shapes.
    #     """
    #     if node.is_leaf():
    #         return 0.0  # No space between groups in a leaf node

    #     total_score = 0.0
