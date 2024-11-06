from pptx.shapes.base import BaseShape
from pptx.util import Length

# Assuming GroupSpacingWhiteSpaceScorer and SegmentTreeNode are defined in the module 'pptx_segmenter'
from aesthetic_code.scorer.group_spacing_scorer import GroupSpacingWhiteSpaceScorer
from aesthetic_code.segmenter.segmenter import SegmentTreeNode


# Mock the BaseShape class to simulate shape properties
class MockShape(BaseShape):
    def __init__(self, left: float, top: float, width: float, height: float):
        self.left = Length(left)
        self.top = Length(top)
        self.width = Length(width)
        self.height = Length(height)


# Test case 1: No shapes
def test_empty_segment_tree():
    # Create an empty segment tree (no shapes)
    segment_tree = SegmentTreeNode()

    # Create a scorer instance
    scorer = GroupSpacingWhiteSpaceScorer(segment_tree)

    # The score should be 0 as there are no shapes
    assert scorer.score() == 0.0


# Test case 2: Two groups of shapes with some spacing
def test_two_groups_with_spacing():
    # Create some mock shapes for the groups
    shape1 = MockShape(0, 0, 100, 100)
    shape2 = MockShape(
        0, 120, 100, 100
    )  # This will create a vertical gap between the two shapes
    shape3 = MockShape(200, 0, 100, 100)
    shape4 = MockShape(200, 120, 100, 100)

    # Create segment nodes for the two groups
    group1 = SegmentTreeNode([shape1, shape2])
    group2 = SegmentTreeNode([shape3, shape4])

    # Create a root node with both groups as subregions
    segment_tree = SegmentTreeNode([], [group1, group2])

    # Create a scorer instance
    scorer = GroupSpacingWhiteSpaceScorer(segment_tree)

    # The score should consider the vertical gap between group1 and group2
    # The vertical distance is at least 20 (120 - 100), so the score should reflect that
    assert scorer.score() > 0.0


# Test case 3: Groups with no spacing (touching)
def test_no_spacing_between_groups():
    # Create some mock shapes for the groups with no gap between them
    shape1 = MockShape(0, 0, 100, 100)
    shape2 = MockShape(0, 100, 100, 100)  # No gap between the two shapes
    shape3 = MockShape(200, 0, 100, 100)
    shape4 = MockShape(200, 100, 100, 100)  # No gap between the two shapes

    # Create segment nodes for the two groups
    group1 = SegmentTreeNode([shape1, shape2])
    group2 = SegmentTreeNode([shape3, shape4])

    # Create a root node with both groups as subregions
    segment_tree = SegmentTreeNode([], [group1, group2])

    # Create a scorer instance
    scorer = GroupSpacingWhiteSpaceScorer(segment_tree)

    # The score should be 0 as the groups are directly adjacent (no gap)
    assert scorer.score() == 0.0


# Test case 4: Multiple subregions with mixed spacing
def test_multiple_subregions():
    # Create mock shapes for three subregions
    shape1 = MockShape(0, 0, 100, 100)
    shape2 = MockShape(0, 100, 100, 100)
    shape3 = MockShape(200, 0, 100, 100)
    shape4 = MockShape(200, 100, 100, 100)
    shape5 = MockShape(400, 0, 100, 100)
    shape6 = MockShape(400, 100, 100, 100)

    # Create segment nodes for the three groups
    group1 = SegmentTreeNode([shape1, shape2])
    group2 = SegmentTreeNode([shape3, shape4])
    group3 = SegmentTreeNode([shape5, shape6])

    # Create a root node with all three groups as subregions
    segment_tree = SegmentTreeNode([], [group1, group2, group3])

    # Create a scorer instance
    scorer = GroupSpacingWhiteSpaceScorer(segment_tree)

    # The score will depend on the gaps between the groups
    assert scorer.score() > 0.0  # There is some spacing between the groups
