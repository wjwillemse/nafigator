=========
nafigator
=========


.. image:: https://img.shields.io/pypi/v/nafigator.svg
        :target: https://pypi.python.org/pypi/nafigator

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

* Convert text files to naf-files that satisfy the NLP Annotation Format (NAF)

  - Supported input media types: application/pdf (.pdf), text/plain (.txt), text/html (.html), MS Word (.docx)

  - Supported output formats: naf-xml (.naf.xml), naf-rdf in turtle-syntax (.ttl) and xml-syntax (.rdf) (experimental)

  - Supported NLP processors: spaCy, stanza

  - Supported NAF layers: raw, text, terms, entities, deps, multiwords

* Read naf-files and access data as Python lists and dicts

When reading naf-files Nafigator stores data in memory as lxml ElementTrees. The lxml package provides a Pythonic binding for C libaries so it should be very fast.

The NLP Annotation Format (NAF)
-------------------------------

Key features:

* Multilayered extensible annotations;

* Reproducible NLP pipelines;

* NLP processor agnostic;

* Compatible with RDF

References:

* `NAF: the NLP Annotation Format <http://newsreader-project.eu/files/2013/01/techreport.pdf>`_

* `NAF documentation on Github <https://github.com/newsreader/NAF>`_


Current changes to NAF:

* a 'formats' layer is added with text format data (font and size) to allow text classification like header detection

* a 'model' attribute is added to LinguisticProcessors to record the model that was used

* all attributes of public are Dublin Core elements and mapped to the dc namespace

* attributes in a dependency relation are renamed 'from_term' and 'to_term' ('from' is a Python reserved word)

The code of the SpaCy converter to NAF is partially based on `SpaCy-to-NAF <https://github.com/cltl/SpaCy-to-NAF>`_

Installation
------------

To install the package

::

    pip install nafigator

To install the package from Github

::

    pip install -e git+https://github.com/denederlandschebank/nafigator.git#egg=nafigator


How to run
----------

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

To parse a pdf, .docx, .txt or .html-file from the command line interface run in the root of the project::

    python -m nafigator.cli


Function calls
~~~~~~~~~~~~~~

To convert a .pdf, .docx, .txt or .html-file in Python code you can use: ::

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

Get all sentences in the document via::

  doc.sentences

Output of doc.sentences::

  [
    {'text': 'The Nafigator package allows you to store NLP output from custom made Spacy and stanza pipelines with ( intermediate ) results and all processing steps in one format .', 
    'para': ['1'], 
    'page': ['1'], 
    'span': [{'id': 'w1'}, {'id': 'w2'}, {'id': 'w3'}, {'id': 'w4'}, {'id': 'w5'}, {'id': 'w6'}, {'id': 'w7'}, {'id': 'w8'}, {'id': 'w9'}, {'id': 'w10'}, {'id': 'w11'}, {'id': 'w12'}, {'id': 'w13'}, {'id': 'w14'}, {'id': 'w15'}, {'id': 'w16'}, {'id': 'w17'}, {'id': 'w18'}, {'id': 'w19'}, {'id': 'w20'}, {'id': 'w21'}, {'id': 'w22'}, {'id': 'w23'}, {'id': 'w24'}, {'id': 'w25'}, {'id': 'w26'}, {'id': 'w27'}, {'id': 'w28'}, {'id': 'w29'}], 
    'terms': [{'id': 't1'}, {'id': 't2'}, {'id': 't3'}, {'id': 't4'}, {'id': 't5'}, {'id': 't6'}, {'id': 't7'}, {'id': 't8'}, {'id': 't9'}, {'id': 't10'}, {'id': 't11'}, {'id': 't12'}, {'id': 't13'}, {'id': 't14'}, {'id': 't15'}, {'id': 't16'}, {'id': 't17'}, {'id': 't18'}, {'id': 't19'}, {'id': 't20'}, {'id': 't21'}, {'id': 't22'}, {'id': 't23'}, {'id': 't24'}, {'id': 't25'}, {'id': 't26'}, {'id': 't27'}, {'id': 't28'}, {'id': 't29'}]}, 
  ...

Note that you get the word ids (the span) as well as the terms ids in the sentence.


Adding new annotation layers
----------------------------

To add a new annotation layer with elements, start with registering the processor of the new annotations::

  lp = ProcessorElement(name="processorname", model="modelname", version="1.0", timestamp=None, beginTimestamp=None,   endTimestamp=None, hostname=None)

  doc.add_processor_element("recommendations", lp)

Then get the layer and add subelements::

  layer = doc.layer("recommendations")

  data_recommendation = {'id': "recommendation1", 'subjectivity': 0.5, 'polarity': 0.25, 'span': ['t37', 't39']}

  element = doc.subelement(element=layer, tag="recommendation", data=data_recommendation)

  doc.add_span_element(element=element, data=data_recommendation)

Retrieve the recommendations with::

  doc.recommendations


Convert NAF to the NLP Interchange Format (NIF)
-----------------------------------------------

The `NLP Interchange Format (NIF) <https://github.com/NLP2RDF/ontologies>` is an RDF/OWL-based format that aims to achieve interoperability between NLP tools.

Here's an example::

  doc = nafigator.NafDocument().open("..//data//example.naf.xml")

  nif = nafigator.naf2nif(uri="https://mangosaurus.eu/rdf-data/nif-data/doc_1",
                          collection_uri="https://mangosaurus.eu/rdf-data/nif-data/collection",
                          doc=doc)

This results in an object that contains the rdflib Graph and can be serialized with::

  nif.graph.serialize(format="turtle"))

This results in the graph in turtle format. 

The prefixes and namespaces:

::

  @prefix dcterms: <http://purl.org/dc/terms/> .
  @prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
  @prefix olia: <http://purl.org/olia/olia.owl#> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

The nif:ContextCollection

::

  <https://mangosaurus.eu/rdf-data/nif-data/collection> a nif:ContextCollection ;
      nif:hasContext <https://mangosaurus.eu/rdf-data/nif-data/doc_1> ;
      dcterms:conformsTo <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1> .

The nif:Context (a document)

::

  <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_0_265> a nif:Context,
          nif:String ;
      nif:beginIndex "0"^^xsd:nonNegativeInteger ;
      nif:endIndex "265"^^xsd:nonNegativeInteger ;
      nif:hasSentences ( 
        <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_0_165> 
        <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_167_265> 
      ) ;
      nif:isString "The Nafigator package allows you to store NLP output from custom made Spacy and stanza  pipelines with (intermediate) results and all processing steps in one format.  Multiwords like in “we have set that out below” are recognized (depending on your NLP  processor)."^^xsd:string ;
      nif:lastSentence <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_167_265> ;
      nif:firstSentence <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_0_165> ;
      nif:referenceContext <https://mangosaurus.eu/rdf-data/nif-data/doc_1> .

The nif:Sentence

::

  <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_0_165> a nif:OffsetBasedString,
          nif:Paragraph,
          nif:Sentence ;
    nif:anchorOf "The Nafigator package allows you to store NLP output from custom made Spacy and stanza pipelines with ( intermediate ) results and all processing steps in one format ."^^xsd:string ;
    nif:beginIndex "0"^^xsd:nonNegativeInteger ;
    nif:endIndex "165"^^xsd:nonNegativeInteger ;
    nif:firstWord <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_0_3> ;
    nif:hasWords ( 
      <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_0_3> 
      <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_4_13> 
      ...
      <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_164_165> 
    ) ;
    nif:lastWord <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_164_165> ;
    nif:nextSentence <https://mangosaurus.eu/rdf-data/nif-data/doc_1#offset_167_265> ;
    nif:referenceContext <https://mangosaurus.eu/rdf-data/nif-data/doc_1> .

The nif:Word

::

  <https://mangosaurus.eu/rdf-data/nif-data/3968fc96-5750-3fdb-be58-46f182762119#offset_0_3> a nif:OffsetBasedString,
          nif:Word ;
      nif:anchorOf "The"^^xsd:string ;
      nif:beginIndex "0"^^xsd:nonNegativeInteger ;
      nif:endIndex "3"^^xsd:nonNegativeInteger ;
      nif:lemma "the"^^xsd:string ;
      nif:nextWord <https://mangosaurus.eu/rdf-data/nif-data/3968fc96-5750-3fdb-be58-46f182762119#offset_4_13> ;
      nif:oliaLink olia:Article,
          olia:Definite,
          olia:Determiner ;
      nif:referenceContext <https://mangosaurus.eu/rdf-data/nif-data/3968fc96-5750-3fdb-be58-46f182762119#offset_0_265> ;
      nif:sentence <https://mangosaurus.eu/rdf-data/nif-data/3968fc96-5750-3fdb-be58-46f182762119#offset_0_165> .

Part of speech tags and morphological features are here combined: the part-of-speech tag is *olia:Determiner*. The morphological features are *olia:Article* (the pronType:Art in terms of Universal Dependencies) and *olia:Definite* (the Definite:Def in terms of Universal Dependencies).

Changes to NIF
~~~~~~~~~~~~~~

Instead of the original RDF predicates *nif:word* and *nif:sentence* (used to link words to sentences and vice versa) I used predicates *nif:hasWord* and *nif:hasSentence* which point to a RDF collection (a linked list) of respectively word and sentences. The RDF collection maintains order of the elements and easy traversing. These predicates are not part of the original NIF ontology.
