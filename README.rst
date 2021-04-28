=========
nafigator
=========


.. image:: https://img.shields.io/pypi/v/nafigator.svg
        :target: https://pypi.python.org/pypi/nafigator

.. image:: https://img.shields.io/travis/wjwillemse/nafigator.svg
        :target: https://travis-ci.com/wjwillemse/nafigator

.. image:: https://readthedocs.org/projects/nafigator/badge/?version=latest
        :target: https://nafigator.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


**DISCLAIMER - BETA PHASE**

*This parser to naf is currently in a beta phase.*

Python package to convert text documents to NLP Annotation Format (NAF)


* Free software: MIT license
* Documentation: https://nafigator.readthedocs.io.


Features
--------

Nafigator allows you to store NLP output from custom made spaCy and stanza pipelines with (intermediate) results and all processing steps in one format.

* Convert text files to .naf files that satisfy the NLP Annotation Format (NAF)

	* Supported input media types: application/pdf (.pdf), text/plain (.txt)

	* Supported output format: .naf (xml)

	* Supported NLP pipelines: spaCy, stanza

	* Supported NAF layers: raw, text, terms, entities, deps

* Read .naf documents and access data as Python lists and dicts

The NAF format
--------------

Key features:

* Multilayered extensible annotations;

* Reproducible NLP pipelines;

* NLP processor agnostic;

* Compatible with RDF

References:

* `NAF: the NLP Annotation Format <http://newsreader-project.eu/files/2013/01/techreport.pdf>`_

* `NAF documentation on Github <https://github.com/newsreader/NAF>`_


Installation
------------

To install the package

::

    pip install nafigator

To install the package from Github

::

	pip install -e git+https://github.com/wjwillemse/nafigator.git#egg=nafigator


How to run
----------

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

To parse an pdf or a txt file run in the root of the project::

	python -m nafigator.parse


Function calls
~~~~~~~~~~~~~~

Example: ::

	from nafigator.parse import generate_naf

	doc = generate_naf(input = "../data/example.pdf",
	                   engine = "stanza",
	                   language = "en",
	                   naf_version = "v3.1",
	                   dtd_validation = False,
	                   params = {'fileDesc': {'author': 'W.J.Willemse'}},
	                   nlp = None)

- input: text document to convert to naf document
- engine: pipeline processor, i.e. 'spacy' or 'stanza'
- language: 'en' or 'nl'
- naf_version: 'v3' or 'v3.1'
- dtd_validation: True or False (default = False)
- params: dictionary with parameters (default = {})	
- nlp: custom made pipeline object from spacy or stanza (default = None)

Get the document and processors metadata via::

	doc.header

Output of doc.header of processed data/example.pdf::

	{
		'fileDesc': {
			'author': 'W.J.Willemse',
			'creationtime': '2021-04-25T11:28:58UTC', 
	 	 	'filename': 'data/example.pdf', 
	 	 	'filetype': 'application/pdf', 
	 	 	'pages': '2'}, 
	 	'public': {
			'{http://purl.org/dc/elements/1.1/}uri': 'data/example.pdf', 
			'{http://purl.org/dc/elements/1.1/}format': 'application/pdf'}, 
	 		...

Get the raw layer output via::

	doc.raw

Output of doc.raw of processed data/example.pdf::

	The cat sat on the mat. Matt was his name.

Get the text layer output via::

	doc.text

Output of doc.text of processed data/example.pdf::

	[
		{'text': 'The', 'page': '1', 'sent': '1', 'id': 'w1', 'length': '3', 'offset': '0'}, 
		{'text': 'cat', 'page': '1', 'sent': '1', 'id': 'w2', 'length': '3', 'offset': '4'}, 
		{'text': 'sat', 'page': '1', 'sent': '1', 'id': 'w3', 'length': '3', 'offset': '8'}, 
		{'text': 'on', 'page': '1', 'sent': '1', 'id': 'w4', 'length': '2', 'offset': '12'}, 
		{'text': 'the', 'page': '1', 'sent': '1', 'id': 'w5', 'length': '3', 'offset': '15'}, 
		{'text': 'mat', 'page': '1', 'sent': '1', 'id': 'w6', 'length': '3', 'offset': '19'}, 
		{'text': '.', 'page': '1', 'sent': '1', 'id': 'w7', 'length': '1', 'offset': '22'}, 
		{'text': 'Matt', 'page': '1', 'sent': '2', 'id': 'w8', 'length': '4', 'offset': '24'},
		{'text': 'was', 'page': '1', 'sent': '2', 'id': 'w9', 'length': '3', 'offset': '29'}, 
		{'text': 'his', 'page': '1', 'sent': '2', 'id': 'w10', 'length': '3', 'offset': '33'},
		{'text': 'name', 'page': '1', 'sent': '2', 'id': 'w11', 'length': '4', 'offset': '37'},
		{'text': '.', 'page': '1', 'sent': '2', 'id': 'w12', 'length': '1', 'offset': '41'}
	]

Get the terms layer output via::

	doc.terms

Output of doc.terms of processed data/example.pdf::

	[
		{'id': 't1', 'lemma': 'the', 'pos': 'DET', 'targets': ['w1']}, 
		{'id': 't2', 'lemma': 'cat', 'pos': 'NOUN', 'targets': ['w2']}, 
		{'id': 't3', 'lemma': 'sit', 'pos': 'VERB', 'targets': ['w3']}, 
		{'id': 't4', 'lemma': 'on', 'pos': 'ADP', 'targets': ['w4']}, 
		{'id': 't5', 'lemma': 'the', 'pos': 'DET', 'targets': ['w5']}, 
		{'id': 't6', 'lemma': 'mat', 'pos': 'NOUN', 'targets': ['w6']}, 
		{'id': 't7', 'lemma': '.', 'pos': 'PUNCT', 'targets': ['w7']}, 
		{'id': 't8', 'lemma': 'Matt', 'pos': 'PROPN', 'targets': ['w8']}, 
		{'id': 't9', 'lemma': 'be', 'pos': 'AUX', 'targets': ['w9']}, 
		{'id': 't10', 'lemma': 'he', 'pos': 'PRON', 'targets': ['w10']}, 
		{'id': 't11', 'lemma': 'name', 'pos': 'NOUN', 'targets': ['w11']}, 
		{'id': 't12', 'lemma': '.', 'pos': 'PUNCT', 'targets': ['w12']}]

Get the entities layer output via::

	doc.entities

Output of doc.entities of processed data/example.pdf::

	[
		{'id': 'e1', 'type': 'PERSON', 'targets': ['t8']}
	]

Get the entities layer output via::

	doc.deps

Output of doc.deps of processed data/example.pdf::

	[
		{'from': 't2', 'to': 't1', 'rfunc': 'det'},
		{'from': 't3', 'to': 't2', 'rfunc': 'nsubj'}, 
		{'from': 't6', 'to': 't4', 'rfunc': 'case'}, 
		{'from': 't3', 'to': 't6', 'rfunc': 'obl'}, 
		{'from': 't6', 'to': 't5', 'rfunc': 'det'}, 
		{'from': 't3', 'to': 't7', 'rfunc': 'punct'}, 
		{'from': 't11', 'to': 't8', 'rfunc': 'nsubj'}, 
		{'from': 't11', 'to': 't9', 'rfunc': 'cop'}, 
		{'from': 't11', 'to': 't10', 'rfunc': 'nmod:poss'}, 
		{'from': 't11', 'to': 't12', 'rfunc': 'punct'}
	]

Get the formats layer output via::

	doc.formats

Output of doc.formats::

	[
		{'length': '45', 'offset': '0', 'textboxes': [
			{'textlines': [
				{'texts': [
					{'font': 'CIDFont+F1', 
					 'size': '12.000', 
					 'length': '42', 
					 'offset': '0', 
					 'text': 'The cat sat on the mat. Matt was his name.'}]
				}
			}]
		]}
	]

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
