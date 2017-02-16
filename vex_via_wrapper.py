import requests
MATCH_LIST_URL = "http://data.vexvia.dwabtech.net/mobile/events/csv"
DIVISION_URL = "http://data.vexvia.dwabtech.net/mobile/{}/divisions/csv"
MATCH_URL = "http://data.vexvia.dwabtech.net/mobile/{}/{}/matches/csv"


def get_events(iq=False):
    data = requests.get(MATCH_LIST_URL).text.split("\r\n")[1:-1]
    if iq:
        return [match.split(",") for match in data if u"re-viqc" in match]
    else:
        return [match.split(",") for match in data if u"re-vrc" in match]


def get_divisions(event_id):
    data = requests.get(DIVISION_URL.format(event_id)).text.split("\r\n")[1:-1]
    return [division.split(",") for division in data]


def get_matches(event_id, division):
    data = requests.get(MATCH_URL.format(
        event_id, division)).text.split("\r\n")[1:-1]
    return [division.split(",") for division in data]
