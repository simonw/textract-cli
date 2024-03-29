import os

def pytest_configure():
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
