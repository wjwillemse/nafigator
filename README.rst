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

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT
        :alt: License: MIT

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black
        :alt: Code style: black

**DISCLAIMER - BETA PHASE**

*This package is currently in a beta phase.*

to nafigate [ **naf**-i-geyt ]
------------------------------

    *v.intr*, **nafigated**, **nafigating**

    1. To process one of more text documents through a NLP pipeline and output results in the NLP Annotation Format.


Features
--------

The Nafigator package allows you to store (intermediate) results and processing steps from custom made spaCy and stanza pipelines in one format.

* Convert text files to .naf-files that satisfy the NLP Annotation Format (NAF)

  - Supported input media types: application/pdf (.pdf), text/plain (.txt), text/html (.html)

  - Supported output format: naf-xml (.naf), naf-rdf in turtle syntax (.ttl) (very experimental)

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

To convert a .pdf, .txt or .html-file you can use: ::

    from nafigator.parse2naf import generate_naf

    doc = generate_naf(input = "../data/example.pdf",
                       engine = "stanza",
                       language = "en",
                       naf_version = "v3.1",
                       dtd_validation = False,
                       params = {'fileDesc': {'author': 'anonymous'}},
                       nlp = None)

- input: document to convert to naf document
- engine: pipeline processor, i.e. 'spacy' or 'stanza'
- language: for example 'en' or 'nl'
- naf_version: 'v3' or 'v3.1'
- dtd_validation: True or False (default = False)
- params: dictionary with parameters (default = {}) 
- nlp: custom made pipeline object from spacy or stanza (default = None)

The returning object, doc, is a NafDocument from which layers can be accessed.

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
  ...

Get the terms layer output via::

  doc.terms

Output of doc.terms of processed data/example.pdf::

  [
    {'id': 't1', 'lemma': 'the', 'pos': 'DET', 'type': 'open', 'morphofeat': 'Definite=Def|PronType=Art', 'targets': [{'id': 'w1'}]}, 
    {'id': 't2', 'lemma': 'Nafigator', 'pos': 'PROPN', 'type': 'open', 'morphofeat': 'Number=Sing', 'targets': [{'id': 'w2'}]}, 
    {'id': 't3', 'lemma': 'package', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'targets': [{'id': 'w3'}]}, 
    {'id': 't4', 'lemma': 'allow', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin',    
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
  ...


Adding new annotation layers
----------------------------

To add a new annotation layer with elements, start with registering the processor of the new annotations::

  lp = ProcessorElement(name="processorname", version="1.0", timestamp=None, beginTimestamp=None,   endTimestamp=None, hostname=None)

  naf.add_processor_element("recommendations", lp)

Then get the layer and add subelements::

  layer = naf.layer("recommendations")

  data_recommendation = {'id': "recommendation1", 'subjectivity': 0.5, 'polarity': 0.25, 'span': [{'id': 't37'}, {'id': 't39'}]}

  element = self.subelement(element=layer, tag="recommendation", data=data_recommendation)

  naf.add_span_element(element=element, data=data_recommendation)

Retrieve the recommendations with::

  naf.recommendations


Convert NAF file to RDF in turtle syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just run::

	python -m nafigator.convert2rdf

No ontology or vocabulary of NAF exists yet. For now, we map xml tags and attributes to RDF predicates using provisional prefixes and namespaces, for example base attributes are mapped to the prefix naf-base.

Below are some excerpts.

From the nafHeader::

	_:nafHeader
	    naf-base:hasFileDesc [
        	naf-fileDesc:hasCreationtime "2021-05-24T11:29:44UTC"^^xsd:dateTime ;
        	naf-fileDesc:hasFilename "data/example.pdf"^^rdf:XMLLiteral ;
        	naf-fileDesc:hasFiletype "application/pdf"^^rdf:XMLLiteral ;
    	] ;

A word::

	_:w1
	    xl:type naf-base:wordform ;
	    naf-base:hasText """The"""^^rdf:XMLLiteral ;
	    naf-base:hasSent "1"^^xsd:integer ;
	    naf-base:hasPage "1"^^xsd:integer ;
	    naf-base:hasOffset "0"^^xsd:integer ;
	    naf-base:hasLength "3"^^xsd:integer .

A term::

	_:t1
	    xl:type naf-base:term ;
	    naf-base:hasType naf-base:close ;
	    naf-base:hasLemma "the" ;
	    naf-base:hasPos <http://purl.org/olia/olia.owl#Determiner> ;
	    naf-morphofeat:hasDefinite "Def" ;
	    naf-morphofeat:hasPronType "Art" ;
	    naf-base:hasSpan [
        	naf-base:ref _:w1
    	] .

An entity::

	_:e1
	    xl:type naf-base:entity ;
	    naf-base:hasType naf-entity:PRODUCT ;
	    naf-base:hasSpan [
        	naf-base:ref _:t2
    	] .

A dependency::

	_:t3 naf-rfunc:det _:t1

