"""
Build tre_event_lib with schemas and API.
"""
import os
import setuptools

build_version = os.environ['BUILD_VERSION']

setuptools.setup(
    name='tre_event_lib',
    version=build_version,
    description='TRE Python JSON schema event library',
    packages=['tre_event_lib.tre_schemas', 'tre_event_lib'],
    package_data={
        'tre_event_lib.tre_schemas': ['*.json'],
        'tre_event_lib': [
            'about.json'
        ]
    },
    python_requires='>=3.8'
)
