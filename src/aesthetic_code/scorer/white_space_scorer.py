from pptx.util import Length

from aesthetic_code.segmenter.segmenter import SegmentTreeNode
from aesthetic_code.utils import unit_conversion


class MarginWhiteSpaceScorer:
    """
    This class is responsible for scoring the white space in the margins of a slide.
    """

    def __init__(
        self,
        segment_tree: SegmentTreeNode,
        slide_width: Length,
        slide_height: Length,
        measurement_unit: str = "pt",
    ):
        self._segment_tree = segment_tree
        self._shapes = segment_tree.shapes
        self._measurement_unit = measurement_unit
        self._width = unit_conversion(slide_width, self._measurement_unit)
        self._height = unit_conversion(slide_height, self._measurement_unit)
        self._margin_threshold = {
            "horizontal": (0.1 * self._width, 0.3 * self._width),
            "vertical": (0.1 * self._height, 0.3 * self._height),
        }

    def _get_bounding_box(self) -> dict:
        leftmost_x = self._width
        rightmost_x = 0.0
        topmost_y = self._height
        bottommost_y = 0.0
        for shape in self._shapes:
            left = unit_conversion(shape.left, self._measurement_unit)
            top = unit_conversion(shape.top, self._measurement_unit)
            width = unit_conversion(shape.width, self._measurement_unit)
            height = unit_conversion(shape.height, self._measurement_unit)
            right = left + width
            bottom = top + height
            leftmost_x = min(leftmost_x, left)
            rightmost_x = max(rightmost_x, right)
            topmost_y = min(topmost_y, top)
            bottommost_y = max(bottommost_y, bottom)

        return {
            "left": leftmost_x,
            "right": rightmost_x,
            "top": topmost_y,
            "bottom": bottommost_y,
        }

    def _calculate_margins(self) -> dict:
        bounding_box = self._get_bounding_box()
        left_margin = bounding_box["left"]
        right_margin = self._width - bounding_box["right"]
        top_margin = bounding_box["top"]
        bottom_margin = self._height - bounding_box["bottom"]
        return {
            "left": left_margin,
            "right": right_margin,
            "top": top_margin,
            "bottom": bottom_margin,
        }

    def calculate_white_space_score(self) -> float:
        margins = self._calculate_margins()
        horizontal_margin_score = 0
        vertical_margin_score = 0
        if (
            margins["left"] >= self._margin_threshold["horizontal"][0]
            and margins["left"] <= self._margin_threshold["horizontal"][1]
        ):
            horizontal_margin_score += 1
        if (
            margins["right"] >= self._margin_threshold["horizontal"][0]
            and margins["right"] <= self._margin_threshold["horizontal"][1]
        ):
            horizontal_margin_score += 1
        if (
            margins["top"] >= self._margin_threshold["vertical"][0]
            and margins["top"] <= self._margin_threshold["vertical"][1]
        ):
            vertical_margin_score += 1
        if (
            margins["bottom"] >= self._margin_threshold["vertical"][0]
            and margins["bottom"] <= self._margin_threshold["vertical"][1]
        ):
            vertical_margin_score += 1
        return float((horizontal_margin_score + vertical_margin_score) / 4)
