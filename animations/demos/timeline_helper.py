"""
This script is used to assist in the creation of a timeline of events.
"""

from dataclasses import dataclass
from typing import List as ListType, Union as UnionType

from manim import *

from animations.beamer.presentation.introduction.proposal import proposal
from animations.beamer.slides import PromptSlide
from animations.demos.people.aristotle import Aristotle
from animations.demos.people.bertrand_russell import BertrandRussellQuote
from animations.demos.people.einstein import EinsteinQuote
from animations.demos.people.max_black import MaxBlack
from animations.demos.people.plato import PlatoTheoryOfForms
from animations.demos.ww2 import CaptionedSVG
from animations.beamer.presentation.introduction.dnn import (
    pros_and_cons as dnn_pros_and_cons,
)
from animations.beamer.presentation.introduction.nfn import (
    pros_and_cons as nfn_pros_and_cons,
)
from soft.utilities.reproducibility import path_to_project_root


@dataclass
class TimelineEvent:
    start_year: int  # e.g. 2015
    end_year: int  # e.g. 2025
    era: str  # e.g. Ancient Greece
    era_notation: str  # e.g. BCE, CE
    event: str  # e.g. The birth of the internet
    animation: UnionType[Scene, MovingCameraScene]
    poi: int = None  # e.g. 2020,  A specific year of interest
    skip: bool = (
        False  # skip this event, if True, event is still drawn but not focused on
    )


def make_ww2_slide(file_name: str, poi: int, caption: str) -> TimelineEvent:
    return TimelineEvent(
        start_year=1939,
        end_year=1945,
        era="Common Era",
        era_notation="CE",
        event="World War II",
        animation=CaptionedSVG(
            path=path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "ww2"
            / f"{file_name}.svg",
            caption=caption,
        ),
        poi=poi,
        skip=True,
    )


def get_noteworthy_events() -> ListType:
    return [
        dnn_pros_and_cons(),
        PromptSlide(prompt="Could we have done better?", skip=True),
        nfn_pros_and_cons(),
        proposal(),
        PromptSlide(prompt='But before we begin - what does "fuzzy" mean?', skip=True),
        PromptSlide(prompt="And do we even need it?", skip=True),
        # TimelineEvent(
        #     start_year=470,
        #     end_year=399,
        #     era="Ancient Greece",
        #     era_notation="BCE",
        #     event="Socrates",
        #     animation=Socrates,
        # ),
        TimelineEvent(
            start_year=427,
            end_year=348,
            era="Ancient Greece",
            era_notation="BCE",
            event="Plato",
            animation=PlatoTheoryOfForms,
        ),
        TimelineEvent(
            start_year=384,
            end_year=322,
            era="Ancient Greece",
            era_notation="BCE",
            event="Aristotle",
            animation=Aristotle,
        ),
        TimelineEvent(
            start_year=1879,
            end_year=1955,
            poi=1921,  # the year of the quote
            era="Common Era",
            era_notation="CE",
            event="Albert Einstein",
            animation=EinsteinQuote,
        ),
        TimelineEvent(
            start_year=1872,
            end_year=1970,
            poi=1923,  # the year of the quote (Vagueness)
            era="Common Era",
            era_notation="CE",
            event="Bertrand Russell",
            animation=BertrandRussellQuote,
        ),
        TimelineEvent(
            start_year=1909,
            end_year=1988,
            poi=1937,
            era="Common Era",
            era_notation="CE",
            event="Max Black",
            animation=MaxBlack,
        ),
        make_ww2_slide(
            "germans_in_poland_1939",
            1939,
            caption="Nazi Germany invades Poland (September 1, 1939).",
        ),
        make_ww2_slide(
            "first_mass_bombing_in_london_sept_7_1940",
            1940,
            caption="First mass bombing in London (September 7, 1940).",
        ),
        make_ww2_slide(
            "germans_attack_soviets_eastern_front_june_22_1941",
            1941,
            "Germans attack Soviets on the Eastern Front (June 22, 1941).",
        ),
        make_ww2_slide(
            "pearl_harbor_dec_7_1941",
            1941,
            "Pearl Harbor attacked by Japan (December 7, 1941).",
        ),
        make_ww2_slide(
            "soviet_offensive_against_germans_in_stalingrad_feb_1943",
            1942,
            "Battle of Stalingrad (August 23, 1942).",
        ),
        make_ww2_slide(
            "d_day_june_6_1944",
            1944,
            "D-Day: Allied invasion of Normandy (June 6, 1944).",
        ),
        make_ww2_slide(
            "nagasaki_aug_9_1945", 1945, "Nagasaki bombed by the US (August 9, 1945)."
        ),
    ]
