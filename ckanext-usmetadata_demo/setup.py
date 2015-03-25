from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
    name='ckanext-usmetadata_demo',
    version=version,
    description="CivicData compatible version of USmetadata extension",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='tanmay',
    author_email='tthakur@accela.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.usmetadata_demo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        usmetadata_demo=ckanext.usmetadata_demo.plugin:MyPlugin
    ''',
)
