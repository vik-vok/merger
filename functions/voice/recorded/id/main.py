import json
import requests

API_PATH = "https://vikvok-anldg2io3q-ew.a.run.app"

ORIGINAL_VOICES = API_PATH + "/originalvoices/{originalVoiceId}"
USER = API_PATH + "/users/{userId}"


def merge_original_voice_single_full(request):
    # 1. Get ID from request
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "originalVoiceId" in request_json:
        original_voice_id = request_json["originalVoiceId"]
    elif request_args and "originalVoiceId" in request_args:
        original_voice_id = request_args["originalVoiceId"]
    else:
        return json.dumps({"error": "Missing parameter: originalVoiceId"}), 422, {}

    # 2. Get Recorded Voice
    try:
        url = ORIGINAL_VOICES.format(originalVoiceId=original_voice_id)
        original_voice = requests.get(url).json()
    except requests.exceptions.RequestException as err:
        return json.dumps({"API Call Path": url, "Error": err}), 500, {}

    # 3. Get Users for Recorded Voice
    user_id = original_voice.get("userId")
    try:
        user = None
        if user_id:
            url = USER.format(userId=user_id)
            user = requests.get(url).json()
            del original_voice["userId"]
        original_voice["user"] = user
    except requests.exceptions.RequestException as err:
        return json.dumps({"API Call Path": url, "Error": err}), 500, {}

    # 4. Return Data in JSON
    return json.dumps(original_voice, indent=4, sort_keys=True, default=str)
