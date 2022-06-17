#!/usr/bin/env python

"""Tests for `nafigator` package."""


import os
from os.path import join
from nafigator import NafDocument, parse2naf
from click.testing import CliRunner
from deepdiff import DeepDiff
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class TestNafigator_pdf(unittest.TestCase):
    """Tests for `nafigator` package."""

    def test_1_pdf_generate_naf(self):
        """ """
        tree = parse2naf.generate_naf(
            input="tests" + os.sep + "tests" + os.sep + "example.pdf",
            engine="stanza",
            language="en",
            naf_version="v3.1",
            dtd_validation=False,
            params={},
            nlp=None,
        )
        assert (
            tree.write("tests" + os.sep + "tests" + os.sep + "example.naf.xml") == None
        )

    def test_1_split_pre_linguistic(self):
        """ """
        # only save the preprocess steps
        tree = parse2naf.generate_naf(
            input=join("tests", "tests", "example.pdf"),
            engine="stanza",
            language="en",
            naf_version="v3.1",
            dtd_validation=False,
            params={"linguistic_layers": []},
            nlp=None,
        )
        tree.write(join("tests", "tests", "example_preprocess.naf.xml")) == None

        # start with saved document and process linguistic steps
        naf = NafDocument().open(join("tests", "tests", "example_preprocess.naf.xml"))
        tree = parse2naf.generate_naf(
            input=naf,
            engine="stanza",
            language="en",
            naf_version="v3.1",
            params={"preprocess_layers": []},
        )

        doc = NafDocument().open(join("tests", "tests", "example.naf.xml"))

        assert tree.raw == doc.raw

    def test_2_pdf_header_filedesc(self):
        """ """
        naf = NafDocument().open(
            "tests" + os.sep + "tests" + os.sep + "example.naf.xml"
        )
        actual = naf.header["fileDesc"]
        expected = {
            "filename": "tests" + os.sep + "tests" + os.sep + "example.pdf",
            "filetype": "application/pdf",
        }
        assert actual["filename"] == expected["filename"]
        assert actual["filetype"] == expected["filetype"]

    def test_3_pdf_header_public(self):
        """ """
        naf = NafDocument().open(
            "tests" + os.sep + "tests" + os.sep + "example.naf.xml"
        )
        actual = naf.header["public"]
        expected = {
            "{http://purl.org/dc/elements/1.1/}uri": "tests"
            + os.sep
            + "tests"
            + os.sep
            + "example.pdf",
            "{http://purl.org/dc/elements/1.1/}format": "application/pdf",
        }
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    # def test_4_pdf_header_linguistic_processors(self):
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

    # assert actual == expected, "expected: "+str(expected)+", actual: "+str(actual)

    def test_5_pdf_formats(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.formats
        expected = [
            {
                "length": "268",
                "offset": "0",
                "textboxes": [
                    {
                        "textlines": [
                            {
                                "texts": [
                                    {
                                        "font": "CIDFont+F1",
                                        "size": "12.000",
                                        "length": "87",
                                        "offset": "0",
                                        "text": "The Nafigator package allows you to store NLP output from custom made spaCy and stanza ",
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "CIDFont+F1",
                                        "size": "12.000",
                                        "length": "77",
                                        "offset": "88",
                                        "text": "pipelines with (intermediate) results and all processing steps in one format.",
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        "textlines": [
                            {
                                "texts": [
                                    {
                                        "font": "CIDFont+F1",
                                        "size": "12.000",
                                        "length": "86",
                                        "offset": "167",
                                        "text": "Multiwords like in “we have set that out below” are recognized (depending on your NLP ",
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "CIDFont+F1",
                                        "size": "12.000",
                                        "length": "11",
                                        "offset": "254",
                                        "text": "processor).",
                                    }
                                ]
                            },
                        ]
                    },
                ],
                "figures": [],
                "headers": [],
                "tables": [],
            }
        ]

        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_6_pdf_entities(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.entities
        expected = [
            {
                "id": "e1",
                "type": "PRODUCT",
                "text": "Nafigator",
                "span": [{"id": "t2"}],
            },
            {"id": "e2", "type": "CARDINAL", "text": "one", "span": [{"id": "t27"}]},
        ]

        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_7_pdf_text(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.text
        expected = [
            {
                "text": "The",
                "id": "w1",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "0",
                "length": "3",
            },
            {
                "text": "Nafigator",
                "id": "w2",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "4",
                "length": "9",
            },
            {
                "text": "package",
                "id": "w3",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "14",
                "length": "7",
            },
            {
                "text": "allows",
                "id": "w4",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "22",
                "length": "6",
            },
            {
                "text": "you",
                "id": "w5",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "29",
                "length": "3",
            },
            {
                "text": "to",
                "id": "w6",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "33",
                "length": "2",
            },
            {
                "text": "store",
                "id": "w7",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "36",
                "length": "5",
            },
            {
                "text": "NLP",
                "id": "w8",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "42",
                "length": "3",
            },
            {
                "text": "output",
                "id": "w9",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "46",
                "length": "6",
            },
            {
                "text": "from",
                "id": "w10",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "53",
                "length": "4",
            },
            {
                "text": "custom",
                "id": "w11",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "58",
                "length": "6",
            },
            {
                "text": "made",
                "id": "w12",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "65",
                "length": "4",
            },
            {
                "text": "spaCy",
                "id": "w13",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "70",
                "length": "5",
            },
            {
                "text": "and",
                "id": "w14",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "76",
                "length": "3",
            },
            {
                "text": "stanza",
                "id": "w15",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "80",
                "length": "6",
            },
            {
                "text": "pipelines",
                "id": "w16",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "88",
                "length": "9",
            },
            {
                "text": "with",
                "id": "w17",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "98",
                "length": "4",
            },
            {
                "text": "(",
                "id": "w18",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "103",
                "length": "1",
            },
            {
                "text": "intermediate",
                "id": "w19",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "104",
                "length": "12",
            },
            {
                "text": ")",
                "id": "w20",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "116",
                "length": "1",
            },
            {
                "text": "results",
                "id": "w21",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "118",
                "length": "7",
            },
            {
                "text": "and",
                "id": "w22",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "126",
                "length": "3",
            },
            {
                "text": "all",
                "id": "w23",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "130",
                "length": "3",
            },
            {
                "text": "processing",
                "id": "w24",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "134",
                "length": "10",
            },
            {
                "text": "steps",
                "id": "w25",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "145",
                "length": "5",
            },
            {
                "text": "in",
                "id": "w26",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "151",
                "length": "2",
            },
            {
                "text": "one",
                "id": "w27",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "154",
                "length": "3",
            },
            {
                "text": "format",
                "id": "w28",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "158",
                "length": "6",
            },
            {
                "text": ".",
                "id": "w29",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "164",
                "length": "1",
            },
            {
                "text": "Multiwords",
                "id": "w30",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "167",
                "length": "10",
            },
            {
                "text": "like",
                "id": "w31",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "178",
                "length": "4",
            },
            {
                "text": "in",
                "id": "w32",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "183",
                "length": "2",
            },
            {
                "text": "“",
                "id": "w33",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "186",
                "length": "1",
            },
            {
                "text": "we",
                "id": "w34",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "187",
                "length": "2",
            },
            {
                "text": "have",
                "id": "w35",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "190",
                "length": "4",
            },
            {
                "text": "set",
                "id": "w36",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "195",
                "length": "3",
            },
            {
                "text": "that",
                "id": "w37",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "199",
                "length": "4",
            },
            {
                "text": "out",
                "id": "w38",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "204",
                "length": "3",
            },
            {
                "text": "below",
                "id": "w39",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "208",
                "length": "5",
            },
            {
                "text": "”",
                "id": "w40",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "213",
                "length": "1",
            },
            {
                "text": "are",
                "id": "w41",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "215",
                "length": "3",
            },
            {
                "text": "recognized",
                "id": "w42",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "219",
                "length": "10",
            },
            {
                "text": "(",
                "id": "w43",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "230",
                "length": "1",
            },
            {
                "text": "depending",
                "id": "w44",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "231",
                "length": "9",
            },
            {
                "text": "on",
                "id": "w45",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "241",
                "length": "2",
            },
            {
                "text": "your",
                "id": "w46",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "244",
                "length": "4",
            },
            {
                "text": "NLP",
                "id": "w47",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "249",
                "length": "3",
            },
            {
                "text": "processor",
                "id": "w48",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "254",
                "length": "9",
            },
            {
                "text": ")",
                "id": "w49",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "263",
                "length": "1",
            },
            {
                "text": ".",
                "id": "w50",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "264",
                "length": "1",
            },
        ]
        diff = DeepDiff(actual, expected)
        assert diff == dict(), diff

    def test_8_pdf_terms(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.terms

        expected = [
            {
                "id": "t1",
                "type": "open",
                "lemma": "the",
                "pos": "DET",
                "morphofeat": "Definite=Def|PronType=Art",
                "span": [{"id": "w1"}],
            },
            {
                "id": "t2",
                "type": "open",
                "lemma": "Nafigator",
                "pos": "PROPN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w2"}],
            },
            {
                "id": "t3",
                "type": "open",
                "lemma": "package",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w3"}],
            },
            {
                "id": "t4",
                "type": "open",
                "lemma": "allow",
                "pos": "VERB",
                "morphofeat": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w4"}],
            },
            {
                "id": "t5",
                "type": "open",
                "lemma": "you",
                "pos": "PRON",
                "morphofeat": "Case=Acc|Person=2|PronType=Prs",
                "span": [{"id": "w5"}],
            },
            {
                "id": "t6",
                "type": "open",
                "lemma": "to",
                "pos": "PART",
                "span": [{"id": "w6"}],
            },
            {
                "id": "t7",
                "type": "open",
                "lemma": "store",
                "pos": "VERB",
                "morphofeat": "VerbForm=Inf",
                "span": [{"id": "w7"}],
            },
            {
                'id': 't8',
                'type': 'open',
                'lemma': 'NLP',
                'pos': 'PROPN',
                'morphofeat': 'Number=Sing',
                'span': [{'id': 'w8'}],
            },
            {
                "id": "t9",
                "type": "open",
                "lemma": "output",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w9"}],
            },
            {
                "id": "t10",
                "type": "open",
                "lemma": "from",
                "pos": "ADP",
                "span": [{"id": "w10"}],
            },
            {
                'id': 't11',
                'type': 'open',
                'lemma': 'custom',
                'pos': 'NOUN',
                'morphofeat': 'Number=Sing',
                'span': [{'id': 'w11'}],
            },
            {
                "id": "t12",
                "type": "open",
                "lemma": "make",
                "pos": "VERB",
                "morphofeat": "Tense=Past|VerbForm=Part",
                "span": [{"id": "w12"}],
            },
            {'id': 't13',
             'type': 'open',
             'lemma': 'spacy',
             'pos': 'ADJ',
             'morphofeat': 'Degree=Pos',
             'span': [{'id': 'w13'}],
             },
            {
                "id": "t14",
                "type": "open",
                "lemma": "and",
                "pos": "CCONJ",
                "span": [{"id": "w14"}],
            },
            {
                "id": "t15",
                "type": "open",
                "lemma": "stanza",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w15"}],
            },
            {
                "id": "t16",
                "type": "open",
                "lemma": "pipeline",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w16"}],
            },
            {
                "id": "t17",
                "type": "open",
                "lemma": "with",
                "pos": "ADP",
                "span": [{"id": "w17"}],
            },
            {
                "id": "t18",
                "type": "open",
                "lemma": "(",
                "pos": "PUNCT",
                "span": [{"id": "w18"}],
            },
            {
                "id": "t19",
                "type": "open",
                "lemma": "intermediate",
                "pos": "ADJ",
                "morphofeat": "Degree=Pos",
                "span": [{"id": "w19"}],
            },
            {
                "id": "t20",
                "type": "open",
                "lemma": ")",
                "pos": "PUNCT",
                "span": [{"id": "w20"}],
            },
            {
                "id": "t21",
                "type": "open",
                "lemma": "result",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w21"}],
            },
            {
                "id": "t22",
                "type": "open",
                "lemma": "and",
                "pos": "CCONJ",
                "span": [{"id": "w22"}],
            },
            {
                "id": "t23",
                "type": "open",
                "lemma": "all",
                "pos": "DET",
                "span": [{"id": "w23"}],
            },
            {
                "id": "t24",
                "type": "open",
                "lemma": "processing",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w24"}],
            },
            {
                "id": "t25",
                "type": "open",
                "lemma": "step",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w25"}],
            },
            {
                "id": "t26",
                "type": "open",
                "lemma": "in",
                "pos": "ADP",
                "span": [{"id": "w26"}],
            },
            {
                "id": "t27",
                "type": "open",
                "lemma": "one",
                "pos": "NUM",
                "morphofeat": "NumType=Card",
                "span": [{"id": "w27"}],
            },
            {
                "id": "t28",
                "type": "open",
                "lemma": "format",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w28"}],
            },
            {
                "id": "t29",
                "type": "open",
                "lemma": ".",
                "pos": "PUNCT",
                "span": [{"id": "w29"}],
            },
            {
                "id": "t30",
                "type": "open",
                "lemma": "multiword",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w30"}],
            },
            {
                'id': 't31',
                'type': 'open',
                'lemma': 'like',
                'pos': 'VERB',
                'morphofeat': 'Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin',
                'span': [{'id': 'w31'}],
            },
            {
                "id": "t32",
                "type": "open",
                "lemma": "in",
                "pos": "ADP",
                "span": [{"id": "w32"}],
            },
            {
                "id": "t33",
                "type": "open",
                "lemma": "''",
                "pos": "PUNCT",
                "span": [{"id": "w33"}],
            },
            {
                "id": "t34",
                "type": "open",
                "lemma": "we",
                "pos": "PRON",
                "morphofeat": "Case=Nom|Number=Plur|Person=1|PronType=Prs",
                "span": [{"id": "w34"}],
            },
            {
                'id': 't35',
                'type': 'open',
                'lemma': 'have',
                'pos': 'AUX',
                'morphofeat': 'Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin',
                'span': [{'id': 'w35'}],
            },
            {
                "id": "t36",
                "type": "open",
                "lemma": "set",
                "pos": "VERB",
                "morphofeat": "Tense=Past|VerbForm=Part",
                "component_of": "mw1",
                "span": [{"id": "w36"}],
            },
            {
                "id": "t37",
                "type": "open",
                "lemma": "that",
                "pos": "PRON",
                "morphofeat": "Number=Sing|PronType=Dem",
                "span": [{"id": "w37"}],
            },
            {
                "id": "t38",
                "type": "open",
                "lemma": "out",
                "pos": "ADP",
                "component_of": "mw1",
                "span": [{"id": "w38"}],
            },
            {
                "id": "t39",
                "type": "open",
                "lemma": "below",
                "pos": "ADV",
                "span": [{"id": "w39"}],
            },
            {
                "id": "t40",
                "type": "open",
                "lemma": "''",
                "pos": "PUNCT",
                "span": [{"id": "w40"}],
            },
            {
                'id': 't41',
                'type': 'open',
                'lemma': 'be',
                'pos': 'AUX',
                'morphofeat': 'Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin',
                'span': [{'id': 'w41'}],
            },
            {
                "id": "t42",
                "type": "open",
                "lemma": "recognize",
                "pos": "VERB",
                "morphofeat": "Tense=Past|VerbForm=Part|Voice=Pass",
                "span": [{"id": "w42"}],
            },
            {
                "id": "t43",
                "type": "open",
                "lemma": "(",
                "pos": "PUNCT",
                "span": [{"id": "w43"}],
            },
            {
                "id": "t44",
                "type": "open",
                "lemma": "depend",
                "pos": "VERB",
                "morphofeat": "VerbForm=Ger",
                "span": [{"id": "w44"}],
            },
            {
                "id": "t45",
                "type": "open",
                "lemma": "on",
                "pos": "ADP",
                "span": [{"id": "w45"}],
            },
            {
                "id": "t46",
                "type": "open",
                "lemma": "you",
                "pos": "PRON",
                "morphofeat": "Person=2|Poss=Yes|PronType=Prs",
                "span": [{"id": "w46"}],
            },
            {
                "id": "t47",
                "type": "open",
                "lemma": "nlp",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w47"}],
            },
            {
                "id": "t48",
                "type": "open",
                "lemma": "processor",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w48"}],
            },
            {
                "id": "t49",
                "type": "open",
                "lemma": ")",
                "pos": "PUNCT",
                "span": [{"id": "w49"}],
            },
            {
                "id": "t50",
                "type": "open",
                "lemma": ".",
                "pos": "PUNCT",
                "span": [{"id": "w50"}],
            },
        ]

        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_9_pdf_dependencies(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.deps

        expected = [
            {"from_term": "t3", "to_term": "t1", "rfunc": "det"},
            {"from_term": "t4", "to_term": "t3", "rfunc": "nsubj"},
            {"from_term": "t3", "to_term": "t2", "rfunc": "compound"},
            {"from_term": "t4", "to_term": "t5", "rfunc": "obj"},
            {"from_term": "t7", "to_term": "t6", "rfunc": "mark"},
            {"from_term": "t4", "to_term": "t7", "rfunc": "xcomp"},
            {"from_term": "t9", "to_term": "t8", "rfunc": "compound"},
            {"from_term": "t7", "to_term": "t9", "rfunc": "obj"},
            {'from_term': 't11', 'to_term': 't10', 'rfunc': 'case'},
            {'from_term': 't7', 'to_term': 't11', 'rfunc': 'obl'},
            {'from_term': 't11', 'to_term': 't12', 'rfunc': 'acl'},
            {'from_term': 't16', 'to_term': 't13', 'rfunc': 'amod'},
            {'from_term': 't12', 'to_term': 't16', 'rfunc': 'obj'},
            {'from_term': 't15', 'to_term': 't14', 'rfunc': 'cc'},
            {'from_term': 't13', 'to_term': 't15', 'rfunc': 'conj'},
            {"from_term": "t21", "to_term": "t17", "rfunc": "case"},
            {'from_term': 't16', 'to_term': 't21', 'rfunc': 'nmod'},
            {"from_term": "t19", "to_term": "t18", "rfunc": "punct"},
            {"from_term": "t21", "to_term": "t19", "rfunc": "amod"},
            {"from_term": "t19", "to_term": "t20", "rfunc": "punct"},
            {"from_term": "t25", "to_term": "t22", "rfunc": "cc"},
            {"from_term": "t21", "to_term": "t25", "rfunc": "conj"},
            {"from_term": "t25", "to_term": "t23", "rfunc": "det"},
            {"from_term": "t25", "to_term": "t24", "rfunc": "compound"},
            {"from_term": "t28", "to_term": "t26", "rfunc": "case"},
            {"from_term": "t25", "to_term": "t28", "rfunc": "nmod"},
            {"from_term": "t28", "to_term": "t27", "rfunc": "nummod"},
            {"from_term": "t4", "to_term": "t29", "rfunc": "punct"},
            {'from_term': 't31', 'to_term': 't30', 'rfunc': 'nsubj'},
            {'from_term': 't36', 'to_term': 't32', 'rfunc': 'mark'},
            {"from_term": "t42", "to_term": "t36", "rfunc": "advcl"},
            {'from_term': 't31', 'to_term': 't42', 'rfunc': 'ccomp'},
            {"from_term": "t36", "to_term": "t33", "rfunc": "punct"},
            {"from_term": "t36", "to_term": "t34", "rfunc": "nsubj"},
            {"from_term": "t36", "to_term": "t35", "rfunc": "aux"},
            {"from_term": "t36", "to_term": "t37", "rfunc": "obj"},
            {"from_term": "t36", "to_term": "t38", "rfunc": "compound:prt"},
            {"from_term": "t36", "to_term": "t39", "rfunc": "advmod"},
            {"from_term": "t36", "to_term": "t40", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t41", "rfunc": "aux:pass"},
            {"from_term": "t48", "to_term": "t43", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t48", "rfunc": "obl"},
            {"from_term": "t48", "to_term": "t44", "rfunc": "case"},
            {"from_term": "t44", "to_term": "t45", "rfunc": "fixed"},
            {"from_term": "t48", "to_term": "t46", "rfunc": "nmod:poss"},
            {"from_term": "t48", "to_term": "t47", "rfunc": "compound"},
            {"from_term": "t48", "to_term": "t49", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t50", "rfunc": "punct"},
        ]

        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_10_pdf_multiwords(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.multiwords
        expected = [
            {
                "id": "mw1",
                "lemma": "set_out",
                "pos": "VERB",
                "type": "phrasal",
                "components": [
                    {"id": "mw1.c1", "span": [{"id": "t36"}]},
                    {"id": "mw1.c2", "span": [{"id": "t38"}]},
                ],
            }
        ]
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_11_raw(self):
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.raw
        expected = "The Nafigator package allows you to store NLP output from custom made spaCy and stanza  pipelines with (intermediate) results and all processing steps in one format.  Multiwords like in “we have set that out below” are recognized (depending on your NLP  processor)."
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_12_tables(self):
        doc = parse2naf.generate_naf(
            input="tests" + os.sep + "tests" + os.sep + "example_tables.pdf",
            engine="stanza",
            language="en",
            naf_version="v3.1",
            dtd_validation=False,
            params={"parse_tables_with_camelot": True},
            nlp=None,
        )
        doc.write(
            "tests" + os.sep + "tests" + os.sep + "example_tables.naf.xml"
        ) == None
        assert doc.raw[109: 109 + 44] == "2020/08/20 | Lorem ipsum test text | HM | Q2"
        assert (
            doc.raw[154: 154 + 49]
            == "2020/05/27 | Test text lorem ipsum | JR | Ongoing"
        )
        assert doc.formats[0]["tables"] == [
            {
                "page": "1",
                "order": "1",
                "shape": "(5, 4)",
                "table": [
                    {
                        "row": [
                            {"index": "0"},
                            {"cell": "Datum"},
                            {"cell": "Openstaande actiepunten"},
                            {"cell": "Actiehouder"},
                            {"cell": "Gereed"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "1"},
                            {"cell": "2020/08/20"},
                            {"cell": "Lorem ipsum test text"},
                            {"cell": "HM"},
                            {"cell": "Q2"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "2"},
                            {"cell": "2020/05/27"},
                            {"cell": "Test text lorem ipsum"},
                            {"cell": "JR"},
                            {"cell": "Ongoing"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "3"},
                            {"cell": "2021/02/29"},
                            {"cell": "Ipsum Lorem Test Text"},
                            {"cell": "WR"},
                            {"cell": "Ongoing"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "4"},
                            {"cell": "2021/04/28"},
                            {"cell": "Kirn Ipsyum Test test test"},
                            {"cell": "WJ"},
                            {"cell": "10-08-2022"},
                        ]
                    },
                ]
            },
            {
                "page": "1",
                "order": "2",
                "shape": "(5, 4)",
                "table": [
                    {
                        "row": [
                            {"index": "0"},
                            {"cell": "atum"},
                            {"cell": "Gesloten actiepunten"},
                            {"cell": "Actiehouder"},
                            {"cell": "Gereed"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "1"},
                            {"cell": "2022/01/10"},
                            {"cell": "Lorem ipsum test text"},
                            {"cell": "HM"},
                            {"cell": "Q2"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "2"},
                            {"cell": "2022/02/11"},
                            {"cell": "Test text lorem ipsum"},
                            {"cell": "JR"},
                            {"cell": "Ongoing"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "3"},
                            {"cell": "2022/03/12"},
                            {"cell": "Ipsum Lorem Test Text"},
                            {"cell": "WR"},
                            {"cell": "Ongoing"},
                        ]
                    },
                    {
                        "row": [
                            {"index": "4"},
                            {"cell": "2022/04/13"},
                            {"cell": "Kirn Ipsyum Test test test"},
                            {"cell": "WJ"},
                            {"cell": "10-08-2022"},
                        ]
                    },
                ]
            },
        ]

    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     # assert 'nafigator.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output


class TestNafigator_docx(unittest.TestCase):
    def test_1_docx_generate_naf(self):
        """ """
        tree = parse2naf.generate_naf(
            input=join("tests", "tests", "example.docx"),
            engine="stanza",
            language="en",
            naf_version="v3.1",
            dtd_validation=False,
            params={},
            nlp=None,
        )
        assert tree.write(join("tests", "tests", "example.docx.naf.xml")) == None

    def test_2_docx_header_filedesc(self):
        """ """
        naf = NafDocument().open(
            "tests" + os.sep + "tests" + os.sep + "example.docx.naf.xml"
        )
        actual = naf.header["fileDesc"]
        expected = {
            "filename": "tests" + os.sep + "tests" + os.sep + "example.docx",
            "filetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        assert actual["filename"] == expected["filename"]
        assert actual["filetype"] == expected["filetype"]

    def test_3_docx_header_public(self):
        """ """
        naf = NafDocument().open(
            "tests" + os.sep + "tests" + os.sep + "example.docx.naf.xml"
        )
        actual = naf.header["public"]
        expected = {
            "{http://purl.org/dc/elements/1.1/}uri": "tests"
            + os.sep
            + "tests"
            + os.sep
            + "example.docx",
            "{http://purl.org/dc/elements/1.1/}format": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    # def test_5_formats(self):

    #     assert actual == expected

    def test_6_docx_entities(self):
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.entities
        expected = [
            {
                "id": "e1",
                "type": "PRODUCT",
                "text": "Nafigator",
                "span": [{"id": "t2"}],
            },
            {"id": "e2", "type": "PRODUCT", "text": "Spacy", "span": [{"id": "t13"}]},
            {"id": "e3", "type": "CARDINAL", "text": "one", "span": [{"id": "t27"}]},
        ]
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_7_docx_text(self):
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.text
        expected = [
            {
                "text": "The",
                "id": "w1",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "0",
                "length": "3",
            },
            {
                "text": "Nafigator",
                "id": "w2",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "4",
                "length": "9",
            },
            {
                "text": "package",
                "id": "w3",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "14",
                "length": "7",
            },
            {
                "text": "allows",
                "id": "w4",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "22",
                "length": "6",
            },
            {
                "text": "you",
                "id": "w5",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "29",
                "length": "3",
            },
            {
                "text": "to",
                "id": "w6",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "33",
                "length": "2",
            },
            {
                "text": "store",
                "id": "w7",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "36",
                "length": "5",
            },
            {
                "text": "NLP",
                "id": "w8",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "42",
                "length": "3",
            },
            {
                "text": "output",
                "id": "w9",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "46",
                "length": "6",
            },
            {
                "text": "from",
                "id": "w10",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "53",
                "length": "4",
            },
            {
                "text": "custom",
                "id": "w11",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "58",
                "length": "6",
            },
            {
                "text": "made",
                "id": "w12",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "65",
                "length": "4",
            },
            {
                "text": "Spacy",
                "id": "w13",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "70",
                "length": "5",
            },
            {
                "text": "and",
                "id": "w14",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "76",
                "length": "3",
            },
            {
                "text": "stanza",
                "id": "w15",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "80",
                "length": "6",
            },
            {
                "text": "pipelines",
                "id": "w16",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "87",
                "length": "9",
            },
            {
                "text": "with",
                "id": "w17",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "97",
                "length": "4",
            },
            {
                "text": "(",
                "id": "w18",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "102",
                "length": "1",
            },
            {
                "text": "intermediate",
                "id": "w19",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "103",
                "length": "12",
            },
            {
                "text": ")",
                "id": "w20",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "115",
                "length": "1",
            },
            {
                "text": "results",
                "id": "w21",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "117",
                "length": "7",
            },
            {
                "text": "and",
                "id": "w22",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "125",
                "length": "3",
            },
            {
                "text": "all",
                "id": "w23",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "129",
                "length": "3",
            },
            {
                "text": "processing",
                "id": "w24",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "133",
                "length": "10",
            },
            {
                "text": "steps",
                "id": "w25",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "144",
                "length": "5",
            },
            {
                "text": "in",
                "id": "w26",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "150",
                "length": "2",
            },
            {
                "text": "one",
                "id": "w27",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "153",
                "length": "3",
            },
            {
                "text": "format",
                "id": "w28",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "157",
                "length": "6",
            },
            {
                "text": ".",
                "id": "w29",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "163",
                "length": "1",
            },
            {
                "text": "Multiwords",
                "id": "w30",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "166",
                "length": "10",
            },
            {
                "text": "like",
                "id": "w31",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "177",
                "length": "4",
            },
            {
                "text": "in",
                "id": "w32",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "182",
                "length": "2",
            },
            {
                "text": "“",
                "id": "w33",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "185",
                "length": "1",
            },
            {
                "text": "we",
                "id": "w34",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "186",
                "length": "2",
            },
            {
                "text": "have",
                "id": "w35",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "189",
                "length": "4",
            },
            {
                "text": "set",
                "id": "w36",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "194",
                "length": "3",
            },
            {
                "text": "that",
                "id": "w37",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "198",
                "length": "4",
            },
            {
                "text": "out",
                "id": "w38",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "203",
                "length": "3",
            },
            {
                "text": "below",
                "id": "w39",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "207",
                "length": "5",
            },
            {
                "text": "”",
                "id": "w40",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "212",
                "length": "1",
            },
            {
                "text": "are",
                "id": "w41",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "214",
                "length": "3",
            },
            {
                "text": "recognized",
                "id": "w42",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "218",
                "length": "10",
            },
            {
                "text": "(",
                "id": "w43",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "229",
                "length": "1",
            },
            {
                "text": "depending",
                "id": "w44",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "230",
                "length": "9",
            },
            {
                "text": "on",
                "id": "w45",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "240",
                "length": "2",
            },
            {
                "text": "your",
                "id": "w46",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "243",
                "length": "4",
            },
            {
                "text": "NLP",
                "id": "w47",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "248",
                "length": "3",
            },
            {
                "text": "processor",
                "id": "w48",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "252",
                "length": "9",
            },
            {
                "text": ")",
                "id": "w49",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "261",
                "length": "1",
            },
            {
                "text": ".",
                "id": "w50",
                "sent": "2",
                "para": "2",
                "page": "1",
                "offset": "262",
                "length": "1",
            },
        ]
        diff = DeepDiff(actual, expected)
        assert diff == dict(), diff

    def test_8_docx_terms(self):
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.terms

        expected = [
            {
                "id": "t1",
                "type": "open",
                "lemma": "the",
                "pos": "DET",
                "morphofeat": "Definite=Def|PronType=Art",
                "span": [{"id": "w1"}],
            },
            {
                "id": "t2",
                "type": "open",
                "lemma": "Nafigator",
                "pos": "PROPN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w2"}],
            },
            {
                "id": "t3",
                "type": "open",
                "lemma": "package",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w3"}],
            },
            {
                "id": "t4",
                "type": "open",
                "lemma": "allow",
                "pos": "VERB",
                "morphofeat": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w4"}],
            },
            {
                "id": "t5",
                "type": "open",
                "lemma": "you",
                "pos": "PRON",
                "morphofeat": "Case=Acc|Person=2|PronType=Prs",
                "span": [{"id": "w5"}],
            },
            {
                "id": "t6",
                "type": "open",
                "lemma": "to",
                "pos": "PART",
                "span": [{"id": "w6"}],
            },
            {
                "id": "t7",
                "type": "open",
                "lemma": "store",
                "pos": "VERB",
                "morphofeat": "VerbForm=Inf",
                "span": [{"id": "w7"}],
            },
            {
                "id": "t8",
                "type": "open",
                "lemma": "nlp",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w8"}],
            },
            {
                "id": "t9",
                "type": "open",
                "lemma": "output",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w9"}],
            },
            {
                "id": "t10",
                "type": "open",
                "lemma": "from",
                "pos": "ADP",
                "span": [{"id": "w10"}],
            },
            {
                "id": "t11",
                "type": "open",
                "lemma": "custom",
                "pos": "ADJ",
                "morphofeat": "Degree=Pos",
                "span": [{"id": "w11"}],
            },
            {
                "id": "t12",
                "type": "open",
                "lemma": "make",
                "pos": "VERB",
                "morphofeat": "Tense=Past|VerbForm=Part",
                "span": [{"id": "w12"}],
            },
            {
                "id": "t13",
                "type": "open",
                "lemma": "Spacy",
                "pos": "PROPN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w13"}],
            },
            {
                "id": "t14",
                "type": "open",
                "lemma": "and",
                "pos": "CCONJ",
                "span": [{"id": "w14"}],
            },
            {
                "id": "t15",
                "type": "open",
                "lemma": "stanza",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w15"}],
            },
            {
                "id": "t16",
                "type": "open",
                "lemma": "pipeline",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w16"}],
            },
            {
                "id": "t17",
                "type": "open",
                "lemma": "with",
                "pos": "ADP",
                "span": [{"id": "w17"}],
            },
            {
                "id": "t18",
                "type": "open",
                "lemma": "(",
                "pos": "PUNCT",
                "span": [{"id": "w18"}],
            },
            {
                "id": "t19",
                "type": "open",
                "lemma": "intermediate",
                "pos": "ADJ",
                "morphofeat": "Degree=Pos",
                "span": [{"id": "w19"}],
            },
            {
                "id": "t20",
                "type": "open",
                "lemma": ")",
                "pos": "PUNCT",
                "span": [{"id": "w20"}],
            },
            {
                "id": "t21",
                "type": "open",
                "lemma": "result",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w21"}],
            },
            {
                "id": "t22",
                "type": "open",
                "lemma": "and",
                "pos": "CCONJ",
                "span": [{"id": "w22"}],
            },
            {
                "id": "t23",
                "type": "open",
                "lemma": "all",
                "pos": "DET",
                "span": [{"id": "w23"}],
            },
            {
                "id": "t24",
                "type": "open",
                "lemma": "processing",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w24"}],
            },
            {
                "id": "t25",
                "type": "open",
                "lemma": "step",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w25"}],
            },
            {
                "id": "t26",
                "type": "open",
                "lemma": "in",
                "pos": "ADP",
                "span": [{"id": "w26"}],
            },
            {
                "id": "t27",
                "type": "open",
                "lemma": "one",
                "pos": "NUM",
                "morphofeat": "NumType=Card",
                "span": [{"id": "w27"}],
            },
            {
                "id": "t28",
                "type": "open",
                "lemma": "format",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w28"}],
            },
            {
                "id": "t29",
                "type": "open",
                "lemma": ".",
                "pos": "PUNCT",
                "span": [{"id": "w29"}],
            },
            {
                "id": "t30",
                "type": "open",
                "lemma": "multiword",
                "pos": "NOUN",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w30"}],
            },
            {
                "id": "t31",
                "type": "open",
                "lemma": "like",
                "pos": "ADP",
                "span": [{"id": "w31"}],
            },
            {
                "id": "t32",
                "type": "open",
                "lemma": "in",
                "pos": "ADP",
                "span": [{"id": "w32"}],
            },
            {
                "id": "t33",
                "type": "open",
                "lemma": "''",
                "pos": "PUNCT",
                "span": [{"id": "w33"}],
            },
            {
                "id": "t34",
                "type": "open",
                "lemma": "we",
                "pos": "PRON",
                "morphofeat": "Case=Nom|Number=Plur|Person=1|PronType=Prs",
                "span": [{"id": "w34"}],
            },
            {
                "id": "t35",
                "type": "open",
                "lemma": "have",
                "pos": "AUX",
                "morphofeat": "Mood=Ind|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w35"}],
            },
            {
                "id": "t36",
                "type": "open",
                "lemma": "set",
                "pos": "VERB",
                "morphofeat": "Tense=Past|VerbForm=Part",
                "component_of": "mw1",
                "span": [{"id": "w36"}],
            },
            {
                "id": "t37",
                "type": "open",
                "lemma": "that",
                "pos": "PRON",
                "morphofeat": "Number=Sing|PronType=Dem",
                "span": [{"id": "w37"}],
            },
            {
                "id": "t38",
                "type": "open",
                "lemma": "out",
                "pos": "ADP",
                "component_of": "mw1",
                "span": [{"id": "w38"}],
            },
            {
                "id": "t39",
                "type": "open",
                "lemma": "below",
                "pos": "ADV",
                "span": [{"id": "w39"}],
            },
            {
                "id": "t40",
                "type": "open",
                "lemma": "''",
                "pos": "PUNCT",
                "span": [{"id": "w40"}],
            },
            {
                "id": "t41",
                "type": "open",
                "lemma": "be",
                "pos": "AUX",
                "morphofeat": "Mood=Ind|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w41"}],
            },
            {
                "id": "t42",
                "type": "open",
                "lemma": "recognize",
                "pos": "VERB",
                "morphofeat": "Tense=Past|VerbForm=Part|Voice=Pass",
                "span": [{"id": "w42"}],
            },
            {
                "id": "t43",
                "type": "open",
                "lemma": "(",
                "pos": "PUNCT",
                "span": [{"id": "w43"}],
            },
            {
                "id": "t44",
                "type": "open",
                "lemma": "depend",
                "pos": "VERB",
                "morphofeat": "VerbForm=Ger",
                "span": [{"id": "w44"}],
            },
            {
                "id": "t45",
                "type": "open",
                "lemma": "on",
                "pos": "ADP",
                "span": [{"id": "w45"}],
            },
            {
                "id": "t46",
                "type": "open",
                "lemma": "you",
                "pos": "PRON",
                "morphofeat": "Person=2|Poss=Yes|PronType=Prs",
                "span": [{"id": "w46"}],
            },
            {
                "id": "t47",
                "type": "open",
                "lemma": "nlp",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w47"}],
            },
            {
                "id": "t48",
                "type": "open",
                "lemma": "processor",
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w48"}],
            },
            {
                "id": "t49",
                "type": "open",
                "lemma": ")",
                "pos": "PUNCT",
                "span": [{"id": "w49"}],
            },
            {
                "id": "t50",
                "type": "open",
                "lemma": ".",
                "pos": "PUNCT",
                "span": [{"id": "w50"}],
            },
        ]

        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_9_docx_dependencies(self):
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.deps

        expected = [
            {"from_term": "t3", "to_term": "t1", "rfunc": "det"},
            {"from_term": "t4", "to_term": "t3", "rfunc": "nsubj"},
            {"from_term": "t3", "to_term": "t2", "rfunc": "compound"},
            {"from_term": "t4", "to_term": "t5", "rfunc": "obj"},
            {"from_term": "t7", "to_term": "t6", "rfunc": "mark"},
            {"from_term": "t4", "to_term": "t7", "rfunc": "xcomp"},
            {"from_term": "t9", "to_term": "t8", "rfunc": "compound"},
            {"from_term": "t7", "to_term": "t9", "rfunc": "obj"},
            {"from_term": "t16", "to_term": "t10", "rfunc": "case"},
            {"from_term": "t7", "to_term": "t16", "rfunc": "obl"},
            {"from_term": "t16", "to_term": "t11", "rfunc": "amod"},
            {"from_term": "t16", "to_term": "t12", "rfunc": "amod"},
            {"from_term": "t16", "to_term": "t13", "rfunc": "compound"},
            {"from_term": "t15", "to_term": "t14", "rfunc": "cc"},
            {"from_term": "t13", "to_term": "t15", "rfunc": "conj"},
            {"from_term": "t21", "to_term": "t17", "rfunc": "case"},
            {"from_term": "t7", "to_term": "t21", "rfunc": "obl"},
            {"from_term": "t19", "to_term": "t18", "rfunc": "punct"},
            {"from_term": "t21", "to_term": "t19", "rfunc": "amod"},
            {"from_term": "t19", "to_term": "t20", "rfunc": "punct"},
            {"from_term": "t25", "to_term": "t22", "rfunc": "cc"},
            {"from_term": "t21", "to_term": "t25", "rfunc": "conj"},
            {"from_term": "t25", "to_term": "t23", "rfunc": "det"},
            {"from_term": "t25", "to_term": "t24", "rfunc": "compound"},
            {"from_term": "t28", "to_term": "t26", "rfunc": "case"},
            {"from_term": "t25", "to_term": "t28", "rfunc": "nmod"},
            {"from_term": "t28", "to_term": "t27", "rfunc": "nummod"},
            {"from_term": "t4", "to_term": "t29", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t30", "rfunc": "nsubj:pass"},
            {"from_term": "t36", "to_term": "t31", "rfunc": "mark"},
            {"from_term": "t42", "to_term": "t36", "rfunc": "advcl"},
            {"from_term": "t36", "to_term": "t32", "rfunc": "mark"},
            {"from_term": "t36", "to_term": "t33", "rfunc": "punct"},
            {"from_term": "t36", "to_term": "t34", "rfunc": "nsubj"},
            {"from_term": "t36", "to_term": "t35", "rfunc": "aux"},
            {"from_term": "t36", "to_term": "t37", "rfunc": "obj"},
            {"from_term": "t36", "to_term": "t38", "rfunc": "compound:prt"},
            {"from_term": "t36", "to_term": "t39", "rfunc": "advmod"},
            {"from_term": "t36", "to_term": "t40", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t41", "rfunc": "aux:pass"},
            {"from_term": "t48", "to_term": "t43", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t48", "rfunc": "obl"},
            {"from_term": "t48", "to_term": "t44", "rfunc": "case"},
            {"from_term": "t44", "to_term": "t45", "rfunc": "fixed"},
            {"from_term": "t48", "to_term": "t46", "rfunc": "nmod:poss"},
            {"from_term": "t48", "to_term": "t47", "rfunc": "compound"},
            {"from_term": "t48", "to_term": "t49", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t50", "rfunc": "punct"},
        ]

        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_10_docx_multiwords(self):
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.multiwords
        expected = [
            {
                "id": "mw1",
                "lemma": "set_out",
                "pos": "VERB",
                "type": "phrasal",
                "components": [
                    {"id": "mw1.c1", "span": [{"id": "t36"}]},
                    {"id": "mw1.c2", "span": [{"id": "t38"}]},
                ],
            }
        ]
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )

    def test_11_docx_raw(self):
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.raw
        expected = "The Nafigator package allows you to store NLP output from custom made Spacy and stanza pipelines with (intermediate) results and all processing steps in one format.  Multiwords like in “we have set that out below” are recognized (depending on your NLP processor)."
        assert actual == expected, (
            "expected: " + str(expected) + ", actual: " + str(actual)
        )
