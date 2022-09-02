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
    # py_modules=['tre_event_api'],
    # packages=['tre_schemas', ''],
    packages=['tre_schemas', 'tre_event_api'],
    package_dir={
        'tre_schemas': 'tre_schemas',
        'tre_event_api': '.'
    },
    package_data={
        'tre_schemas': ['*.json'],
        'tre_event_api': [
            'manifest.json',
            'about.json'
        ]
    },
    python_requires='>=3.8'
)
