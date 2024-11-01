import json
def request_successful(message):
    response = {
        "statusCode": 200,
        "body": json.dumps(message),
        "headers": { "Content-Type": "application/json" }
    }
    return response