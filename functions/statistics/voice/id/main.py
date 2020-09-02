import json
import requests

API_PATH = "https://vikvok-anldg2io3q-ew.a.run.app"

STATISTICS_VOICE_URL = API_PATH + "/statistics/voice/{voiceId}"
USERS_URL = API_PATH + "/originalvoices/{userId}"


def one_voice_statistics(request):
    # 1. Get Original Voice ID
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "originalVoiceId" in request_json:
        voiceId = request_json["originalVoiceId"]
    elif request_args and "originalVoiceId" in request_args:
        voiceId = request_args["originalVoiceId"]
    else:
        return (json.dumps({"error": "Missing parameter: originalVoiceId"}), 422, {})

    try:
        url = STATISTICS_VOICE_URL.format(voiceId=voiceId)
        statistics_json = requests.get(url).json()
    except requests.exceptions.RequestException as err:
        return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    for i, dic in statistics_json["maxScorers"]:
        userId = dic["UserId"]
        del dic["UserId"]
        try:
            url = USERS_URL.format(userId=userId)
            statistics_json = requests.get(url).json()
            user = requests.get(url).json()
            dic["user"] = user
        except requests.exceptions.RequestException as err:
            return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    return json.dumps(statistics_json)
