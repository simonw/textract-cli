import os

def pytest_configure():
    os.environ["MOTO_ALLOW_NONEXISTENT_REGION"] = "1"
