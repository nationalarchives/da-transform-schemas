import os
import setuptools

build_version = os.environ['BUILD_VERSION']
api_name='tre_event_lib'

setuptools.setup(
    name=api_name,
    version=build_version,
    description='TRE Python JSON schema event library',
    py_modules=[api_name],
    packages=['tre_schemas', ''],
    package_dir={
        'tre_schemas': 'tre_schemas',
        '': '.'
    },
    package_data={
        'tre_schemas': ['*.json'],
        '': [
            'manifest.json',
            'about.json'
        ]
    },
    python_requires='>=3.8'
)
