import json
import db

def handler(event, context):
    # api_path = event.get('path', '')
    print("Start of event")

    # Get JSON body of HTTP request
    raw_request = event.get('body', '{}')

    body = json.loads(raw_request)

    # What request is it (GET, POST, PUT, DELETE)?
    method = event.get('httpMethod', '')

    # Get user_id, entry_name, and password from JSON body
    prefix = body.get('prefix', '')
    code = body.get('code', '')

    # If no user_id, entry_name, or password, return error
    # if not prefix or not code:
    #     return {
    #         'statusCode': 400,
    #         'body': "You didn't specify any parameters\n"
    #     }

    match method:
        case 'POST':
            result = db.get_course(prefix, code)
            print(result)
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }