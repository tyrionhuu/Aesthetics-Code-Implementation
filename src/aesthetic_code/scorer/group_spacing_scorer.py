from aesthetic_code.segmenter.segmenter import SegmentTreeNode


class GroupSpacingeScorer:
    """
    This class is responsible for scoring the white space between groups of shapes on a slide.
    It evaluates the vertical and horizontal spacing between groups of elements and assigns a score.
    """

    def __init__(
        self,
        segment_tree: SegmentTreeNode,
    ):
        self._segment_tree = segment_tree

    def score(self) -> float:
        """
        Calculate the overall white space score for the segment tree.
        The score is based on the spacing between the groups of shapes.
        """
        return self._score_subregions(self._segment_tree)

    def _score_subregions(self, node: SegmentTreeNode) -> float:
        """
        Recursively score the white space for each subregion of the segment tree.
        The score is calculated based on the distances between groups of shapes.
        """
        if node.is_leaf():
            return 0.0  # No space between groups in a leaf node

        total_score = 0.0
        subregion_count = len(node.subregions)

        for i, subregion in enumerate(node.subregions):
            # Score the distance between the current subregion and the next one
            if i < subregion_count - 1:
                next_subregion = node.subregions[i + 1]
                total_score += self._score_spacing_between_groups(
                    subregion, next_subregion
                )

            # Recursively score subregions within the current subregion
            total_score += self._score_subregions(subregion)

        return total_score

    def _score_spacing_between_groups(
        self, group1: SegmentTreeNode, group2: SegmentTreeNode
    ) -> float:
        """
        Calculate the score for the spacing between two groups of shapes.
        """
        # Calculate the minimum vertical and horizontal distance between groups
        vertical_distance = self._calculate_vertical_distance(group1, group2)
        horizontal_distance = self._calculate_horizontal_distance(group1, group2)

        # Combine the distances into a single score, with weights for vertical and horizontal spacing
        return vertical_distance * 0.7 + horizontal_distance * 0.3

    def _calculate_vertical_distance(
        self, group1: SegmentTreeNode, group2: SegmentTreeNode
    ) -> float:
        """
        Calculate the minimum vertical distance between two groups of shapes.
        """
        top1 = min([shape.top for shape in group1.shapes])
        bottom1 = max([shape.top + shape.height for shape in group1.shapes])
        top2 = min([shape.top for shape in group2.shapes])
        bottom2 = max([shape.top + shape.height for shape in group2.shapes])

        # Calculate vertical distance as the gap between the bottom of one group and the top of the other
        return max(0.0, min(top1, top2) - max(bottom1, bottom2))

    def _calculate_horizontal_distance(
        self, group1: SegmentTreeNode, group2: SegmentTreeNode
    ) -> float:
        """
        Calculate the minimum horizontal distance between two groups of shapes.
        """
        left1 = min([shape.left for shape in group1.shapes])
        right1 = max([shape.left + shape.width for shape in group1.shapes])
        left2 = min([shape.left for shape in group2.shapes])
        right2 = max([shape.left + shape.width for shape in group2.shapes])

        # Calculate horizontal distance as the gap between the right of one group and the left of the other
        return max(0.0, min(left1, left2) - max(right1, right2))
