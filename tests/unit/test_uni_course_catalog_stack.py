import aws_cdk as core
import aws_cdk.assertions as assertions

from uni_course_catalog.uni_course_catalog_stack import UniCourseCatalogStack

# example tests. To run these tests, uncomment this file along with the example
# resource in uni_course_catalog/uni_course_catalog_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UniCourseCatalogStack(app, "uni-course-catalog")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
