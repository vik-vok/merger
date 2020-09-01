import json
import requests


USERS_URL = 'https://vikvok-anldg2io3q-ew.a.run.app/originalvoices/{}'
STATISTICS_VOICE_URL = 'https://vikvok-anldg2io3q-ew.a.run.app/statistics/voice/{}'


def one_voice_statistics(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'originalVoiceId' in request_json:
        voice_id = request_json['originalVoiceId']
    elif request_args and 'originalVoiceId' in request_args:
        voice_id = request_args['originalVoiceId']
    else:
        #
        return "originalVoiceId not found!"

    statistics_json = requests.get(STATISTICS_VOICE_URL.format(voice_id)).json()

    for i, dic in statistics_json['maxScorers']:
        user_id = dic['user_id']
        del dic['user_id']
        dic['user'] = requests.get(USERS_URL.format(user_id)).json()

    return json.dumps(statistics_json)
