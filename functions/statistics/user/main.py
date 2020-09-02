import json
import requests

STATISTICS_USER_URL = "https://vikvok-anldg2io3q-ew.a.run.app/statistics/user/{}"
ORIGINAL_VOICES_URL = "https://vikvok-anldg2io3q-ew.a.run.app/originalvoices/{}"


def user_statistics(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "userId" in request_json:
        user_id = request_json["userId"]
    elif request_args and "userId" in request_args:
        user_id = request_args["userId"]
    else:
        #
        return "userId not found!"

    statistics_json = requests.get(STATISTICS_USER_URL.format(user_id)).json()

    for key in ["maxScores", "timeScores"]:
        for dic in statistics_json[key]:
            voice_id = dic["voiceId"]
            del dic["voiceId"]
            dic["voice"] = requests.get(ORIGINAL_VOICES_URL.format(voice_id)).json()

    for i, voice_id in enumerate(statistics_json["popular_voices"]):
        statistics_json["popular_voices"][i] = requests.get(
            ORIGINAL_VOICES_URL.format(voice_id)
        ).json()

    return json.dumps(statistics_json)
