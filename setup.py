from setuptools import setup, find_packages

setup(
    name='eol_service',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'httpx'
    ],
)
