from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    CfnOutput
)
from constructs import Construct

class UniCourseCatalogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table
        table = dynamodb.TableV2(self, f"Table{construct_id}",
            partition_key=dynamodb.Attribute(name="prefix", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="code", type=dynamodb.AttributeType.STRING)
        )

        # Lambda Function
        dockerFunc = _lambda.DockerImageFunction(
            scope=self,
            id=f"ID{construct_id}",
            function_name=construct_id,
            environment= {
                "TABLE_NAME": table.table_name
            },            
            code=_lambda.DockerImageCode.from_image_asset(
                directory="src"
            ),
            timeout=Duration.seconds(900)
        )

        # API Gateway to Lambda
        api = apigateway.LambdaRestApi(self, f"API{construct_id}",
            handler=dockerFunc,
            proxy=True,
        )

        # Grant read/write permissions to the Lambda function
        table.grant_read_write_data(dockerFunc.role)

        # Output name of the table
        CfnOutput(self, f"TableName{construct_id}", value=table.table_name)