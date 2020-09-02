import json
import requests

API_PATH = "https://vikvok-anldg2io3q-ew.a.run.app"

STATISTICS_VOICE_URL = API_PATH + "/statistics/voice/{voiceId}"
USERS_URL = API_PATH + "/users/{userId}"


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

    # 2. Fetch Statistics for given voice
    try:
        url = STATISTICS_VOICE_URL.format(voiceId=voiceId)
        statistics_json = requests.get(url).json()
    except requests.exceptions.RequestException as err:
        return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    # 3. Fetch Maxscorer users
    for elem in statistics_json["maxScorers"]:
        try:
            userId = elem["UserId"]
            url = USERS_URL.format(userId=userId)
            user = requests.get(url).json()
            elem["user"] = user
        except requests.exceptions.RequestException as err:
            return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    # 4. Return Data in JSON
    return json.dumps(statistics_json, indent=4, sort_keys=True, default=str)
