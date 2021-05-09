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

The Nafigator package allows you to store (intermediate) results and processing steps from custom made spaCy and stanza pipelines in one format.

* Convert text files to .naf-files that satisfy the NLP Annotation Format (NAF)

  - Supported input media types: application/pdf (.pdf), text/plain (.txt), text/html (.html)

  - Supported output format: .naf (xml)

  - Supported NLP processors: spaCy, stanza

  - Supported NAF layers: raw, text, terms, entities, deps, multiwords

* Read .naf documents and access data as Python lists and dicts

In addition to NAF a 'formats' layer is added with text format data (font and size) to allow text classification like header detection.

When reading .naf-files Nafigator stores data in memory as lxml ElementTrees. The lxml package provides a Pythonic binding for C libaries so it should be very fast.

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
	                   params = {'fileDesc': {'author': 'anonymous'}},
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
			'author': 'anonymous',
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

	The Nafigator package allows you to store NLP output from custom made spaCy and stanza  pipelines with (intermediate) results and all processing steps in one format.  Multiwords like in 'we have set that out below' are recognized (depending on your NLP  processor).

Get the text layer output via::

	doc.text

Output of doc.text of processed data/example.pdf::

	[
		{'text': 'The', 'page': '1', 'sent': '1', 'id': 'w1', 'length': '3', 'offset': '0'}, 
		{'text': 'Nafigator', 'page': '1', 'sent': '1', 'id': 'w2', 'length': '9', 'offset': '4'}, 
		{'text': 'package', 'page': '1', 'sent': '1', 'id': 'w3', 'length': '7', 'offset': '14'}, 
		{'text': 'allows', 'page': '1', 'sent': '1', 'id': 'w4', 'length': '6', 'offset': '22'}, 
		{'text': 'you', 'page': '1', 'sent': '1', 'id': 'w5', 'length': '3', 'offset': '29'}, 
		{'text': 'to', 'page': '1', 'sent': '1', 'id': 'w6', 'length': '2', 'offset': '33'}, 
		{'text': 'store', 'page': '1', 'sent': '1', 'id': 'w7', 'length': '5', 'offset': '36'}, {'text': 'NLP', 'page': '1', 'sent': '1', 'id': 'w8', 'length': '3', 'offset': '42'}, 
		{'text': 'output', 'page': '1', 'sent': '1', 'id': 'w9', 'length': '6', 'offset': '46'}, 
		{'text': 'from', 'page': '1', 'sent': '1', 'id': 'w10', 'length': '4', 'offset': '53'}, 
		{'text': 'custom', 'page': '1', 'sent': '1', 'id': 'w11', 'length': '6', 'offset': '58'}, 
		{'text': 'made', 'page': '1', 'sent': '1', 'id': 'w12', 'length': '4', 'offset': '65'}, 
		{'text': 'spa', 'page': '1', 'sent': '1', 'id': 'w13', 'length': '3', 'offset': '70'}, 
		{'text': 'Cy', 'page': '1', 'sent': '2', 'id': 'w14', 'length': '2', 'offset': '73'}, 
		{'text': 'and', 'page': '1', 'sent': '2', 'id': 'w15', 'length': '3', 'offset': '76'}, 
		{'text': 'stanza', 'page': '1', 'sent': '2', 'id': 'w16', 'length': '6', 'offset': '80'}, 
		{'text': 'pipelines', 'page': '1', 'sent': '2', 'id': 'w17', 'length'
		...

Get the terms layer output via::

	doc.terms

Output of doc.terms of processed data/example.pdf::

	[
		{'id': 't1', 'lemma': 'the', 'pos': 'DET', 'type': 'open', 'morphofeat': 'Definite=Def|PronType=Art', 'targets': [{'id': 'w1'}]}, 
		{'id': 't2', 'lemma': 'Nafigator', 'pos': 'PROPN', 'type': 'open', 'morphofeat': 'Number=Sing', 'targets': [{'id': 'w2'}]}, 
		{'id': 't3', 'lemma': 'package', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'targets': [{'id': 'w3'}]}, 
		{'id': 't4', 'lemma': 'allow', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin', 'targets': [{'id': 'w4'}]}, 
		{'id': 't5', 'lemma': 'you', 'pos': 'PRON', 'type': 'open', 'morphofeat': 'Case=Acc|Person=2|PronType=Prs', 'targets': [{'id': 'w5'}]}, 
		{'id': 't6', 'lemma': 'to', 'pos': 'PART', 'type': 'open', 'targets': [{'id': 'w6'}]}, 
		{'id': 't7', 'lemma': 'store', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'VerbForm=Inf', 'targets': [{'id': 'w7'}]}, 
		{'id': 't8', 'lemma': 'nlp', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'targets': [{'id': 'w8'}]}, 
		{'id': 't9', 'lemma': 'output', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'targets': [{'id': 'w9'}]},
		...
 
Get the entities layer output via::

	doc.entities

Output of doc.entities of processed data/example.pdf::

	[
		{'id': 'e1', 'type': 'PRODUCT', 'text': 'Nafigator', 'targets': [{'id': 't2'}]}, 
		{'id': 'e2', 'type': 'CARDINAL', 'text': 'one', 'targets': [{'id': 't28'}]}]
	]

Get the entities layer output via::

	doc.deps

Output of doc.deps of processed data/example.pdf::

	[
		{'from_term': 't3', 'to_term': 't1', 'from_orth': 'package', 'to_orth': 'The', 'rfunc': 'det'}, 
		{'from_term': 't4', 'to_term': 't3', 'from_orth': 'allows', 'to_orth': 'package', 'rfunc': 'nsubj'}, 
		{'from_term': 't3', 'to_term': 't2', 'from_orth': 'package', 'to_orth': 'Nafigator', 'rfunc': 'compound'}, 
		{'from_term': 't4', 'to_term': 't5', 'from_orth': 'allows', 'to_orth': 'you', 'rfunc': 'obj'},
		{'from_term': 't7', 'to_term': 't6', 'from_orth': 'store', 'to_orth': 'to', 'rfunc': 'mark'},
		{'from_term': 't4', 'to_term': 't7', 'from_orth': 'allows', 'to_orth': 'store', 'rfunc': 'xcomp'}, 
		{'from_term': 't9', 'to_term': 't8', 'from_orth': 'output', 'to_orth': 'NLP', 'rfunc': 'compound'}, 
		{'from_term': 't7', 'to_term': 't9', 'from_orth': 'store', 'to_orth': 'output', 'rfunc': 'obj'}, 
		...

Get the multiwords layer output via::

	doc.multiwords

Output of doc.multiwords::

	[
		{'id': 'mw1', 'lemma': 'set_out', 'pos': 'VERB', 'type': 'phrasal', 'components': [
				{'id': 'mw1.c1', 'targets': [{'id': 't37'}]}, 
				{'id': 'mw1.c2', 'targets': [{'id': 't39'}]}]}
	]


Get the formats layer output via::

	doc.formats

Output of doc.formats::

	[	
		{'length': '268', 'offset': '0', 'textboxes': [
			{'textlines': [
				{'texts': [
					{'font': 'CIDFont+F1', 'size': '12.000', 'length': '87', 'offset': '0', 'text': 'The Nafigator package allows you to store NLP output from custom made spaCy and stanza '
					}]
				}, 
 				{'texts': [
					{'font': 'CIDFont+F1', 'size': '12.000', 'length': '77', 'offset': '88', 'text': 'pipelines with (intermediate) results and all processing steps in one format.'
					}]
				}]
			}, 
			{'textlines': [
				{'texts': [
					{'font': 'CIDFont+F1', 'size': '12.000', 'length': '86', 'offset': '167', 'text': 'Multiwords like in 'we have set that out below' are recognized (depending on your NLP '
					}]
				}, 
				{'texts': [
					{'font': 'CIDFont+F1', 'size': '12.000', 'length': '11', 'offset': '254', 'text': 'processor).'
					}]
				}]}], 
	...


