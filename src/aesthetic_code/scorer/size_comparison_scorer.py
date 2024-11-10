from aesthetic_code.segmenter.segmenter import SegmentTreeNode


class SizeComparisonScorer:
    def __init__(
        self,
        segment_node1: SegmentTreeNode,
        segment_node2: SegmentTreeNode,
        thresholds: tuple = (0.25, 4),
    ):
        self._segment_node1 = segment_node1
        self._segment_node2 = segment_node2
        self._thresholds = thresholds

    def get_width(self, segment_node: SegmentTreeNode) -> float:
        return segment_node.bounding_box["right"] - segment_node.bounding_box["left"]

    def get_height(self, segment_node: SegmentTreeNode) -> float:
        return segment_node.bounding_box["bottom"] - segment_node.bounding_box["top"]

    def score(self) -> float:
        """
        Returns a score for the size comparison of two segment nodes.
        """
        return self._score_size_comparison(self._segment_node1, self._segment_node2)

    def _score_size_comparison(
        self, segment_node1: SegmentTreeNode, segment_node2: SegmentTreeNode
    ) -> float:
        """
        Returns a score for the size comparison of two segment nodes.
        """
        width_segment_node1 = self.get_width(segment_node1)
        height_segment_node1 = self.get_height(segment_node1)

        width_segment_node2 = self.get_width(segment_node2)
        height_segment_node2 = self.get_height(segment_node2)

        score = 0.0

        if (
            width_segment_node1 / width_segment_node2 >= self._thresholds[0]
            and width_segment_node1 / width_segment_node2 <= self._thresholds[1]
        ):
            score += 0.5

        if (
            height_segment_node1 / height_segment_node2 >= self._thresholds[0]
            and height_segment_node1 / height_segment_node2 <= self._thresholds[1]
        ):
            score += 0.5

        return score
