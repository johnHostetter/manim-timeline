import sys

from manim_timeline.timeline import Timeline, TimelineCatchUp
from examples.presentation.timeline_events import (
    get_historical_context,
    from_zadeh_to_nfn,
    from_nfn_to_wang_mendel,
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


if __name__ == "__main__":
    """
    Run this script with the following arguments:
    - timeline: to render the history timeline
    - catchup: render a catchup to the timeline (useful for splitting the timeline into chapters)
    """
    if len(sys.argv) > 1 and sys.argv[1] == "timeline":
        History().render()
    elif len(sys.argv) > 1 and sys.argv[1] == "catchup":
        RW1().render()
    else:
        raise ValueError("Please provide a valid argument: history or rw1")
