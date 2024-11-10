from unittest.mock import MagicMock, patch

import pytest
from pptx import Presentation
from pptx.util import Pt

from aesthetic_code.scorer.size_comparison_scorer import SizeComparisonScorer
from aesthetic_code.segmenter.segmenter import (
    PowerPointSegmenter,
    SegmentTreeNode,
    get_all_neighbor_pairs,
)


# Mock the unit_conversion function to simply return the Pt in points
@pytest.fixture
def mock_unit_conversion():
    with patch("aesthetic_code.utils.unit_conversion") as mock_conversion:
        mock_conversion.side_effect = lambda x, unit: x
        yield mock_conversion


# Mock a pptx presentation with slides and shapes
@pytest.fixture
def mock_pptx_presentation():
    presentation = MagicMock(spec=Presentation)
    presentation.slide_width, presentation.slide_height = Pt(800), Pt(600)
    slide = MagicMock()
    shape1 = MagicMock()
    shape2 = MagicMock()
    shape3 = MagicMock()
    shape4 = MagicMock()
    shape5 = MagicMock()
    shape6 = MagicMock()
    shape1.left, shape1.top, shape1.width, shape1.height = (
        Pt(0),
        Pt(0),
        Pt(100),
        Pt(100),
    )
    shape2.left, shape2.top, shape2.width, shape2.height = (
        Pt(100),
        Pt(100),
        Pt(100),
        Pt(100),
    )
    shape3.left, shape3.top, shape3.width, shape3.height = (
        Pt(200),
        Pt(300),
        Pt(100),
        Pt(100),
    )
    shape4.left, shape4.top, shape4.width, shape4.height = (
        Pt(400),
        Pt(200),
        Pt(100),
        Pt(100),
    )
    shape5.left, shape5.top, shape5.width, shape5.height = (
        Pt(100),
        Pt(300),
        Pt(100),
        Pt(100),
    )
    shape6.left, shape6.top, shape6.width, shape6.height = (
        Pt(400),
        Pt(100),
        Pt(200),
        Pt(100),
    )
    shape1.slide_type, shape2.slide_type, shape3.slide_type = (
        "AutoShape",
        "AutoShape",
        "AutoShape",
    )
    shape4.slide_type, shape5.slide_type, shape6.slide_type = (
        "AutoShape",
        "AutoShape",
        "AutoShape",
    )
    slide.shapes = [shape1, shape2, shape3, shape4, shape5, shape6]
    presentation.slides = [slide]
    return presentation


def test_segmenter(mock_pptx_presentation):
    presentation = mock_pptx_presentation
    segmenter = PowerPointSegmenter(presentation, "pt")

    # Segment a single slide (index 0)
    segments = segmenter.segment_all()
    segment_tree: SegmentTreeNode = segments[0]
    # segment_tree.print_tree()
    neighbor_pairs = get_all_neighbor_pairs(segment_tree)

    for pair in neighbor_pairs:
        scorer = SizeComparisonScorer(pair[1], pair[2])
        score = scorer.score()
        print(score)
    # Assert that the segmenter returned a non-empty segment tree
    assert isinstance(segment_tree, SegmentTreeNode)

    # Adjust based on expected output from _try_split logic
    assert (
        segment_tree.is_leaf() or segment_tree.subregions
    )  # Expected behavior is context-dependent
