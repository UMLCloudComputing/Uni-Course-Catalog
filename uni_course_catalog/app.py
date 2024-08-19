#!/usr/bin/env python3
import os

import aws_cdk as cdk

from uni_course_catalog_stack import UniCourseCatalogStack

from dotenv import load_dotenv
load_dotenv()

APP_NAME = os.getenv("APP_NAME")
app = cdk.App()
UniCourseCatalogStack(app, APP_NAME)
app.synth()
