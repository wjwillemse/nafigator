#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['click>=7.0', 'pdfminer.six', 'lxml', 'python-docx', 'folia', 'pandas']

setup_requirements = ['click>=7.0', 'pdfminer.six', 'lxml', 'python-docx', 'folia', 'pandas']

test_requirements = ['click>=7.0', 'pdfminer.six', 'lxml', 'python-docx', 'folia', 'pandas', 'stanza', 'spacy']

setup(
    author="De Nederlandsche Bank",
    author_email='w.j.willemse@dnb.nl',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python package to convert spaCy and Stanza documents to NLP Annotation Format (NAF)",
    entry_points={
        'console_scripts': [
            'nafigator=nafigator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nafigator',
    name='nafigator',
    packages=find_packages(include=['nafigator', 'nafigator.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/denederlandschebank/nafigator',
    version='0.1.32',
    zip_safe=False,
)
