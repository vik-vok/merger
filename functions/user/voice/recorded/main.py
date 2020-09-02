import json
import requests

API_PATH = "https://vikvok-anldg2io3q-ew.a.run.app"

ORIGINALS_TRIED = API_PATH + "/originalvoices/tried/{userId}"
RECORDED_VOICES_BY_ORIGINAL = (
    API_PATH + "/recordedvoices/original/test/{originalVoiceId}/{userId}"
)


def merge_user_voice_recorded_all(request):
    # 1. Get User ID from request
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "userId" in request_json:
        userId = request_json["userId"]
    elif request_args and "userId" in request_args:
        userId = request_args["userId"]
    else:
        return (json.dumps({"error": "Missing parameter: userId"}), 422, {})

    # 2. Get All Original Voices Tried by given User
    try:
        url = ORIGINALS_TRIED.format(userId=userId)
        originals_tried = requests.get(url).json()
    except requests.exceptions.RequestException as err:
        return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    # 3. Get All Recorded voices for all Original Voices
    for elem in originals_tried:
        originalVoiceId = elem["originalVoiceId"]

        # Retrieve data
        try:
            path = RECORDED_VOICES_BY_ORIGINAL.format(
                userId=userId, originalVoiceId=originalVoiceId
            )
            recorded_voices = requests.get(path).json()
            elem["recordedVoices"] = recorded_voices
        except requests.exceptions.RequestException as err:
            return (json.dumps({"API Call Path": path, "Error": err}), 500, {})

    # 4. Return Data in JSON
    return json.dumps(originals_tried, indent=4, sort_keys=True, default=str)
