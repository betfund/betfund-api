"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="betfund-api",
    version="0.0.1",
    description="API powering the backend of Betfund.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/betfund/betfund-api",
    author="Michell Bregman, Leon Kozlowski",
    author_email="mitchbregs@gmail.com, leonkozlowski@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="betfund api fastapi",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.55.1,<1",
        "motor>=2.1.0,<3",
        "python-decouple>=3.3.0,<4",
        "pydantic>=1.5.1,<2",
        "sqlalchemy>=1.3.17,<2",
        "python-dateutil>=2.8.1,<3",
        "python-jose>=3.1.0,<4",
        "passlib>=1.7.2,<2",
        "emails>=0.5.15,<1",
        "jinja2>=2.11.2,<3",
        "celery>=4.4.2,<5",
        "uvicorn>=0.11.5,<1"
    ],
    extras_require={
        "testing": [
            "black",
            "flake8",
            "mock",
            "pylint",
            "pytest",
            "pytest-cov"
        ]
    }
)