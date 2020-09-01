import json
import requests

COMMENTS_URL = 'https://vikvok-anldg2io3q-ew.a.run.app/comments/original/{}'
USERS_URL = 'https://vikvok-anldg2io3q-ew.a.run.app/users/{}'


def original_voice_comments(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'voiceId' in request_json:
        voice_id = request_json['voiceId']
    elif request_args and 'voiceId' in request_args:
        voice_id = request_args['voiceId']
    else:
        # return error apiresponse
        return ""

    comments_json = requests.get(COMMENTS_URL.format(voice_id)).json()
    for i, comment in enumerate(comments_json):
        user_id = comment['userId']
        user = requests.get(USERS_URL.format(user_id)).json()
        del comments_json[i]['userId']
        comments_json[i]['user'] = user

    return json.dumps(comments_json)
