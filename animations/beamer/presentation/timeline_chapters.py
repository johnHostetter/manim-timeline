from animations.demos.timeline import Timeline
from animations.demos.timeline_helper import TimelineConfig
from animations.beamer.presentation.timeline_events import (
    get_historical_context, from_zadeh_to_nfn, from_nfn_to_wang_mendel, from_wang_mendel_to_apfrb,
    from_apfrb_to_cew, from_cew_to_lers, from_lers_to_llm, from_llm_to_fyd, from_fyd_to_morphism,
    expected_timeline
)


class History(Timeline):
    """
    Stops at the first NFN publication.
    """

    def __init__(self, **kwargs):
        super().__init__(
            timeline_events=get_historical_context() + from_zadeh_to_nfn(),
            incl_ending=False,
            globally_enable_animation=True,
            **kwargs
        )


class TimelineCatchUp(Timeline):
    """
    Adds the prior events without animations and then adds the new events with animations.
    """

    def __init__(self, prior_events, new_events, incl_ending=False, **kwargs):
        super().__init__(
            timeline_events=(
                    [
                        TimelineConfig(draw_animations=False)
                    ] + prior_events + [
                        TimelineConfig(draw_animations=True)
                    ] + new_events
            ),
            globally_enable_animation=False,
            incl_ending=incl_ending,
            **kwargs
        )


class RW1(TimelineCatchUp):
    """
    Continues from the first NFN publication to the Wang-Mendel publication.
    """

    def __init__(self, **kwargs):
        # the following has already been added
        super().__init__(
            prior_events=get_historical_context() + from_zadeh_to_nfn(),
            new_events=from_nfn_to_wang_mendel(),
            **kwargs
        )


class RW2(TimelineCatchUp):
    """
    Continues from the Wang-Mendel publication to my APFRB study.
    """

    def __init__(self, **kwargs):
        # the following has already been added
        super().__init__(
            prior_events=from_nfn_to_wang_mendel(),
            # (
            #         get_historical_context() + from_zadeh_to_nfn() + from_nfn_to_wang_mendel()
            # ),
            new_events=from_wang_mendel_to_apfrb(),
            **kwargs
        )


class M1(TimelineCatchUp):
    """
    Continues from my APFRB study to my CEW study.
    """

    def __init__(self, **kwargs):
        # the following has already been added, and the {None: ...} is a special flag
        background = (
                get_historical_context() + from_zadeh_to_nfn()
                + from_nfn_to_wang_mendel() + from_wang_mendel_to_apfrb()
        )
        super().__init__(
            prior_events=background,
            new_events=from_apfrb_to_cew(),
            **kwargs
        )


class M2(TimelineCatchUp):
    """
    Continues from my CEW study to my LERS study.
    """

    def __init__(self, **kwargs):
        # the following has already been added, and the {None: ...} is a special flag
        background = (
                get_historical_context() + from_zadeh_to_nfn()
                + from_nfn_to_wang_mendel() + from_wang_mendel_to_apfrb()
        )
        super().__init__(
            prior_events=background + from_apfrb_to_cew(),
            new_events=from_cew_to_lers(),
            **kwargs
        )


class M3(TimelineCatchUp):
    """
    Continues from my LERS study to my LLM study.
    """

    def __init__(self, **kwargs):
        # the following has already been added, and the {None: ...} is a special flag
        background = (
                get_historical_context() + from_zadeh_to_nfn()
                + from_nfn_to_wang_mendel() + from_wang_mendel_to_apfrb()
        )
        super().__init__(
            prior_events=background + from_apfrb_to_cew() + from_cew_to_lers(),
            new_events=from_lers_to_llm(),
            **kwargs
        )


class M4(TimelineCatchUp):
    """
    Continues from my LLM study to my FYD study.
    """

    def __init__(self, **kwargs):
        # the following has already been added, and the {None: ...} is a special flag
        background = (
                get_historical_context() + from_zadeh_to_nfn()
                + from_nfn_to_wang_mendel() + from_wang_mendel_to_apfrb()
        )
        super().__init__(
            prior_events=background + from_apfrb_to_cew() + from_cew_to_lers() + from_lers_to_llm(),
            new_events=from_llm_to_fyd(),
            **kwargs
        )


class P1(TimelineCatchUp):
    """
    Continues from my FYD study to my MED proposal.
    """

    def __init__(self, **kwargs):
        # the following has already been added, and the {None: ...} is a special flag
        background = (
                get_historical_context() + from_zadeh_to_nfn()
                + from_nfn_to_wang_mendel() + from_wang_mendel_to_apfrb()
        )
        old_methods = (
                from_apfrb_to_cew() + from_cew_to_lers() + from_lers_to_llm() + from_llm_to_fyd()
        )
        super().__init__(
            prior_events=background + old_methods,
            new_events=from_fyd_to_morphism(),
            **kwargs
        )


class P2(TimelineCatchUp):
    """
    Continues from my MED proposal to expected timeline.
    """

    def __init__(self, **kwargs):
        # the following has already been added, and the {None: ...} is a special flag
        background = (
                get_historical_context() + from_zadeh_to_nfn()
                + from_nfn_to_wang_mendel() + from_wang_mendel_to_apfrb()
        )
        old_methods = (
                from_apfrb_to_cew() + from_cew_to_lers() + from_lers_to_llm() + from_llm_to_fyd()
        )
        super().__init__(
            prior_events=background + old_methods + from_fyd_to_morphism(),
            new_events=expected_timeline(),
            incl_ending=True,
            **kwargs
        )
