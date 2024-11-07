# from pptx.util import Pt
# from pptx import Presentation
# from aesthetic_code.scorer.group_spacing_scorer import GroupSpacingScorer
# from aesthetic_code.segmenter.segmenter import SegmentTreeNode

# # Test case 1: No shapes
# def test_empty_segment_tree():
#     # Create an empty segment tree (no shapes)
#     segment_tree = SegmentTreeNode()

#     # Create a scorer instance
#     scorer = GroupSpacingScorer(segment_tree)

#     # The score should be 0 as there are no shapes
#     assert scorer.score() == 0.0

# # Test case 2: Two groups of shapes with some spacing
# def test_two_groups_with_spacing():
#     # Create a presentation object
#     ppt = Presentation()

#     # Add slide
#     slide = ppt.slides.add_slide(ppt.slide_layouts[5])  # Blank slide layout

#     # Create some real shapes for the groups (e.g., rectangles)
#     shape1 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(0),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape2 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(0),
#         top=Pt(120),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape3 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(200),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape4 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(200),
#         top=Pt(120),
#         width=Pt(100),
#         height=Pt(100),
#     )

#     # Create segment nodes for the two groups
#     group1 = SegmentTreeNode([shape1, shape2])
#     group2 = SegmentTreeNode([shape3, shape4])

#     # Create a root node with both groups as subregions
#     segment_tree = SegmentTreeNode([], [group1, group2])

#     # Create a scorer instance
#     scorer = GroupSpacingScorer(segment_tree)

#     # The score should consider the vertical gap between group1 and group2
#     # The vertical distance is at least 20 (120 - 100), so the score should reflect that
#     assert scorer.score() > 0.0


# # Test case 3: Groups with no spacing (touching)
# def test_no_spacing_between_groups():
#     # Create a presentation object
#     ppt = Presentation()

#     # Add slide
#     slide = ppt.slides.add_slide(ppt.slide_layouts[5])  # Blank slide layout

#     # Create some real shapes for the groups with no gap between them
#     shape1 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(0),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape2 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(0),
#         top=Pt(100),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape3 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(200),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape4 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(200),
#         top=Pt(100),
#         width=Pt(100),
#         height=Pt(100),
#     )

#     # Create segment nodes for the two groups
#     group1 = SegmentTreeNode([shape1, shape2])
#     group2 = SegmentTreeNode([shape3, shape4])

#     # Create a root node with both groups as subregions
#     segment_tree = SegmentTreeNode([], [group1, group2])

#     # Create a scorer instance
#     scorer = GroupSpacingScorer(segment_tree)

#     # The score should be 0 as the groups are directly adjacent (no gap)
#     assert scorer.score() == 0.0


# # Test case 4: Multiple subregions with mixed spacing
# def test_multiple_subregions():
#     # Create a presentation object
#     ppt = Presentation()

#     # Add slide
#     slide = ppt.slides.add_slide(ppt.slide_layouts[5])  # Blank slide layout

#     # Create mock shapes for three subregions
#     shape1 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(0),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape2 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(10),
#         top=Pt(110),
#         width=Pt(110),
#         height=Pt(110),
#     )
#     shape3 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(200),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape4 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(220),
#         top=Pt(120),
#         width=Pt(120),
#         height=Pt(120),
#     )
#     shape5 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(400),
#         top=Pt(0),
#         width=Pt(100),
#         height=Pt(100),
#     )
#     shape6 = slide.shapes.add_shape(
#         autoshape_type_id=1,  # msoShapeRectangle
#         left=Pt(430),
#         top=Pt(130),
#         width=Pt(130),
#         height=Pt(130),
#     )

#     # Create segment nodes for the three groups
#     group1 = SegmentTreeNode([shape1, shape2])
#     group2 = SegmentTreeNode([shape3, shape4])
#     group3 = SegmentTreeNode([shape5, shape6])

#     # Create a root node with all three groups as subregions
#     segment_tree = SegmentTreeNode([], [group1, group2, group3])

#     # Create a scorer instance
#     scorer = GroupSpacingScorer(segment_tree)

#     # The score will depend on the gaps between the groups
#     assert scorer.score() > 0.0  # There is some spacing between the groups
