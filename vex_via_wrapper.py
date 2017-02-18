import requests
MATCH_LIST_URL = "http://data.vexvia.dwabtech.net/mobile/events/csv"
DIVISION_URL = "http://data.vexvia.dwabtech.net/mobile/{}/divisions/csv"
MATCH_URL = "http://data.vexvia.dwabtech.net/mobile/{}/{}/matches/csv"


def get_events(is_iq: bool=False) -> list:
    """Get a list of iq events or edr events.

    Args:
        is_iq: True for vex iq tournaments, False for vex edr(default).

    Returns:
        A 2D array of the events.

    """
    data = requests.get(MATCH_LIST_URL).text.split("\r\n")[1:-1]
    if is_iq:
        return [match.split(",") for match in data if u"re-viqc" in match]
    else:
        return [match.split(",") for match in data if u"re-vrc" in match]


def get_divisions(event_id: str) -> list:
    """Get a list of the divisions of an event.

    Args:
        event_id: The id of the event.

    Returns:
        A 2D array of the divisions.

    """
    data = requests.get(DIVISION_URL.format(event_id)).text.split("\r\n")[1:-1]
    return [division.split(",") for division in data]


def get_matches(event_id: str, division: str) -> list:
    """Get a list of the matches in a divisions of an event.

    Args:
        event_id: The id of the event.
        division: The division id.

    Returns:
        A 2D array of the matches.

    """
    data = requests.get(MATCH_URL.format(
        event_id, division)).text.split("\r\n")[1:-1]
    return [division.split(",") for division in data]
