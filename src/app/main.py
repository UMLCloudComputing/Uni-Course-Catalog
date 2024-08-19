import json
import db

def handler(event, context):
    # api_path = event.get('path', '')
    print("Start of event")
    method = event.get('httpMethod', '')

    match method:
        case 'GET':
            prefix = event.get('queryStringParameters', {}).get('prefix', '')
            code = event.get('queryStringParameters', {}).get('code', '')
            

            # If there's a prefix and code in query paramters, return the course
            if prefix and code:
                result = db.get_course(prefix, code)
                return {
                    'statusCode': 200,
                    'body': json.dumps(result)
                }
            
            # If there's only a prefix in query parameters, return all courses in that department
            elif prefix:
                return {
                    'statusCode': 200,
                    'body': json.dumps(db.get_department(prefix))
                }