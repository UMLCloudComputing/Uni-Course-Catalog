import boto3
import os

TABLE_NAME = os.getenv("TABLE")

# # set TABLE_NAME to 'TinypassTable' if it is not set
if TABLE_NAME is None:
    TABLE_NAME = 'UniCourseCatalogStack-TableUniCourseCatalogStack6BE39F41-G4BYFQ24EUN0'

def get_dynamodb_client():
    return boto3.client('dynamodb', region_name='us-east-1')

# Add an entry with certain attribute
def insert_course(dict):
    dynamodb = get_dynamodb_client()
    response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            'prefix': {'S': dict['Department']},
            'code': {'S': dict['CatalogNumber']},
            'title': {'S': dict["Title"]},
            'description': {'S': dict["Description"]},
            'credits' : {'S': str(dict["UnitsMinimum"])},
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False
    
def delete_password(user_id, entry_name):
    # Delete password
    dynamodb = get_dynamodb_client()
    response = dynamodb.delete_item (
        TableName=TABLE_NAME,
        Key= {
            'UserID' : {'S' : user_id},
            'EntryName' : {'S' : entry_name}
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False
    
if __name__ == "__main__":
    dict = {'Id': '008054', 'Department': 'COMP', 'CatalogNumber': '1000', 'Title': 'Media Computing (Formerly 91.100)', 'Description': 'An introductory course to computer programming using multimedia applications such as images, video and audio. Linear data structures representing multimedia data are manipulated with loops and conditionals in the Python language.', 'UnitsMinimum': 3.0, 'UnitsMaximum': 3.0, 'AcademicCareer': {'Value': 1, 'Description': 'Undergraduate', 'XmlValue': 'UGRD'}, 'AcademicGroup': 'SCI', 'AcademicOrganization': 'LCOMPSCI', 'EnrollmentRequirements': '', 'RequirementDesignation': {'Value': 0, 'Description': 'Any', 'XmlValue': ''}, 'Components': None}
    print(insert_course(dict))