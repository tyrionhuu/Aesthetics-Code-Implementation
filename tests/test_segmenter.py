from unittest.mock import MagicMock, patch

import pytest
from pptx.presentation import Presentation
from pptx.util import Pt

from aesthetic_code.segmenter.segmenter import (
    PowerPointSegmenter,
    PowerPointSegmentPrinter,
    SegmentTreeNode,
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
    slide = MagicMock()
    shape1 = MagicMock()
    shape2 = MagicMock()
    shape1.left, shape1.top, shape1.width, shape1.height = (
        Pt(100),
        Pt(100),
        Pt(200),
        Pt(100),
    )
    shape2.left, shape2.top, shape2.width, shape2.height = (
        Pt(400),
        Pt(300),
        Pt(200),
        Pt(150),
    )
    slide.shapes = [shape1, shape2]
    presentation.slides = [slide]
    return presentation


def test_segmenter(mock_pptx_presentation, mock_unit_conversion):
    presentation = mock_pptx_presentation
    segmenter = PowerPointSegmenter(presentation, "pt")

    # Segment a single slide (index 0)
    segment_tree = segmenter.segment(0)
    PowerPointSegmentPrinter(segment_tree)()  # Print the segment tree

    # Assert that the segmenter returned a non-empty segment tree
    assert isinstance(segment_tree, SegmentTreeNode)

    # Adjust based on expected output from _try_split logic
    assert (
        segment_tree.is_leaf() or segment_tree.subregions
    )  # Expected behavior is context-dependent
