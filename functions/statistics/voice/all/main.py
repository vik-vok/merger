import json
import requests


USERS_URL = "https://vikvok-anldg2io3q-ew.a.run.app/originalvoices/{}"
STATISTICS_VOICE_URL = "https://vikvok-anldg2io3q-ew.a.run.app/statistics/voice/"


def all_voice_statistics(request):

    statistics_json = requests.get(STATISTICS_VOICE_URL).json()

    for key, elem in statistics_json.items():
        for i, dic in elem["maxScorers"].items():
            user_id = dic["UserId"]
            del dic["UserId"]
            dic["user"] = requests.get(USERS_URL.format(user_id)).json()

    return json.dumps(statistics_json)
