import pathlib


def get_project_root() -> pathlib.Path:
    """
    Get the root directory of the project.

    Returns:
        The root directory of the project.
    """
    return pathlib.Path(__file__).parent.parent
