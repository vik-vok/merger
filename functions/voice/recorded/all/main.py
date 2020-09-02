import json
import requests

API_PATH = "https://vikvok-anldg2io3q-ew.a.run.app"

ORIGINAL_VOICES = API_PATH + "/originalvoices"
USER = API_PATH + "/users/{userId}"


def recorded_voices_full(request):
    # 1. Get All Original Voices
    try:
        url = ORIGINAL_VOICES
        originals_tried = requests.get(url).json()
    except requests.exceptions.RequestException as err:
        return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    # 2. Get All Users for all Original Voices
    cache = {}
    for elem in originals_tried:
        userId = elem.get("userId")

        # Retrieve data
        try:
            if not userId:
                user = None
            else:
                if userId in cache:
                    user = cache[userId]
                else:
                    url = USER.format(userId=userId)
                    user = requests.get(url).json()
                    cache[userId] = user
                del elem["userId"]
            elem["user"] = user
        except requests.exceptions.RequestException as err:
            return (json.dumps({"API Call Path": url, "Error": err}), 500, {})

    # 3. Return Data in JSON
    return json.dumps(originals_tried, indent=4, sort_keys=True, default=str)
