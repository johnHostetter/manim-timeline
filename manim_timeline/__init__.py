from dataclasses import dataclass


@dataclass
class ItemColor:
    ACTIVE_1: str = "#FD56DC"  # hot pink
    INACTIVE_1: str = "#FFB9CB"  # light pink
    ACTIVE_2: str = "#68EF00"  # hot pink
    INACTIVE_2: str = "#01D3FC"  # light pink
    BACKGROUND: str = "#025393"  # dark blue