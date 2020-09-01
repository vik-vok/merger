import json
import requests

def merge_user_voice_recorded_all(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'userId' in request_json:
        userId = request_json['userId']
    elif request_args and 'userId' in request_args:
        userId = request_args['userId']
    else:
        return (
            json.dumps({"error": "Missing parameter: userId"}),
            422,
            {})

    return {}

