from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_ASSETS = [
    {
        "id": "hoodie-front",
        "filename": "v1_1_front_1.webp",
        "role": "secondary_full_body_outfit_anchor",
        "orientation_state": "front_view_character_left_is_viewer_right",
    },
    {
        "id": "base-front",
        "filename": "v1_1_front_2.webp",
        "role": "base_body_outfit_anchor",
        "orientation_state": "front_view_character_left_is_viewer_right",
    },
    {
        "id": "expression-sheet",
        "filename": "v1_1_front_3.webp",
        "role": "primary_face_hair_identity_anchor",
        "orientation_state": "expression_grid_unmirrored",
    },
    {
        "id": "hoodie-back",
        "filename": "v1_1_back.webp",
        "role": "back_turnaround_anchor",
        "orientation_state": "back_view_unmirrored",
    },
    {
        "id": "side-view",
        "filename": "v1_1_真横.webp",
        "role": "side_turnaround_anchor",
        "orientation_state": "side_view_unmirrored",
    },
    {
        "id": "hairpin-side-45",
        "filename": "v1_1_髪飾り側_45deg.webp",
        "role": "hairpin_side_turnaround_anchor",
        "orientation_state": "hairpin_side_45_unmirrored",
    },
    {
        "id": "non-hairpin-side-45",
        "filename": "v1_1_非髪飾り側45deg.webp",
        "role": "non_hairpin_side_turnaround_anchor",
        "orientation_state": "non_hairpin_side_45_unmirrored",
    },
    {
        "id": "footwear-board",
        "filename": "v1_1_standard_foot_set.webp",
        "role": "footwear_sock_reference_board",
        "orientation_state": "board_unmirrored",
    },
    {
        "id": "shoe-board",
        "filename": "v1_1_shoes.webp",
        "role": "sneaker_reference_board",
        "orientation_state": "board_unmirrored",
    },
    {
        "id": "bag-board",
        "filename": "v1_1_bag.webp",
        "role": "bag_accessory_reference_board",
        "orientation_state": "board_unmirrored",
    },
]
