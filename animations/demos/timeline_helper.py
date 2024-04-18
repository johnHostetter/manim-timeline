from typing import List

from animations.demos.timeline_events import TimelineEvent


# consistent spacing for the timeline
# spacing = 5  # a good spacing for the timeline I found works well
# digraph_layout = {idx: (idx * spacing, 0, 0) for idx in range(num_of_vertices)}
# spacing relative to timeline events' start and end years
# def get_loc_from_start_end_years(start_year, end_year):
#     return (start_year + end_year) / 2

# def get_event_plot_coords(timeline_event: TimelineEvent):
#     spacing = 5  # a good spacing for the timeline I found works well
#
#     if timeline_event.poi is not None:
#         return timeline_event.poi + spacing, 0, 0
#     return (
#         timeline_event.start_year + spacing, 0, 0
#     ) if timeline_event.era_notation == "CE" else (
#         -1 * (timeline_event.start_year + spacing), 0, 0
#     )
#
# digraph_layout = {
#     idx: get_event_plot_coords(timeline_events[idx - 1])
#     for idx in range(1, num_of_vertices)
# }
# digraph_layout[0] = (timeline_events[0].start_year - 10, 0, 0)

def create_timeline_layout(timeline_events: List[TimelineEvent]) -> dict:
    """
    Given a sequence of timeline events, create a layout for the timeline.
    This layout is a dictionary where the key is the index of the vertex
    and the value is a tuple with the x, y, and z coordinates of the vertex.

    Args:
        timeline_events:

    Returns:
        A dictionary with the layout of the timeline.
    """
    prev_x_location: float = 0
    prev_timeline_event = None
    digraph_layout = {0: (prev_x_location, 0, 0)}
    for timeline_event in timeline_events:
        if not isinstance(timeline_event, dict):
            spacing = 5  # a good spacing for the timeline I found works well
            if isinstance(prev_timeline_event, str) and isinstance(
                    timeline_event, str
            ):
                # two consecutive strings do not need as much spacing
                spacing = 1
            # technically we never use the vertex located at index 0
            new_x_location = prev_x_location + spacing
            digraph_layout[max(digraph_layout.keys()) + 1] = (new_x_location, 0, 0)
            prev_timeline_event = timeline_event
            prev_x_location = new_x_location
        else:
            # this is a dictionary, which means we breeze over the timeline,
            # but we still need to account for the spacing and timeline pins
            for publication in list(timeline_event.values())[0]:
                spacing = 5  # a good spacing for the timeline I found works well
                if isinstance(prev_timeline_event, str) and isinstance(
                        publication, str
                ):
                    # two consecutive strings do not need as much spacing
                    spacing = 1
                # technically we never use the vertex located at index 0
                new_x_location = prev_x_location + spacing
                digraph_layout[max(digraph_layout.keys()) + 1] = (
                    new_x_location,
                    0,
                    0,
                )
                prev_timeline_event = publication
                prev_x_location = new_x_location
    return digraph_layout
