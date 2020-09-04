import json
import requests
from google.cloud import bigquery

RECORDED_VOICES_URL = (
    "https://vikvok-anldg2io3q-ew.a.run.app/recordedvoices/original/{}"
)
USERS_URL = "https://vikvok-anldg2io3q-ew.a.run.app/users/{}"


def get_score():
    client = bigquery.Client("speech-similarity")

    query_job = client.query(
        """
            select
                Score, RecordedVoiceId
            from 
                statistics.recorded_voices 
        """
    )

    users_tried = query_job.result()
    result = {}
    for row in users_tried:
        result[row.RecordedVoiceId] = row.Score
    return result


def original_voice_recorded_voices(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "originalVoiceId" in request_json:
        voice_id = request_json["originalVoiceId"]
    elif request_args and "originalVoiceId" in request_args:
        voice_id = request_args["originalVoiceId"]
    else:
        # error
        return "originalVoiceId not found!"

    voices_json = requests.get(RECORDED_VOICES_URL.format(voice_id)).json()
    print(voices_json[0])
    result = get_score()
    cache = {}
    for i, voice in enumerate(voices_json):
        
        user_id = voice["userId"]
        if user_id in cache:
            user = cache[user_id]
        else:
            user = requests.get(USERS_URL.format(user_id)).json()
            cache[user_id] = user
        voices_json[i]["user"] = user
        del voices_json[i]["userId"]
        rec_id = str(voices_json[i]['recordedVoiceId'])
        voices_json[i]["score"] = 0 if rec_id not in result else result[rec_id]

    return json.dumps(voices_json)
