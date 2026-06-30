import os
from setuptools import setup, find_packages

version = os.environ.get("SDK_VERSION", "0.0.0")

setup(
    name="loga-sms-sdk",
    version=version,
    description="Official Python SDK for Loga SMS Core Middleware API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Loga Engineering",
    author_email="support@loga-engineering.com",
    url="https://github.com/loga-engineering/loga-sms-python-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
