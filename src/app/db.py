import boto3
import os
from dotenv import load_dotenv
load_dotenv()

def get_dynamodb_client():
    return boto3.client('dynamodb', region_name='us-east-1')

# Add an entry with certain attribute
def insert_course(dict):
    dynamodb = get_dynamodb_client()
    response = dynamodb.put_item(
        TableName=os.getenv('TABLE_NAME'),
        Item={
            'prefix': {'S': dict['Department']},
            'code': {'S': dict['CatalogNumber']},
            'title': {'S': dict["Title"]},
            'description': {'S': dict["Description"]},
            'credits' : {'S': str(dict["UnitsMinimum"])},
            'career' : {'S': dict["AcademicCareer"]["Description"]},
            'requirements' : {'S': dict["EnrollmentRequirements"]},
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False
    
def get_course(prefix, code):
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(
        TableName=os.getenv('TABLE_NAME'),
        Key={
            'prefix': {'S': prefix},
            'code': {'S': code}
        }
    )
    if 'Item' in response:
        dict = {
            'Department': response['Item']['prefix']['S'],
            'CatalogNumber': response['Item']['code']['S'],
            'Title': response['Item']['title']['S'],
            'Description': response['Item']['description']['S'],
            'Credits': response['Item']['credits']['S'],
            'Career': response['Item']['career']['S'],
            'Requirements': response['Item']['requirements']['S']
        }
        return dict
    else:
        return None
    
def get_department(prefix):
    dynamodb = get_dynamodb_client()
    response = dynamodb.query(
        TableName=os.getenv('TABLE_NAME'),
        KeyConditionExpression='prefix = :prefix',
        ExpressionAttributeValues={
            ':prefix': {'S': prefix}
        }
    )

    # print(response['Items'])
    list_dict = []

    for result in response['Items']:
        # print(result)
        dict = {
            'Department': result['prefix']['S'],
            'CatalogNumber': result['code']['S'],
            'Title': result['title']['S'],
            'Description': result['description']['S'],
            'Credits': result['credits']['S'],
            'Career': result['career']['S'],
            'Requirements': result['requirements']['S']
        }
        list_dict.append(dict)

    return list_dict

    

## NOT TESTED
def delete_course(prefix, code):
    # Delete password
    dynamodb = get_dynamodb_client()
    response = dynamodb.delete_item (
        TableName=os.getenv('TABLE_NAME'),
        Key= {
            'prefix' : {'S' : prefix},
            'code' : {'S' : code}
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False
    
if __name__ == "__main__":
    # print(get_course('COMP', '1000'))
    print(get_department('COMP'))
    # dict = {'Id': '008054', 'Department': 'COMP', 'CatalogNumber': '1000', 'Title': 'Media Computing (Formerly 91.100)', 'Description': 'An introductory course to computer programming using multimedia applications such as images, video and audio. Linear data structures representing multimedia data are manipulated with loops and conditionals in the Python language.', 'UnitsMinimum': 3.0, 'UnitsMaximum': 3.0, 'AcademicCareer': {'Value': 1, 'Description': 'Undergraduate', 'XmlValue': 'UGRD'}, 'AcademicGroup': 'SCI', 'AcademicOrganization': 'LCOMPSCI', 'EnrollmentRequirements': '', 'RequirementDesignation': {'Value': 0, 'Description': 'Any', 'XmlValue': ''}, 'Components': None}
    # print(insert_course(dict))