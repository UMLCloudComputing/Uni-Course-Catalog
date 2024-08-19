import json
import db

def handler(event, context):
    # api_path = event.get('path', '')

    # Get JSON body of HTTP request
    body = json.loads(event.get('body', '{}'))

    # What request is it (GET, POST, PUT, DELETE)?
    method = event.get('httpMethod', '')

    # Get user_id, entry_name, and password from JSON body
    prefix = body.get('prefix', '')
    code = body.get('code', '')

    # If no user_id, entry_name, or password, return error
    if not prefix or not code:
        return {
            'statusCode': 400,
            'body': "You didn't specify any parameters\n"
        }

    match method:
        case 'POST':
            result = db.get_course(prefix, code)
            return {
                'statusCode': 200 if result else 400,
                'body': result if result else 'Error in upsertion\n'
            }