"""
This script is used to assist in the creation of a timeline of events.
"""

from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.presentation.conclusion.existing_issues import curr_limitations
from animations.beamer.presentation.conclusion.new_horizons import proposed_studies
from animations.beamer.presentation.conclusion.plan import proposed_plan
from animations.beamer.presentation.introduction.linguistics import define_linguistics
from animations.beamer.slides import PromptSlide
from animations.demos.methods.clip import CLIPDemo
from animations.demos.methods.cql import CQLDemo
from animations.demos.methods.ecm import ECMDemo
from animations.demos.people.aristotle import Aristotle
from animations.demos.people.bertrand_russell import BertrandRussellQuote
from animations.demos.people.einstein import EinsteinQuote
from animations.demos.people.godel import GodelQuote
from animations.demos.people.lukasiewicz import Lukasiewicz
from animations.demos.people.max_black import MaxBlack
from animations.demos.people.plato import PlatoTheoryOfForms
from animations.demos.people.zadeh import Zadeh
from animations.demos.timeline_helper import TimelineEvent
from animations.demos.ww2 import CaptionedSVG, CaptionedJPG
from soft.utilities.reproducibility import path_to_project_root


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


def get_historical_context() -> list:
    return [
        # dnn_pros_and_cons(),
        # PromptSlide(prompt="Could we have done better?", skip=True),
        # nfn_pros_and_cons(),
        # proposal(),
        # PromptSlide(prompt='But before we begin - what does "fuzzy" mean?', skip=True),
        # # PromptSlide(prompt="And do we even need it?", skip=True),
        # # TimelineEvent(
        # #     start_year=470,
        # #     end_year=399,
        # #     era="Ancient Greece",
        # #     era_notation="BCE",
        # #     event="Socrates",
        # #     animation=Socrates,
        # # ),
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
            start_year=1878,
            end_year=1956,
            poi=1921,
            era="Common Era",
            era_notation="CE",
            event="Jan Łukasiewicz",
            animation=Lukasiewicz,
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
            start_year=1906,
            end_year=1978,
            poi=1932,  # Gödel-Dummett logic
            era="Common Era",
            era_notation="CE",
            event="Kurt Gödel",
            animation=GodelQuote,
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
        TimelineEvent(
            start_year=1921,
            end_year=2017,
            poi=1965,
            era="Common Era",
            era_notation="CE",
            event="Lotfi A. Zadeh",
            animation=Zadeh,
        ),
    ]


def from_zadeh_to_nfn():
    bib_manager = BibTexManager()
    return [
        bib_manager.cite_entry(bib_manager["zadeh_fuzzy_sets"]),  # 1965
        bib_manager.cite_entry(bib_manager["fuzzy_dp"]),  # 1970
        # mamdani FLC
        bib_manager.cite_entry(bib_manager["Mamdani1974ApplicationsOF"]),
        # relationship to lukasiewicz logic
        bib_manager.cite_entry(bib_manager["giles1976lukasiewicz"]),
        # online
        # bib_manager.cite_entry(bib_manager["barto_neuronlike_1983"]),
        # fuzzy logic formalized by zadeh
        bib_manager.cite_entry(bib_manager["fuzzy_logic"]),  # 1988
        define_linguistics(),
        # possibly first NFN?
        bib_manager.cite_entry(bib_manager["lin_neural-network-based_1991"]),  # 1991
    ]


def from_nfn_to_wang_mendel():
    """
    Pick up from the first NFN and move to the Wang-Mendel method.

    Returns:

    """
    bib_manager = BibTexManager()
    return [
        # online fuzzy RL
        {
            "Online Fuzzy\nReinforcement\nLearning": [
                bib_manager.cite_entry(bib_manager["aric_1"]),  # 1991
                bib_manager.cite_entry(bib_manager["berenji_learning_1992"]),  # 1991
            ]
        },
        # Q-learning
        bib_manager.cite_entry(bib_manager["Watkins1992"]),  # 1992
        # Wang-Mendel Method for fuzzy logic rules
        bib_manager.cite_entry(bib_manager["wang_generating_1992"]),  # 1992
    ]


def from_wang_mendel_to_apfrb():
    """
    Pick up from the Wang-Mendel method and move to my APFRB study.

    Returns:

    """
    bib_manager = BibTexManager()
    return [
        # defend fuzzy logic
        {
            "FLCs are\nuniversal function\napproximators": [
                bib_manager.cite_entry(
                    bib_manager["wang_mendel_universal_function_approx"]
                ),
                # 1992
                bib_manager.cite_entry(
                    bib_manager["wang_universal_function_approx"]
                ),  # 1992
            ],
        },
        # ANFIS
        bib_manager.cite_entry(bib_manager["jang_anfis_1993"]),  # 1993
        # self-organize NFNs
        bib_manager.cite_entry(bib_manager["chen_self-organizing_1993"]),  # 1993
        bib_manager.cite_entry(
            bib_manager["lin_reinforcement_1994"]
        ),  # 1994 Lin does RL
        bib_manager.cite_entry(
            bib_manager["fql_and_dynamic_fql"]
        ),  # 1994 first FQL paper
        bib_manager.cite_entry(bib_manager["elkan_paradoxical_1994"]),
        # 1994 (defend f.l. w/ berenji & zadeh)
        {
            "Additional proof\nFLCs are universal\nfunction approximators": [
                bib_manager.cite_entry(bib_manager["kosko_1994"]),  # 1994
                bib_manager.cite_entry(bib_manager["zeng_approximation_1995"]),  # 1995
            ],
        },
        # self-organize
        bib_manager.cite_entry(bib_manager["zhou_popfnn_1996"]),  # 1996 first POPFNN
        # broader applications
        bib_manager.cite_entry(bib_manager["zadeh_fuzzy_1996"]),  # zadeh's CWW
        bib_manager.cite_entry(
            bib_manager["glorennec_fuzzy_1997"]
        ),  # 1997 fuzzy q-learning
        bib_manager.cite_entry(bib_manager["are_ann_black_boxes"]),  # 1997
        bib_manager.cite_entry(bib_manager["tfig"]),  # 1997
        bib_manager.cite_entry(bib_manager["kosko_blue_book"]),  # 1998 kosko
        bib_manager.cite_entry(
            bib_manager["jouffe_fuzzy_1998"]
        ),  # 1998 fuzzy actor critic
        bib_manager.cite_entry(
            bib_manager["lin_granular_1999"]
        ),  # 1999 zadeh w/ Kacprzyk, Janusz
        bib_manager.cite_entry(
            bib_manager["quek_popfnn-aars_1999"]
        ),  # 1999 POPFNN-AARS
        # equivalence to ANNs/DNNs
        {
            "FLCs are\nmathematically \nequivalent\nto ANNs/DNNs": [
                bib_manager.cite_entry(bib_manager["fls_ann_equivalence"]),  # 2000
                bib_manager.cite_entry(bib_manager["black_box_ext"]),  # 2002
            ],
        },
        # DENFIS
        bib_manager.cite_entry(bib_manager["kasabov_denfis_2002"]),  # 2002
        ECMDemo(),
        # bib_manager.cite_entry(bib_manager["equivalence_implications"]),  # 2003
        # bib_manager.cite_entry(bib_manager["ang_popfnn-cris_2003"]),  # 2003 update to POPFNN
        bib_manager.cite_entry(bib_manager["are_ann_white_boxes"]),  # 2005
        # rough set w/ NFN
        {
            "Rough set theory\n with NFN": [
                bib_manager.cite_entry(bib_manager["ang_rspop_2005"]),  # 2005
                bib_manager.cite_entry(bib_manager["ang_stock_2006"]),  # 2006
            ]
        },
        # return to CWW
        # bib_manager.cite_entry(bib_manager["mendel_computing_2007"]),  # argues CWW to be embraced
        bib_manager.cite_entry(bib_manager["is_there_a_need_for_fuzzy_logic"]),  # 2008
        # genetic fuzzy systems for high dimensions
        bib_manager.cite_entry(bib_manager["gacto_handling_2009"]),  # 2009
        bib_manager.cite_entry(
            bib_manager["kacprzyk_computing_2010"]
        ),  # 2010 CWW is implementable
        # CLIP
        bib_manager.cite_entry(bib_manager["tung_safin_2011"]),  # 2011
        CLIPDemo(),
        # bib_manager.cite_entry(bib_manager["wiering_batch_2012"]),  # 2012, batch RL
        # genetic fuzzy systems for high dimensions
        bib_manager.cite_entry(bib_manager["marquez_efficient_2012"]),  # 2012
        # DENFIS for RL
        bib_manager.cite_entry(bib_manager["denfis_rl"]),  # 2014
        # update rough set w/ NFN
        bib_manager.cite_entry(bib_manager["das_ierspop_2016"]),  # 2016 incremental NFN
        # first offline (model-based) fuzzy RL
        bib_manager.cite_entry(bib_manager["hein_particle_2017"]),  # 2017
        # people begin noticing f.l. can help w/ XAI
        {
            "Zadeh begins to \nbe recognized for \nhis XAI efforts": [
                bib_manager.cite_entry(
                    bib_manager["hagras_towards_nodate"]
                ),  # 2018, f.l. for XAI
                bib_manager.cite_entry(
                    bib_manager["pierrard_learning_2018"]
                ),  # 2018, f.l. for XAI
                bib_manager.cite_entry(bib_manager["mencar_paving_2019"]),
                bib_manager.cite_entry(bib_manager["arrieta_explainable_2019"]),
            ],
        },
        bib_manager.cite_entry(bib_manager["aghaeipoor_mokblmoms_2019"]),
        # # offline RL focus
        # # {
        # #     "Offline \nReinforcement \nLearning": [
        # #         bib_manager.cite_entry(bib_manager["fujimoto_off-policy_2019"]),
        # #         bib_manager.cite_entry(bib_manager["levine_offline_2020"]),  # 2020 offline RL paper
        # #         bib_manager.cite_entry(bib_manager["cql"]),  # 2020 CQL
        # #         bib_manager.cite_entry(bib_manager["REM"]),  # 2020 REM
        # #     ],
        # # },
        bib_manager.cite_entry(bib_manager["cql"]),  # 2020 CQL
        CQLDemo(),
        # 2021 Zadeh recognized for XAI
        {
            "Zadeh further \nrecognized for \nhis XAI efforts": [
                bib_manager.cite_entry(bib_manager["bouchon-meunier_lotfi_2021"]),
                bib_manager.cite_entry(
                    bib_manager["rayz_why_2022"]
                ),  # 2022, why f.l. is needed for XAI
                bib_manager.cite_entry(
                    bib_manager["noauthor_towards_nodate"]
                ),  # 2022, toward f.l. XAI
            ],
        },
        # time for me
        PromptSlide(prompt="Part I: Translation", skip=True),
        bib_manager.cite_entry(bib_manager["hostetter2023leveraging"]),  # 2023 APFRB
    ]


def from_apfrb_to_cew():
    bib_manager = BibTexManager()
    return [
        PromptSlide(prompt="Part II: Self-Organization", skip=True),
        bib_manager.cite_entry(bib_manager["hostetter2023self"]),  # 2023 CEW
    ]


def from_cew_to_lers():
    return [
        "Self-Organizing Computing with Words:\n"
        "Automatic Discovery of Natural Language Control\n"
        "within an Intelligent Tutoring System (Hostetter et al., In Review)",
    ]


def from_lers_to_llm():
    bib_manager = BibTexManager()
    return [
        bib_manager.cite_entry(bib_manager["hostetter2023latent"]),  # 2023 LLM
    ]


def from_llm_to_fyd():
    return [
        "Self-Organizing ε-Complete Neuro-Fuzzy Q-Networks\n"
        "from Frequent Yet Discernible Patterns (Hostetter et al., In Review)",
    ]


def from_fyd_to_morphism():
    return [
        PromptSlide(prompt="Part III: Morphism", skip=True),
        "The Morphetic ϵ-Delayed Neuro-Fuzzy Network:\n"
        "A General Architecture for Transparent Rule-Based Decision-Making\n"
        "(Hostetter, John Wesley 2025)",
    ]


def expected_timeline():
    return [
        curr_limitations(),
        proposed_studies(),
        PromptSlide(prompt="Expected Timeline", skip=True),
        "May to June 2024: Implement experiments",
        CaptionedJPG(
            path=path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "pictures"
            / "evelyn_prenatal_picture.jpg",
            caption="Evelyn is due to be born (June 29, 2024).",
        ),
        "July to August 2024: Attempt proof & begin job search",
        "September to October 2024: Implement proposed changes",
        "November to December 2024: Run experiments",
        "January to February 2025: Run and analyze ITS study",
        "March 2025: Prepare dissertation & slides",
        "April 2025: Defend dissertation",
        "May 2025: Graduate (hopefully)",
        proposed_plan(),
    ]
