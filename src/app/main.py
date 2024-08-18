import json
import db

def handler(event, context):
    api_path = event.get('path', '')
    match api_path:
        case '/entry':
            return entry(event)
        case '/health':
            return {
                'statusCode': 200,
                'body': 'OK'
            }
        case _:
            return {
                'statusCode': 404,
                'body': 'Not Found'
            }
        
def entry(event):
    # Get JSON body of HTTP request
    body = json.loads(event.get('body', '{}'))

    # What request is it (GET, POST, PUT, DELETE)?
    method = event.get('httpMethod', '')

    # Get user_id, entry_name, and password from JSON body
    UserID = body.get('UserID', '')
    EntryName = body.get('EntryName', '')
    Password = body.get('Password', '')

    match method:
        case 'POST':
            result = db.upsert_password(UserID, EntryName, Password)
            return {
                'statusCode': 200 if result else 400,
                'body': 'Password upserted\n' if result else 'Error in upsertion\n'
            }
        # case 'DELETE':
        #     result = db.delete_password(UserID, EntryName)
        #     return {
        #         'statusCode': 200 if result else 400,
        #         'body': 'Password deleted\n' if result else 'Error in deletion\n'
        #     }