from manim_timeline.timeline import Timeline
from manim_timeline.timeline import TimelineCatchUp
from examples.presentation.timeline_events import (
    get_historical_context,
    from_zadeh_to_nfn,
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

if __name__ == "__main__":
    History().render()
