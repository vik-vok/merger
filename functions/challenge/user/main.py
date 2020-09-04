import json
import requests

API_PATH = "https://vikvok-anldg2io3q-ew.a.run.app"

CHALLENGE = API_PATH + "/challenges/{userId}"
USER = API_PATH + "/users/{userId}"


def merge_challenge_user(request):
    # 1. Get ID from request
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "userId" in request_json:
        user_id = request_json["userId"]
    elif request_args and "userId" in request_args:
        user_id = request_args["userId"]
    else:
        return json.dumps({"error": "Missing parameter: userId"}), 422, {}

    # 2. Get Recorded Voice
    url = CHALLENGE.format(userId=user_id)
    try:
        challenges = requests.get(url).json()
    except requests.exceptions.RequestException as err:
        return json.dumps({"API Call Path": url, "Error": err}), 500, {}

    # 3. Get Users for Recorded Voice
    for challenge in challenges:
        sender_user_id = challenge['senderUserId']
        del challenge['senderUserId']
        url = USER.format(userId=sender_user_id)
        try:
            user = requests.get(url).json()
            challenge['senderUser'] = user
        except requests.exceptions.RequestException as err:
            return json.dumps({"API Call Path": url, "Error": err}), 500, {}

    # 4. Return Data in JSON
    return json.dumps(challenges, indent=4, default=str)
