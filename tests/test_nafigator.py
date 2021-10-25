#!/usr/bin/env python

"""Tests for `nafigator` package."""


import unittest

unittest.TestLoader.sortTestMethodsUsing = None
from deepdiff import DeepDiff

from click.testing import CliRunner
from nafigator import NafDocument, parse2naf
from os.path import join


class TestNafigator_pdf(unittest.TestCase):
    """Tests for `nafigator` package."""

    def test_1_pdf_generate_naf(self):
        """ """
        tree = parse2naf.generate_naf(
            input=join("tests", "tests", "example.pdf"),
            engine="stanza",
            language="en",
            naf_version="v3.1",
            dtd_validation=False,
            params={},
            nlp=None,
        )
        assert tree.write(join("tests", "tests", "example.naf.xml")) == None

    def test_1_split_pre_linguistic(self):
        """ """
        # only save the preprocess steps
        tree = parse2naf.generate_naf(
            input=join("tests", "tests", "example.pdf"),
            engine="stanza",
            language="en",
            naf_version="v3.1",
            dtd_validation=False,
            params={'linguistic_layers': []},
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
                        params = {'preprocess_layers': []}
                        )

        doc = NafDocument().open(join("tests", "tests", "example.naf.xml"))

        assert tree.raw == doc.raw

    def test_2_pdf_header_filedesc(self):
        """ """
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.header["fileDesc"]
        expected = {
            "filename": "tests\\tests\\example.pdf",
            "filetype": "application/pdf",
        }
        assert actual["filename"] == expected["filename"]
        assert actual["filetype"] == expected["filetype"]

    def test_3_pdf_header_public(self):
        """ """
        naf = NafDocument().open(join("tests", "tests", "example.naf.xml"))
        actual = naf.header["public"]
        expected = {
            "{http://purl.org/dc/elements/1.1/}uri": "tests\\tests\\example.pdf",
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
            {"id": "e2", "type": "CARDINAL", "text": "one", "span": [{"id": "t28"}]},
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
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w1",
                "length": "3",
                "offset": "0",
            },
            {
                "text": "Nafigator",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w2",
                "length": "9",
                "offset": "4",
            },
            {
                "text": "package",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w3",
                "length": "7",
                "offset": "14",
            },
            {
                "text": "allows",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w4",
                "length": "6",
                "offset": "22",
            },
            {
                "text": "you",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w5",
                "length": "3",
                "offset": "29",
            },
            {
                "text": "to",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w6",
                "length": "2",
                "offset": "33",
            },
            {
                "text": "store",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w7",
                "length": "5",
                "offset": "36",
            },
            {
                "text": "NLP",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w8",
                "length": "3",
                "offset": "42",
            },
            {
                "text": "output",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w9",
                "length": "6",
                "offset": "46",
            },
            {
                "text": "from",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w10",
                "length": "4",
                "offset": "53",
            },
            {
                "text": "custom",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w11",
                "length": "6",
                "offset": "58",
            },
            {
                "text": "made",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w12",
                "length": "4",
                "offset": "65",
            },
            {
                "text": "spa",
                "page": "1",
                "para": "1",
                "sent": "1",
                "id": "w13",
                "length": "3",
                "offset": "70",
            },
            {
                "text": "Cy",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w14",
                "length": "2",
                "offset": "73",
            },
            {
                "text": "and",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w15",
                "length": "3",
                "offset": "76",
            },
            {
                "text": "stanza",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w16",
                "length": "6",
                "offset": "80",
            },
            {
                "text": "pipelines",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w17",
                "length": "9",
                "offset": "88",
            },
            {
                "text": "with",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w18",
                "length": "4",
                "offset": "98",
            },
            {
                "text": "(",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w19",
                "length": "1",
                "offset": "103",
            },
            {
                "text": "intermediate",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w20",
                "length": "12",
                "offset": "104",
            },
            {
                "text": ")",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w21",
                "length": "1",
                "offset": "116",
            },
            {
                "text": "results",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w22",
                "length": "7",
                "offset": "118",
            },
            {
                "text": "and",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w23",
                "length": "3",
                "offset": "126",
            },
            {
                "text": "all",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w24",
                "length": "3",
                "offset": "130",
            },
            {
                "text": "processing",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w25",
                "length": "10",
                "offset": "134",
            },
            {
                "text": "steps",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w26",
                "length": "5",
                "offset": "145",
            },
            {
                "text": "in",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w27",
                "length": "2",
                "offset": "151",
            },
            {
                "text": "one",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w28",
                "length": "3",
                "offset": "154",
            },
            {
                "text": "format",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w29",
                "length": "6",
                "offset": "158",
            },
            {
                "text": ".",
                "page": "1",
                "para": "1",
                "sent": "2",
                "id": "w30",
                "length": "1",
                "offset": "164",
            },
            {
                "text": "Multiwords",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w31",
                "length": "10",
                "offset": "167",
            },
            {
                "text": "like",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w32",
                "length": "4",
                "offset": "178",
            },
            {
                "text": "in",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w33",
                "length": "2",
                "offset": "183",
            },
            {
                "text": "“",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w34",
                "length": "1",
                "offset": "186",
            },
            {
                "text": "we",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w35",
                "length": "2",
                "offset": "187",
            },
            {
                "text": "have",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w36",
                "length": "4",
                "offset": "190",
            },
            {
                "text": "set",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w37",
                "length": "3",
                "offset": "195",
            },
            {
                "text": "that",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w38",
                "length": "4",
                "offset": "199",
            },
            {
                "text": "out",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w39",
                "length": "3",
                "offset": "204",
            },
            {
                "text": "below",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w40",
                "length": "5",
                "offset": "208",
            },
            {
                "text": "”",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w41",
                "length": "1",
                "offset": "213",
            },
            {
                "text": "are",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w42",
                "length": "3",
                "offset": "215",
            },
            {
                "text": "recognized",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w43",
                "length": "10",
                "offset": "219",
            },
            {
                "text": "(",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w44",
                "length": "1",
                "offset": "230",
            },
            {
                "text": "depending",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w45",
                "length": "9",
                "offset": "231",
            },
            {
                "text": "on",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w46",
                "length": "2",
                "offset": "241",
            },
            {
                "text": "your",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w47",
                "length": "4",
                "offset": "244",
            },
            {
                "text": "NLP",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w48",
                "length": "3",
                "offset": "249",
            },
            {
                "text": "processor",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w49",
                "length": "9",
                "offset": "254",
            },
            {
                "text": ")",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w50",
                "length": "1",
                "offset": "263",
            },
            {
                "text": ".",
                "page": "1",
                "para": "2",
                "sent": "3",
                "id": "w51",
                "length": "1",
                "offset": "264",
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
                "lemma": "the",
                "pos": "DET",
                "type": "open",
                "morphofeat": "Definite=Def|PronType=Art",
                "span": [{"id": "w1"}],
            },
            {
                "id": "t2",
                "lemma": "Nafigator",
                "pos": "PROPN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w2"}],
            },
            {
                "id": "t3",
                "lemma": "package",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w3"}],
            },
            {
                "id": "t4",
                "lemma": "allow",
                "pos": "VERB",
                "type": "open",
                "morphofeat": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w4"}],
            },
            {
                "id": "t5",
                "lemma": "you",
                "pos": "PRON",
                "type": "open",
                "morphofeat": "Case=Acc|Person=2|PronType=Prs",
                "span": [{"id": "w5"}],
            },
            {
                "id": "t6",
                "lemma": "to",
                "pos": "PART",
                "type": "open",
                "span": [{"id": "w6"}],
            },
            {
                "id": "t7",
                "lemma": "store",
                "pos": "VERB",
                "type": "open",
                "morphofeat": "VerbForm=Inf",
                "span": [{"id": "w7"}],
            },
            {
                "id": "t8",
                "lemma": "nlp",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w8"}],
            },
            {
                "id": "t9",
                "lemma": "output",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w9"}],
            },
            {
                "id": "t10",
                "lemma": "from",
                "pos": "ADP",
                "type": "open",
                "span": [{"id": "w10"}],
            },
            {
                "id": "t11",
                "lemma": "custom",
                "pos": "ADJ",
                "type": "open",
                "morphofeat": "Degree=Pos",
                "span": [{"id": "w11"}],
            },
            {
                "id": "t12",
                "lemma": "make",
                "pos": "VERB",
                "type": "open",
                "morphofeat": "Tense=Past|VerbForm=Part",
                "span": [{"id": "w12"}],
            },
            {
                "id": "t13",
                "lemma": "spa",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w13"}],
            },
            {
                "id": "t14",
                "lemma": "cy",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w14"}],
            },
            {
                "id": "t15",
                "lemma": "and",
                "pos": "CCONJ",
                "type": "open",
                "span": [{"id": "w15"}],
            },
            {
                "id": "t16",
                "lemma": "stanza",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w16"}],
            },
            {
                "id": "t17",
                "lemma": "pipeline",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w17"}],
            },
            {
                "id": "t18",
                "lemma": "with",
                "pos": "ADP",
                "type": "open",
                "span": [{"id": "w18"}],
            },
            {
                "id": "t19",
                "lemma": "(",
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w19"}],
            },
            {
                "id": "t20",
                "lemma": "intermediate",
                "pos": "ADJ",
                "type": "open",
                "morphofeat": "Degree=Pos",
                "span": [{"id": "w20"}],
            },
            {
                "id": "t21",
                "lemma": ")",
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w21"}],
            },
            {
                "id": "t22",
                "lemma": "result",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w22"}],
            },
            {
                "id": "t23",
                "lemma": "and",
                "pos": "CCONJ",
                "type": "open",
                "span": [{"id": "w23"}],
            },
            {
                "id": "t24",
                "lemma": "all",
                "pos": "DET",
                "type": "open",
                "span": [{"id": "w24"}],
            },
            {
                "id": "t25",
                "lemma": "processing",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w25"}],
            },
            {
                "id": "t26",
                "lemma": "step",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w26"}],
            },
            {
                "id": "t27",
                "lemma": "in",
                "pos": "ADP",
                "type": "open",
                "span": [{"id": "w27"}],
            },
            {
                "id": "t28",
                "lemma": "one",
                "pos": "NUM",
                "type": "open",
                "morphofeat": "NumType=Card",
                "span": [{"id": "w28"}],
            },
            {
                "id": "t29",
                "lemma": "format",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w29"}],
            },
            {
                "id": "t30",
                "lemma": ".",
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w30"}],
            },
            {
                "id": "t31",
                "lemma": "multiword",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Plur",
                "span": [{"id": "w31"}],
            },
            {
                "id": "t32",
                "lemma": "like",
                "pos": "ADP",
                "type": "open",
                "span": [{"id": "w32"}],
            },
            {
                "id": "t33",
                "lemma": "in",
                "pos": "ADP",
                "type": "open",
                "span": [{"id": "w33"}],
            },
            {
                "id": "t34",
                "lemma": '"',
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w34"}],
            },
            {
                "id": "t35",
                "lemma": "we",
                "pos": "PRON",
                "type": "open",
                "morphofeat": "Case=Nom|Number=Plur|Person=1|PronType=Prs",
                "span": [{"id": "w35"}],
            },
            {
                "id": "t36",
                "lemma": "have",
                "pos": "AUX",
                "type": "open",
                "morphofeat": "Mood=Ind|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w36"}],
            },
            {
                "id": "t37",
                "lemma": "set",
                "pos": "VERB",
                "type": "open",
                "morphofeat": "Tense=Past|VerbForm=Part",
                "component_of": "mw1",
                "span": [{"id": "w37"}],
            },
            {
                "id": "t38",
                "lemma": "that",
                "pos": "SCONJ",
                "type": "open",
                "span": [{"id": "w38"}],
            },
            {
                "id": "t39",
                "lemma": "out",
                "pos": "ADP",
                "type": "open",
                "component_of": "mw1",
                "span": [{"id": "w39"}],
            },
            {
                "id": "t40",
                "lemma": "below",
                "pos": "ADV",
                "type": "open",
                "span": [{"id": "w40"}],
            },
            {
                "id": "t41",
                "lemma": '"',
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w41"}],
            },
            {
                "id": "t42",
                "lemma": "be",
                "pos": "AUX",
                "type": "open",
                "morphofeat": "Mood=Ind|Tense=Pres|VerbForm=Fin",
                "span": [{"id": "w42"}],
            },
            {
                "id": "t43",
                "lemma": "recognize",
                "pos": "VERB",
                "type": "open",
                "morphofeat": "Tense=Past|VerbForm=Part|Voice=Pass",
                "span": [{"id": "w43"}],
            },
            {
                "id": "t44",
                "lemma": "(",
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w44"}],
            },
            {
                "id": "t45",
                "lemma": "depend",
                "pos": "VERB",
                "type": "open",
                "morphofeat": "VerbForm=Ger",
                "span": [{"id": "w45"}],
            },
            {
                "id": "t46",
                "lemma": "on",
                "pos": "ADP",
                "type": "open",
                "span": [{"id": "w46"}],
            },
            {
                "id": "t47",
                "lemma": "you",
                "pos": "PRON",
                "type": "open",
                "morphofeat": "Person=2|Poss=Yes|PronType=Prs",
                "span": [{"id": "w47"}],
            },
            {
                "id": "t48",
                "lemma": "nlp",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w48"}],
            },
            {
                "id": "t49",
                "lemma": "processor",
                "pos": "NOUN",
                "type": "open",
                "morphofeat": "Number=Sing",
                "span": [{"id": "w49"}],
            },
            {
                "id": "t50",
                "lemma": ")",
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w50"}],
            },
            {
                "id": "t51",
                "lemma": ".",
                "pos": "PUNCT",
                "type": "open",
                "span": [{"id": "w51"}],
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
            {"from_term": "t13", "to_term": "t10", "rfunc": "case"},
            {"from_term": "t7", "to_term": "t13", "rfunc": "obl"},
            {"from_term": "t12", "to_term": "t11", "rfunc": "compound"},
            {"from_term": "t13", "to_term": "t12", "rfunc": "amod"},
            {"from_term": "t17", "to_term": "t14", "rfunc": "compound"},
            {"from_term": "t16", "to_term": "t15", "rfunc": "cc"},
            {"from_term": "t14", "to_term": "t16", "rfunc": "conj"},
            {"from_term": "t22", "to_term": "t18", "rfunc": "case"},
            {"from_term": "t17", "to_term": "t22", "rfunc": "nmod"},
            {"from_term": "t22", "to_term": "t19", "rfunc": "punct"},
            {"from_term": "t22", "to_term": "t20", "rfunc": "amod"},
            {"from_term": "t22", "to_term": "t21", "rfunc": "punct"},
            {"from_term": "t26", "to_term": "t23", "rfunc": "cc"},
            {"from_term": "t22", "to_term": "t26", "rfunc": "conj"},
            {"from_term": "t26", "to_term": "t24", "rfunc": "det"},
            {"from_term": "t26", "to_term": "t25", "rfunc": "compound"},
            {"from_term": "t29", "to_term": "t27", "rfunc": "case"},
            {"from_term": "t26", "to_term": "t29", "rfunc": "nmod"},
            {"from_term": "t29", "to_term": "t28", "rfunc": "nummod"},
            {"from_term": "t17", "to_term": "t30", "rfunc": "punct"},
            {"from_term": "t37", "to_term": "t32", "rfunc": "mark"},
            {"from_term": "t31", "to_term": "t37", "rfunc": "acl"},
            {"from_term": "t37", "to_term": "t33", "rfunc": "mark"},
            {"from_term": "t37", "to_term": "t34", "rfunc": "punct"},
            {"from_term": "t37", "to_term": "t35", "rfunc": "nsubj"},
            {"from_term": "t37", "to_term": "t36", "rfunc": "aux"},
            {"from_term": "t43", "to_term": "t38", "rfunc": "mark"},
            {"from_term": "t37", "to_term": "t43", "rfunc": "ccomp"},
            {"from_term": "t37", "to_term": "t39", "rfunc": "compound:prt"},
            {"from_term": "t37", "to_term": "t40", "rfunc": "advmod"},
            {"from_term": "t37", "to_term": "t41", "rfunc": "punct"},
            {"from_term": "t43", "to_term": "t42", "rfunc": "aux:pass"},
            {"from_term": "t49", "to_term": "t44", "rfunc": "punct"},
            {"from_term": "t43", "to_term": "t49", "rfunc": "obl"},
            {"from_term": "t49", "to_term": "t45", "rfunc": "case"},
            {"from_term": "t49", "to_term": "t46", "rfunc": "case"},
            {"from_term": "t49", "to_term": "t47", "rfunc": "nmod:poss"},
            {"from_term": "t49", "to_term": "t48", "rfunc": "compound"},
            {"from_term": "t49", "to_term": "t50", "rfunc": "punct"},
            {"from_term": "t43", "to_term": "t51", "rfunc": "punct"},
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
                    {"id": "mw1.c1", "span": [{"id": "t37"}]},
                    {"id": "mw1.c2", "span": [{"id": "t39"}]},
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
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.header["fileDesc"]
        expected = {
            "filename": "tests\\tests\\example.docx",
            "filetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        assert actual["filename"] == expected["filename"]
        assert actual["filetype"] == expected["filetype"]

    def test_3_docx_header_public(self):
        """ """
        naf = NafDocument().open(join("tests", "tests", "example.docx.naf.xml"))
        actual = naf.header["public"]
        expected = {
            "{http://purl.org/dc/elements/1.1/}uri": "tests\\tests\\example.docx",
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
                "pos": "NOUN",
                "morphofeat": "Number=Sing",
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
                "lemma": "spacy",
                "pos": "NOUN",
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
                "lemma": '"',
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
                "pos": "SCONJ",
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
                "lemma": '"',
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
            {"from_term": "t13", "to_term": "t10", "rfunc": "case"},
            {"from_term": "t9", "to_term": "t13", "rfunc": "nmod"},
            {"from_term": "t12", "to_term": "t11", "rfunc": "compound"},
            {"from_term": "t13", "to_term": "t12", "rfunc": "amod"},
            {"from_term": "t16", "to_term": "t14", "rfunc": "cc"},
            {"from_term": "t13", "to_term": "t16", "rfunc": "conj"},
            {"from_term": "t16", "to_term": "t15", "rfunc": "compound"},
            {"from_term": "t21", "to_term": "t17", "rfunc": "case"},
            {"from_term": "t7", "to_term": "t21", "rfunc": "obl"},
            {"from_term": "t21", "to_term": "t18", "rfunc": "punct"},
            {"from_term": "t21", "to_term": "t19", "rfunc": "amod"},
            {"from_term": "t21", "to_term": "t20", "rfunc": "punct"},
            {"from_term": "t25", "to_term": "t22", "rfunc": "cc"},
            {"from_term": "t13", "to_term": "t25", "rfunc": "conj"},
            {"from_term": "t25", "to_term": "t23", "rfunc": "det"},
            {"from_term": "t25", "to_term": "t24", "rfunc": "compound"},
            {"from_term": "t28", "to_term": "t26", "rfunc": "case"},
            {"from_term": "t25", "to_term": "t28", "rfunc": "nmod"},
            {"from_term": "t28", "to_term": "t27", "rfunc": "nummod"},
            {"from_term": "t4", "to_term": "t29", "rfunc": "punct"},
            {"from_term": "t36", "to_term": "t31", "rfunc": "mark"},
            {"from_term": "t30", "to_term": "t36", "rfunc": "acl"},
            {"from_term": "t36", "to_term": "t32", "rfunc": "mark"},
            {"from_term": "t36", "to_term": "t33", "rfunc": "punct"},
            {"from_term": "t36", "to_term": "t34", "rfunc": "nsubj"},
            {"from_term": "t36", "to_term": "t35", "rfunc": "aux"},
            {"from_term": "t42", "to_term": "t37", "rfunc": "mark"},
            {"from_term": "t36", "to_term": "t42", "rfunc": "ccomp"},
            {"from_term": "t36", "to_term": "t38", "rfunc": "compound:prt"},
            {"from_term": "t36", "to_term": "t39", "rfunc": "advmod"},
            {"from_term": "t36", "to_term": "t40", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t41", "rfunc": "aux:pass"},
            {"from_term": "t48", "to_term": "t43", "rfunc": "punct"},
            {"from_term": "t42", "to_term": "t48", "rfunc": "obl"},
            {"from_term": "t48", "to_term": "t44", "rfunc": "case"},
            {"from_term": "t48", "to_term": "t45", "rfunc": "case"},
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
