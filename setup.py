#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding="utf8") as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding="utf8") as history_file:
    history = history_file.read()

requirements = ['click>=7.0', 'pdfminer.six>=20200726', 'lxml', 'python-docx', 'folia', 'pandas', 'camelot-py>=0.10.1', 'opencv-python>=4.5.5.62', 'pdftopng>=0.2.3']

setup_requirements = ['click>=7.0', 'pdfminer.six>=20200726', 'lxml', 'python-docx', 'folia', 'pandas', 'camelot-py>=0.10.1', 'opencv-python>=4.5.5.62', 'pdftopng>=0.2.3']

test_requirements = ['click>=7.0', 'pdfminer.six>=20200726', 'lxml', 'python-docx', 'folia', 'pandas', 'stanza', 'spacy', 'deepdiff', 'camelot-py>=0.10.1', 'opencv-python>=4.5.5.62', 'pdftopng>=0.2.3']

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
    long_description_content_type = 'text/x-rst',
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
    version='0.1.52',
    zip_safe=False,
)
