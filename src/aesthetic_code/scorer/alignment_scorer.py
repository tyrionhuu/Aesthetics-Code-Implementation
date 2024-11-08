from aesthetic_code.segmenter.segmenter import SegmentTreeNode


class AlignmentScorer:
    def __init__(
        self,
        segment_node1: SegmentTreeNode,
        segment_node2: SegmentTreeNode,
    ):
        self._segment_node1 = segment_node1
        self._segment_node2 = segment_node2

    def score(self) -> float:
        """
        Returns a score for the alignment of two segment nodes.
        """
        return self._score_alignment(self._segment_node1, self._segment_node2)

    def _score_alignment(
        self, segment_node1: SegmentTreeNode, segment_node2: SegmentTreeNode
    ) -> float:
        """
        Returns a score for the alignment of two segment nodes.
        """
        # If the two nodes are not aligned, return 0
        top_segment_node1 = segment_node1.bounding_box["top"]
        bottom_segment_node1 = segment_node1.bounding_box["bottom"]
        left_segment_node1 = segment_node1.bounding_box["left"]
        right_segment_node1 = segment_node1.bounding_box["right"]

        top_segment_node2 = segment_node2.bounding_box["top"]
        bottom_segment_node2 = segment_node2.bounding_box["bottom"]
        left_segment_node2 = segment_node2.bounding_box["left"]
        right_segment_node2 = segment_node2.bounding_box["right"]

        score = 0.0

        if (
            top_segment_node1 == top_segment_node2
            and bottom_segment_node1 == bottom_segment_node2
        ):
            score += 1.0
        elif (
            left_segment_node1 == left_segment_node2
            and right_segment_node1 == right_segment_node2
        ):
            score += 1.0

        return score
