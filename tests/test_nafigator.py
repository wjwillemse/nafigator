#!/usr/bin/env python

"""Tests for `nafigator` package."""


import unittest
from click.testing import CliRunner
from nafigator import NafDocument, parse2naf
from os.path import join

class TestNafigator(unittest.TestCase):
    """Tests for `nafigator` package."""

    def test_generate_naf(self):
        """ """
        tree = parse2naf.generate_naf(input=join("tests", "tests", "example.pdf"),
                                  engine="stanza", 
                                  language="en", 
                                  naf_version="v3.1")

        tree.write(join("tests", "tests", "example.naf.xml"))
        
    def test_header_filedesc(self):
        """ """
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.header['fileDesc']
        expected = {'creationtime': '2021-05-05T13:25:16UTC', 
                    'filename': 'tests\\tests\\example.pdf', 
                    'filetype': 'application/pdf'}
        assert actual['filename'] == expected['filename']
        assert actual['filetype'] == expected['filetype']

    def test_header_public(self):
        """ """
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.header['public']
        expected = {'{http://purl.org/dc/elements/1.1/}uri': 'tests\\tests\\example.pdf', 
                    '{http://purl.org/dc/elements/1.1/}format': 'application/pdf'}
        assert actual == expected

    # def test_header_linguistic_processors(self):
    #     naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
    #     actual = naf.header['linguisticProcessors']
    #     expected = [{'layer': 'pdftoxml', 'lps': 
    #                     [{'name': 'pdfminer-pdf2xml', 
    #                       'version': 'pdfminer_version-20200124', 
    #                       'beginTimestamp': '2021-05-05T13:25:16UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:16UTC'}]}, 
    #                 {'layer': 'pdftotext', 'lps': 
    #                     [{'name': 'pdfminer-pdf2text', 
    #                       'version': 'pdfminer_version-20200124', 
    #                       'beginTimestamp': '2021-05-05T13:25:16UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:16UTC'}]}, 
    #                 {'layer': 'formats', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}, 
    #                 {'layer': 'entities', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}, 
    #                 {'layer': 'text', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}, 
    #                 {'layer': 'terms', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}, 
    #                 {'layer': 'deps', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}, 
    #                 {'layer': 'multiwords', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}, 
    #                 {'layer': 'raw', 'lps': 
    #                     [{'name': 'stanza-model_en', 
    #                       'version': 'stanza_version-1.2', 
    #                       'beginTimestamp': '2021-05-05T13:25:18UTC', 
    #                       'endTimestamp': '2021-05-05T13:25:18UTC'}]}]

    #     assert actual == expected

    def test_formats(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.formats
        expected = [{'length': '268', 'offset': '0', 'textboxes': 
                        [{'textlines': 
                            [{'texts': 
                                [{'font': 'CIDFont+F1', 
                                  'size': '12.000', 
                                  'length': '87', 
                                  'offset': '0', 
                                  'text': 'The Nafigator package allows you to store NLP output from custom made spaCy and stanza '}]},
                             {'texts': 
                                [{'font': 'CIDFont+F1', 
                                  'size': '12.000', 
                                  'length': '77', 
                                  'offset': '88', 
                                  'text': 'pipelines with (intermediate) results and all processing steps in one format.'}]}]},
                         {'textlines': 
                            [{'texts': 
                                [{'font': 'CIDFont+F1', 
                                  'size': '12.000', 
                                  'length': '86', 
                                  'offset': '167', 
                                  'text': 'Multiwords like in “we have set that out below” are recognized (depending on your NLP '}]}, 
                             {'texts': 
                                [{'font': 'CIDFont+F1', 
                                  'size': '12.000', 
                                  'length': '11', 
                                  'offset': '254', 
                                  'text': 'processor).'}]}]}], 
                          'figures': []
                        }]

        assert actual == expected

    def test_entities(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.entities

        expected = [{'id': 'e1', 'type': 'PRODUCT', 'text': 'Nafigator', 'span': [{'id': 't2'}]}, 
                    {'id': 'e2', 'type': 'CARDINAL', 'text': 'one', 'span': [{'id': 't28'}]}]

        assert actual == expected, "expected: "+str(expected)

    def test_text(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.text
        expected = [{'text': 'The', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w1', 'length': '3', 'offset': '0'}, 
                    {'text': 'Nafigator', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w2', 'length': '9', 'offset': '4'}, 
                    {'text': 'package', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w3', 'length': '7', 'offset': '14'}, 
                    {'text': 'allows', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w4', 'length': '6', 'offset': '22'}, 
                    {'text': 'you', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w5', 'length': '3', 'offset': '29'}, 
                    {'text': 'to', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w6', 'length': '2', 'offset': '33'}, 
                    {'text': 'store', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w7', 'length': '5', 'offset': '36'}, 
                    {'text': 'NLP', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w8', 'length': '3', 'offset': '42'}, 
                    {'text': 'output', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w9', 'length': '6', 'offset': '46'}, 
                    {'text': 'from', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w10', 'length': '4', 'offset': '53'}, 
                    {'text': 'custom', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w11', 'length': '6', 'offset': '58'}, 
                    {'text': 'made', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w12', 'length': '4', 'offset': '65'}, 
                    {'text': 'spa', 'page': '1', 'para': '1', 'sent': '1', 'id': 'w13', 'length': '3', 'offset': '70'}, 
                    {'text': 'Cy', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w14', 'length': '2', 'offset': '73'}, 
                    {'text': 'and', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w15', 'length': '3', 'offset': '76'}, 
                    {'text': 'stanza', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w16', 'length': '6', 'offset': '80'},
                    {'text': 'pipelines', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w17', 'length': '9', 'offset': '88'}, 
                    {'text': 'with', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w18', 'length': '4', 'offset': '98'}, 
                    {'text': '(', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w19', 'length': '1', 'offset': '103'}, 
                    {'text': 'intermediate', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w20', 'length': '12', 'offset': '104'},
                    {'text': ')', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w21', 'length': '1', 'offset': '116'}, 
                    {'text': 'results', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w22', 'length': '7', 'offset': '118'}, 
                    {'text': 'and', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w23', 'length': '3', 'offset': '126'}, 
                    {'text': 'all', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w24', 'length': '3', 'offset': '130'},
                    {'text': 'processing', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w25', 'length': '10', 'offset': '134'}, 
                    {'text': 'steps', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w26', 'length': '5', 'offset': '145'}, 
                    {'text': 'in', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w27', 'length': '2', 'offset': '151'}, 
                    {'text': 'one', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w28', 'length': '3', 'offset': '154'}, 
                    {'text': 'format', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w29', 'length': '6', 'offset': '158'}, 
                    {'text': '.', 'page': '1', 'para': '1', 'sent': '2', 'id': 'w30', 'length': '1', 'offset': '164'}, 
                    {'text': 'Multiwords', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w31', 'length': '10', 'offset': '167'},
                    {'text': 'like', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w32', 'length': '4', 'offset': '178'}, 
                    {'text': 'in', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w33', 'length': '2', 'offset': '183'},
                    {'text': '“', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w34', 'length': '1', 'offset': '186'}, 
                    {'text': 'we', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w35', 'length': '2', 'offset': '187'},
                    {'text': 'have', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w36', 'length': '4', 'offset': '190'}, 
                    {'text': 'set', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w37', 'length': '3', 'offset': '195'}, 
                    {'text': 'that', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w38', 'length': '4', 'offset': '199'},
                    {'text': 'out', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w39', 'length': '3', 'offset': '204'},
                    {'text': 'below', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w40', 'length': '5', 'offset': '208'}, 
                    {'text': '”', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w41', 'length': '1', 'offset': '213'}, 
                    {'text': 'are', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w42', 'length': '3', 'offset': '215'}, 
                    {'text': 'recognized', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w43', 'length': '10', 'offset': '219'}, 
                    {'text': '(', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w44', 'length': '1', 'offset': '230'}, 
                    {'text': 'depending', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w45', 'length': '9', 'offset': '231'},
                    {'text': 'on', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w46', 'length': '2', 'offset': '241'}, 
                    {'text': 'your', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w47', 'length': '4', 'offset': '244'}, 
                    {'text': 'NLP', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w48', 'length': '3', 'offset': '249'}, 
                    {'text': 'processor', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w49', 'length': '9', 'offset': '254'}, 
                    {'text': ')', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w50', 'length': '1', 'offset': '263'}, 
                    {'text': '.', 'page': '1', 'para': '2', 'sent': '3', 'id': 'w51', 'length': '1', 'offset': '264'}]

        assert actual == expected

    def test_terms(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.terms
        expected = [{'id': 't1', 'lemma': 'the', 'pos': 'DET', 'type': 'open', 'morphofeat': 'Definite=Def|PronType=Art', 'span': [{'id': 'w1'}]}, 
          {'id': 't2', 'lemma': 'Nafigator', 'pos': 'PROPN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w2'}]}, 
          {'id': 't3', 'lemma': 'package', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w3'}]}, 
          {'id': 't4', 'lemma': 'allow', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin', 'span': [{'id': 'w4'}]},
          {'id': 't5', 'lemma': 'you', 'pos': 'PRON', 'type': 'open', 'morphofeat': 'Case=Acc|Person=2|PronType=Prs', 'span': [{'id': 'w5'}]}, 
          {'id': 't6', 'lemma': 'to', 'pos': 'PART', 'type': 'open', 'span': [{'id': 'w6'}]}, 
          {'id': 't7', 'lemma': 'store', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'VerbForm=Inf', 'span': [{'id': 'w7'}]}, 
          {'id': 't8', 'lemma': 'nlp', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w8'}]}, 
          {'id': 't9', 'lemma': 'output', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w9'}]}, 
          {'id': 't10', 'lemma': 'from', 'pos': 'ADP', 'type': 'open', 'span': [{'id': 'w10'}]}, 
          {'id': 't11', 'lemma': 'custom', 'pos': 'ADJ', 'type': 'open', 'morphofeat': 'Degree=Pos', 'span': [{'id': 'w11'}]}, 
          {'id': 't12', 'lemma': 'make', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'Tense=Past|VerbForm=Part', 'span': [{'id': 'w12'}]},
          {'id': 't13', 'lemma': 'spa', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w13'}]}, 
          {'id': 't14', 'lemma': 'cy', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w14'}]}, 
          {'id': 't15', 'lemma': 'and', 'pos': 'CCONJ', 'type': 'open', 'span': [{'id': 'w15'}]}, 
          {'id': 't16', 'lemma': 'stanza', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w16'}]}, 
          {'id': 't17', 'lemma': 'pipeline', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Plur', 'span': [{'id': 'w17'}]}, 
          {'id': 't18', 'lemma': 'with', 'pos': 'ADP', 'type': 'open', 'span': [{'id': 'w18'}]}, 
          {'id': 't19', 'lemma': '(', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w19'}]}, 
          {'id': 't20', 'lemma': 'intermediate', 'pos': 'ADJ', 'type': 'open', 'morphofeat': 'Degree=Pos', 'span': [{'id': 'w20'}]},
          {'id': 't21', 'lemma': ')', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w21'}]}, 
          {'id': 't22', 'lemma': 'result', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Plur', 'span': [{'id': 'w22'}]}, 
          {'id': 't23', 'lemma': 'and', 'pos': 'CCONJ', 'type': 'open', 'span': [{'id': 'w23'}]}, 
          {'id': 't24', 'lemma': 'all', 'pos': 'DET', 'type': 'open', 'span': [{'id': 'w24'}]}, 
          {'id': 't25', 'lemma': 'processing', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w25'}]}, 
          {'id': 't26', 'lemma': 'step', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Plur', 'span': [{'id': 'w26'}]}, 
          {'id': 't27', 'lemma': 'in', 'pos': 'ADP', 'type': 'open', 'span': [{'id': 'w27'}]}, 
          {'id': 't28', 'lemma': 'one', 'pos': 'NUM', 'type': 'open', 'morphofeat': 'NumType=Card', 'span': [{'id': 'w28'}]}, 
          {'id': 't29', 'lemma': 'format', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w29'}]}, 
          {'id': 't30', 'lemma': '.', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w30'}]}, 
          {'id': 't31', 'lemma': 'multiword', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Plur', 'span': [{'id': 'w31'}]}, 
          {'id': 't32', 'lemma': 'like', 'pos': 'ADP', 'type': 'open', 'span': [{'id': 'w32'}]}, 
          {'id': 't33', 'lemma': 'in', 'pos': 'ADP', 'type': 'open', 'span': [{'id': 'w33'}]},
          {'id': 't34', 'lemma': '"', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w34'}]}, 
          {'id': 't35', 'lemma': 'we', 'pos': 'PRON', 'type': 'open', 'morphofeat': 'Case=Nom|Number=Plur|Person=1|PronType=Prs', 'span': [{'id': 'w35'}]},
          {'id': 't36', 'lemma': 'have', 'pos': 'AUX', 'type': 'open', 'morphofeat': 'Mood=Ind|Tense=Pres|VerbForm=Fin', 'span': [{'id': 'w36'}]}, 
          {'id': 't37', 'lemma': 'set', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'Tense=Past|VerbForm=Part', 'component_of': 'mw1', 'span': [{'id': 'w37'}]}, 
          {'id': 't38', 'lemma': 'that', 'pos': 'SCONJ', 'type': 'open', 'span': [{'id': 'w38'}]}, 
          {'id': 't39', 'lemma': 'out', 'pos': 'ADP', 'type': 'open', 'component_of': 'mw1', 'span': [{'id': 'w39'}]},
          {'id': 't40', 'lemma': 'below', 'pos': 'ADV', 'type': 'open', 'span': [{'id': 'w40'}]}, 
          {'id': 't41', 'lemma': '"', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w41'}]}, 
          {'id': 't42', 'lemma': 'be', 'pos': 'AUX', 'type': 'open', 'morphofeat': 'Mood=Ind|Tense=Pres|VerbForm=Fin', 'span': [{'id': 'w42'}]}, 
          {'id': 't43', 'lemma': 'recognize', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'Tense=Past|VerbForm=Part|Voice=Pass', 'span': [{'id': 'w43'}]},
          {'id': 't44', 'lemma': '(', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w44'}]}, 
          {'id': 't45', 'lemma': 'depend', 'pos': 'VERB', 'type': 'open', 'morphofeat': 'VerbForm=Ger', 'span': [{'id': 'w45'}]}, 
          {'id': 't46', 'lemma': 'on', 'pos': 'ADP', 'type': 'open', 'span': [{'id': 'w46'}]}, 
          {'id': 't47', 'lemma': 'you', 'pos': 'PRON', 'type': 'open', 'morphofeat': 'Person=2|Poss=Yes|PronType=Prs', 'span': [{'id': 'w47'}]},
          {'id': 't48', 'lemma': 'nlp', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w48'}]},
          {'id': 't49', 'lemma': 'processor', 'pos': 'NOUN', 'type': 'open', 'morphofeat': 'Number=Sing', 'span': [{'id': 'w49'}]},
          {'id': 't50', 'lemma': ')', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w50'}]},
          {'id': 't51', 'lemma': '.', 'pos': 'PUNCT', 'type': 'open', 'span': [{'id': 'w51'}]}]
        assert actual == expected

    def test_dependencies(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.deps
        expected = [{'from_term': 't3', 'to_term': 't1', 'rfunc': 'det'}, 
                    {'from_term': 't4', 'to_term': 't3', 'rfunc': 'nsubj'}, 
                    {'from_term': 't3', 'to_term': 't2', 'rfunc': 'compound'}, 
                    {'from_term': 't4', 'to_term': 't5', 'rfunc': 'obj'}, 
                    {'from_term': 't7', 'to_term': 't6', 'rfunc': 'mark'}, 
                    {'from_term': 't4', 'to_term': 't7', 'rfunc': 'xcomp'}, 
                    {'from_term': 't9', 'to_term': 't8', 'rfunc': 'compound'}, 
                    {'from_term': 't7', 'to_term': 't9', 'rfunc': 'obj'}, 
                    {'from_term': 't13', 'to_term': 't10', 'rfunc': 'case'}, 
                    {'from_term': 't7', 'to_term': 't13', 'rfunc': 'obl'}, 
                    {'from_term': 't12', 'to_term': 't11', 'rfunc': 'compound'}, 
                    {'from_term': 't13', 'to_term': 't12', 'rfunc': 'amod'}, 
                    {'from_term': 't17', 'to_term': 't14', 'rfunc': 'compound'}, 
                    {'from_term': 't16', 'to_term': 't15', 'rfunc': 'cc'}, 
                    {'from_term': 't14', 'to_term': 't16', 'rfunc': 'conj'}, 
                    {'from_term': 't22', 'to_term': 't18', 'rfunc': 'case'}, 
                    {'from_term': 't17', 'to_term': 't22', 'rfunc': 'nmod'},
                    {'from_term': 't22', 'to_term': 't19', 'rfunc': 'punct'},
                    {'from_term': 't22', 'to_term': 't20', 'rfunc': 'amod'}, 
                    {'from_term': 't22', 'to_term': 't21', 'rfunc': 'punct'}, 
                    {'from_term': 't26', 'to_term': 't23', 'rfunc': 'cc'}, 
                    {'from_term': 't22', 'to_term': 't26', 'rfunc': 'conj'}, 
                    {'from_term': 't26', 'to_term': 't24', 'rfunc': 'det'},
                    {'from_term': 't26', 'to_term': 't25', 'rfunc': 'compound'}, 
                    {'from_term': 't29', 'to_term': 't27', 'rfunc': 'case'}, 
                    {'from_term': 't26', 'to_term': 't29', 'rfunc': 'nmod'}, 
                    {'from_term': 't29', 'to_term': 't28', 'rfunc': 'nummod'}, 
                    {'from_term': 't17', 'to_term': 't30', 'rfunc': 'punct'}, 
                    {'from_term': 't37', 'to_term': 't32', 'rfunc': 'mark'}, 
                    {'from_term': 't31', 'to_term': 't37', 'rfunc': 'acl'}, 
                    {'from_term': 't37', 'to_term': 't33', 'rfunc': 'mark'}, 
                    {'from_term': 't37', 'to_term': 't34', 'rfunc': 'punct'},
                    {'from_term': 't37', 'to_term': 't35', 'rfunc': 'nsubj'}, 
                    {'from_term': 't37', 'to_term': 't36', 'rfunc': 'aux'}, 
                    {'from_term': 't43', 'to_term': 't38', 'rfunc': 'mark'}, 
                    {'from_term': 't37', 'to_term': 't43', 'rfunc': 'ccomp'}, 
                    {'from_term': 't37', 'to_term': 't39', 'rfunc': 'compound:prt'}, 
                    {'from_term': 't37', 'to_term': 't40', 'rfunc': 'advmod'},
                    {'from_term': 't37', 'to_term': 't41', 'rfunc': 'punct'}, 
                    {'from_term': 't43', 'to_term': 't42', 'rfunc': 'aux:pass'},
                    {'from_term': 't49', 'to_term': 't44', 'rfunc': 'punct'},
                    {'from_term': 't43', 'to_term': 't49', 'rfunc': 'obl'}, 
                    {'from_term': 't49', 'to_term': 't45', 'rfunc': 'case'}, 
                    {'from_term': 't49', 'to_term': 't46', 'rfunc': 'case'}, 
                    {'from_term': 't49', 'to_term': 't47', 'rfunc': 'nmod:poss'},
                    {'from_term': 't49', 'to_term': 't48', 'rfunc': 'compound'},
                    {'from_term': 't49', 'to_term': 't50', 'rfunc': 'punct'},
                    {'from_term': 't43', 'to_term': 't51', 'rfunc': 'punct'}]

        assert actual == expected

    def test_multiwords(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.multiwords
        expected = [{'id': 'mw1', 'lemma': 'set_out', 'pos': 'VERB', 'type': 'phrasal', 'components': 
                        [{'id': 'mw1.c1', 'span': [{'id': 't37'}]}, 
                         {'id': 'mw1.c2', 'span': [{'id': 't39'}]}]}]
        assert actual == expected

    def test_raw(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.raw
        expected = "The Nafigator package allows you to store NLP output from custom made spaCy and stanza  pipelines with (intermediate) results and all processing steps in one format.  Multiwords like in “we have set that out below” are recognized (depending on your NLP  processor)."
        assert actual == expected

      # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     # assert 'nafigator.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
