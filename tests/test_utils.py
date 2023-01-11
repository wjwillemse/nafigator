import math
from parameterized import parameterized
import unittest
from nafigator.utils import *


unittest.TestLoader.sortTestMethodsUsing = None


class TestUtils(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    def setUp(self):
        self.doc_sentences = [
            {
                "text": "Natural language processing ( NLP ) is a subfield of linguistics .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w1"},
                    {"id": "w2"},
                    {"id": "w3"},
                    {"id": "w4"},
                    {"id": "w5"},
                    {"id": "w6"},
                    {"id": "w7"},
                    {"id": "w8"},
                    {"id": "w9"},
                    {"id": "w10"},
                    {"id": "w11"},
                    {"id": "w12"},
                ],
                "terms": [
                    {"id": "t1"},
                    {"id": "t2"},
                    {"id": "t3"},
                    {"id": "t4"},
                    {"id": "t5"},
                    {"id": "t6"},
                    {"id": "t7"},
                    {"id": "t8"},
                    {"id": "t9"},
                    {"id": "t10"},
                    {"id": "t11"},
                    {"id": "t12"},
                ],
                "sent": ["1"],
            },
            {
                "text": "It is also a subfield of computer science and artificial intelligence .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w13"},
                    {"id": "w14"},
                    {"id": "w15"},
                    {"id": "w16"},
                    {"id": "w17"},
                    {"id": "w18"},
                    {"id": "w19"},
                    {"id": "w20"},
                    {"id": "w21"},
                    {"id": "w22"},
                    {"id": "w23"},
                    {"id": "w24"},
                ],
                "terms": [
                    {"id": "t13"},
                    {"id": "t14"},
                    {"id": "t15"},
                    {"id": "t16"},
                    {"id": "t17"},
                    {"id": "t18"},
                    {"id": "t19"},
                    {"id": "t20"},
                    {"id": "t21"},
                    {"id": "t22"},
                    {"id": "t23"},
                    {"id": "t24"},
                ],
                "sent": ["2"],
            },
            {
                "text": "It concerns the interactions between computers and human language .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w25"},
                    {"id": "w26"},
                    {"id": "w27"},
                    {"id": "w28"},
                    {"id": "w29"},
                    {"id": "w30"},
                    {"id": "w31"},
                    {"id": "w32"},
                    {"id": "w33"},
                    {"id": "w34"},
                ],
                "terms": [
                    {"id": "t25"},
                    {"id": "t26"},
                    {"id": "t27"},
                    {"id": "t28"},
                    {"id": "t29"},
                    {"id": "t30"},
                    {"id": "t31"},
                    {"id": "t32"},
                    {"id": "t33"},
                    {"id": "t34"},
                ],
                "sent": ["3"],
            },
            {
                "text": ("It is about how to program computers to process and analyze large amounts of natural "
                         "language data ."),
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w35"},
                    {"id": "w36"},
                    {"id": "w37"},
                    {"id": "w38"},
                    {"id": "w39"},
                    {"id": "w40"},
                    {"id": "w41"},
                    {"id": "w42"},
                    {"id": "w43"},
                    {"id": "w44"},
                    {"id": "w45"},
                    {"id": "w46"},
                    {"id": "w47"},
                    {"id": "w48"},
                    {"id": "w49"},
                    {"id": "w50"},
                    {"id": "w51"},
                    {"id": "w52"},
                ],
                "terms": [
                    {"id": "t35"},
                    {"id": "t36"},
                    {"id": "t37"},
                    {"id": "t38"},
                    {"id": "t39"},
                    {"id": "t40"},
                    {"id": "t41"},
                    {"id": "t42"},
                    {"id": "t43"},
                    {"id": "t44"},
                    {"id": "t45"},
                    {"id": "t46"},
                    {"id": "t47"},
                    {"id": "t48"},
                    {"id": "t49"},
                    {"id": "t50"},
                    {"id": "t51"},
                    {"id": "t52"},
                ],
                "sent": ["4"],
            },
            {
                "text": 'The goal is a computer capable of " understanding " the contents of documents .',
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w53"},
                    {"id": "w54"},
                    {"id": "w55"},
                    {"id": "w56"},
                    {"id": "w57"},
                    {"id": "w58"},
                    {"id": "w59"},
                    {"id": "w60"},
                    {"id": "w61"},
                    {"id": "w62"},
                    {"id": "w63"},
                    {"id": "w64"},
                    {"id": "w65"},
                    {"id": "w66"},
                    {"id": "w67"},
                ],
                "terms": [
                    {"id": "t53"},
                    {"id": "t54"},
                    {"id": "t55"},
                    {"id": "t56"},
                    {"id": "t57"},
                    {"id": "t58"},
                    {"id": "t59"},
                    {"id": "t60"},
                    {"id": "t61"},
                    {"id": "t62"},
                    {"id": "t63"},
                    {"id": "t64"},
                    {"id": "t65"},
                    {"id": "t66"},
                    {"id": "t67"},
                ],
                "sent": ["5"],
            },
            {
                "text": "This include the contextual nuances of the language within them .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w68"},
                    {"id": "w69"},
                    {"id": "w70"},
                    {"id": "w71"},
                    {"id": "w72"},
                    {"id": "w73"},
                    {"id": "w74"},
                    {"id": "w75"},
                    {"id": "w76"},
                    {"id": "w77"},
                    {"id": "w78"},
                ],
                "terms": [
                    {"id": "t68"},
                    {"id": "t69"},
                    {"id": "t70"},
                    {"id": "t71"},
                    {"id": "t72"},
                    {"id": "t73"},
                    {"id": "t74"},
                    {"id": "t75"},
                    {"id": "t76"},
                    {"id": "t77"},
                    {"id": "t78"},
                ],
                "sent": ["6"],
            },
            {
                "text": "The technology can then accurately extract information .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w79"},
                    {"id": "w80"},
                    {"id": "w81"},
                    {"id": "w82"},
                    {"id": "w83"},
                    {"id": "w84"},
                    {"id": "w85"},
                    {"id": "w86"},
                ],
                "terms": [
                    {"id": "t79"},
                    {"id": "t80"},
                    {"id": "t81"},
                    {"id": "t82"},
                    {"id": "t83"},
                    {"id": "t84"},
                    {"id": "t85"},
                    {"id": "t86"},
                ],
                "sent": ["7"],
            },
            {
                "text": "This applies also for insights contained in the documents .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w87"},
                    {"id": "w88"},
                    {"id": "w89"},
                    {"id": "w90"},
                    {"id": "w91"},
                    {"id": "w92"},
                    {"id": "w93"},
                    {"id": "w94"},
                    {"id": "w95"},
                    {"id": "w96"},
                ],
                "terms": [
                    {"id": "t87"},
                    {"id": "t88"},
                    {"id": "t89"},
                    {"id": "t90"},
                    {"id": "t91"},
                    {"id": "t92"},
                    {"id": "t93"},
                    {"id": "t94"},
                    {"id": "t95"},
                    {"id": "t96"},
                ],
                "sent": ["8"],
            },
            {
                "text": "It can also work well for categorising and organising the documents themselves .",
                "para": ["1"],
                "page": ["1"],
                "span": [
                    {"id": "w97"},
                    {"id": "w98"},
                    {"id": "w99"},
                    {"id": "w100"},
                    {"id": "w101"},
                    {"id": "w102"},
                    {"id": "w103"},
                    {"id": "w104"},
                    {"id": "w105"},
                    {"id": "w106"},
                    {"id": "w107"},
                    {"id": "w108"},
                    {"id": "w109"},
                ],
                "terms": [
                    {"id": "t97"},
                    {"id": "t98"},
                    {"id": "t99"},
                    {"id": "t100"},
                    {"id": "t101"},
                    {"id": "t102"},
                    {"id": "t103"},
                    {"id": "t104"},
                    {"id": "t105"},
                    {"id": "t106"},
                    {"id": "t107"},
                    {"id": "t108"},
                    {"id": "t109"},
                ],
                "sent": ["9"],
            },
        ]
        self.doc_words = {
            "w1": {
                "text": "Natural",
                "id": "w1",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "0",
                "length": "7",
            },
            "w2": {
                "text": "language",
                "id": "w2",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "8",
                "length": "8",
            },
            "w3": {
                "text": "processing",
                "id": "w3",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "17",
                "length": "10",
            },
            "w4": {
                "text": "(",
                "id": "w4",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "28",
                "length": "1",
            },
            "w5": {
                "text": "NLP",
                "id": "w5",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "29",
                "length": "3",
            },
            "w6": {
                "text": ")",
                "id": "w6",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "32",
                "length": "1",
            },
            "w7": {
                "text": "is",
                "id": "w7",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "34",
                "length": "2",
            },
            "w8": {
                "text": "a",
                "id": "w8",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "37",
                "length": "1",
            },
            "w9": {
                "text": "subfield",
                "id": "w9",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "39",
                "length": "8",
            },
            "w10": {
                "text": "of",
                "id": "w10",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "48",
                "length": "2",
            },
            "w11": {
                "text": "linguistics",
                "id": "w11",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "51",
                "length": "11",
            },
            "w12": {
                "text": ".",
                "id": "w12",
                "sent": "1",
                "para": "1",
                "page": "1",
                "offset": "62",
                "length": "1",
            },
            "w13": {
                "text": "It",
                "id": "w13",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "64",
                "length": "2",
            },
            "w14": {
                "text": "is",
                "id": "w14",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "67",
                "length": "2",
            },
            "w15": {
                "text": "also",
                "id": "w15",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "70",
                "length": "4",
            },
            "w16": {
                "text": "a",
                "id": "w16",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "75",
                "length": "1",
            },
            "w17": {
                "text": "subfield",
                "id": "w17",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "77",
                "length": "8",
            },
            "w18": {
                "text": "of",
                "id": "w18",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "86",
                "length": "2",
            },
            "w19": {
                "text": "computer",
                "id": "w19",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "90",
                "length": "8",
            },
            "w20": {
                "text": "science",
                "id": "w20",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "99",
                "length": "7",
            },
            "w21": {
                "text": "and",
                "id": "w21",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "107",
                "length": "3",
            },
            "w22": {
                "text": "artificial",
                "id": "w22",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "111",
                "length": "10",
            },
            "w23": {
                "text": "intelligence",
                "id": "w23",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "122",
                "length": "12",
            },
            "w24": {
                "text": ".",
                "id": "w24",
                "sent": "2",
                "para": "1",
                "page": "1",
                "offset": "134",
                "length": "1",
            },
            "w25": {
                "text": "It",
                "id": "w25",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "136",
                "length": "2",
            },
            "w26": {
                "text": "concerns",
                "id": "w26",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "139",
                "length": "8",
            },
            "w27": {
                "text": "the",
                "id": "w27",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "148",
                "length": "3",
            },
            "w28": {
                "text": "interactions",
                "id": "w28",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "152",
                "length": "12",
            },
            "w29": {
                "text": "between",
                "id": "w29",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "165",
                "length": "7",
            },
            "w30": {
                "text": "computers",
                "id": "w30",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "173",
                "length": "9",
            },
            "w31": {
                "text": "and",
                "id": "w31",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "184",
                "length": "3",
            },
            "w32": {
                "text": "human",
                "id": "w32",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "188",
                "length": "5",
            },
            "w33": {
                "text": "language",
                "id": "w33",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "194",
                "length": "8",
            },
            "w34": {
                "text": ".",
                "id": "w34",
                "sent": "3",
                "para": "1",
                "page": "1",
                "offset": "202",
                "length": "1",
            },
            "w35": {
                "text": "It",
                "id": "w35",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "204",
                "length": "2",
            },
            "w36": {
                "text": "is",
                "id": "w36",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "207",
                "length": "2",
            },
            "w37": {
                "text": "about",
                "id": "w37",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "210",
                "length": "5",
            },
            "w38": {
                "text": "how",
                "id": "w38",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "216",
                "length": "3",
            },
            "w39": {
                "text": "to",
                "id": "w39",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "220",
                "length": "2",
            },
            "w40": {
                "text": "program",
                "id": "w40",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "223",
                "length": "7",
            },
            "w41": {
                "text": "computers",
                "id": "w41",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "231",
                "length": "9",
            },
            "w42": {
                "text": "to",
                "id": "w42",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "241",
                "length": "2",
            },
            "w43": {
                "text": "process",
                "id": "w43",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "244",
                "length": "7",
            },
            "w44": {
                "text": "and",
                "id": "w44",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "252",
                "length": "3",
            },
            "w45": {
                "text": "analyze",
                "id": "w45",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "256",
                "length": "7",
            },
            "w46": {
                "text": "large",
                "id": "w46",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "264",
                "length": "5",
            },
            "w47": {
                "text": "amounts",
                "id": "w47",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "271",
                "length": "7",
            },
            "w48": {
                "text": "of",
                "id": "w48",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "279",
                "length": "2",
            },
            "w49": {
                "text": "natural",
                "id": "w49",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "282",
                "length": "7",
            },
            "w50": {
                "text": "language",
                "id": "w50",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "290",
                "length": "8",
            },
            "w51": {
                "text": "data",
                "id": "w51",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "299",
                "length": "4",
            },
            "w52": {
                "text": ".",
                "id": "w52",
                "sent": "4",
                "para": "1",
                "page": "1",
                "offset": "303",
                "length": "1",
            },
            "w53": {
                "text": "The",
                "id": "w53",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "305",
                "length": "3",
            },
            "w54": {
                "text": "goal",
                "id": "w54",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "309",
                "length": "4",
            },
            "w55": {
                "text": "is",
                "id": "w55",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "314",
                "length": "2",
            },
            "w56": {
                "text": "a",
                "id": "w56",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "317",
                "length": "1",
            },
            "w57": {
                "text": "computer",
                "id": "w57",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "319",
                "length": "8",
            },
            "w58": {
                "text": "capable",
                "id": "w58",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "328",
                "length": "7",
            },
            "w59": {
                "text": "of",
                "id": "w59",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "336",
                "length": "2",
            },
            "w60": {
                "text": '"',
                "id": "w60",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "339",
                "length": "1",
            },
            "w61": {
                "text": "understanding",
                "id": "w61",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "340",
                "length": "13",
            },
            "w62": {
                "text": '"',
                "id": "w62",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "353",
                "length": "1",
            },
            "w63": {
                "text": "the",
                "id": "w63",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "355",
                "length": "3",
            },
            "w64": {
                "text": "contents",
                "id": "w64",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "360",
                "length": "8",
            },
            "w65": {
                "text": "of",
                "id": "w65",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "369",
                "length": "2",
            },
            "w66": {
                "text": "documents",
                "id": "w66",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "372",
                "length": "9",
            },
            "w67": {
                "text": ".",
                "id": "w67",
                "sent": "5",
                "para": "1",
                "page": "1",
                "offset": "381",
                "length": "1",
            },
            "w68": {
                "text": "This",
                "id": "w68",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "383",
                "length": "4",
            },
            "w69": {
                "text": "include",
                "id": "w69",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "388",
                "length": "7",
            },
            "w70": {
                "text": "the",
                "id": "w70",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "396",
                "length": "3",
            },
            "w71": {
                "text": "contextual",
                "id": "w71",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "400",
                "length": "10",
            },
            "w72": {
                "text": "nuances",
                "id": "w72",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "411",
                "length": "7",
            },
            "w73": {
                "text": "of",
                "id": "w73",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "419",
                "length": "2",
            },
            "w74": {
                "text": "the",
                "id": "w74",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "422",
                "length": "3",
            },
            "w75": {
                "text": "language",
                "id": "w75",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "426",
                "length": "8",
            },
            "w76": {
                "text": "within",
                "id": "w76",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "435",
                "length": "6",
            },
            "w77": {
                "text": "them",
                "id": "w77",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "442",
                "length": "4",
            },
            "w78": {
                "text": ".",
                "id": "w78",
                "sent": "6",
                "para": "1",
                "page": "1",
                "offset": "446",
                "length": "1",
            },
            "w79": {
                "text": "The",
                "id": "w79",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "448",
                "length": "3",
            },
            "w80": {
                "text": "technology",
                "id": "w80",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "453",
                "length": "10",
            },
            "w81": {
                "text": "can",
                "id": "w81",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "464",
                "length": "3",
            },
            "w82": {
                "text": "then",
                "id": "w82",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "468",
                "length": "4",
            },
            "w83": {
                "text": "accurately",
                "id": "w83",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "473",
                "length": "10",
            },
            "w84": {
                "text": "extract",
                "id": "w84",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "484",
                "length": "7",
            },
            "w85": {
                "text": "information",
                "id": "w85",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "492",
                "length": "11",
            },
            "w86": {
                "text": ".",
                "id": "w86",
                "sent": "7",
                "para": "1",
                "page": "1",
                "offset": "503",
                "length": "1",
            },
            "w87": {
                "text": "This",
                "id": "w87",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "505",
                "length": "4",
            },
            "w88": {
                "text": "applies",
                "id": "w88",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "510",
                "length": "7",
            },
            "w89": {
                "text": "also",
                "id": "w89",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "518",
                "length": "4",
            },
            "w90": {
                "text": "for",
                "id": "w90",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "523",
                "length": "3",
            },
            "w91": {
                "text": "insights",
                "id": "w91",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "527",
                "length": "8",
            },
            "w92": {
                "text": "contained",
                "id": "w92",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "536",
                "length": "9",
            },
            "w93": {
                "text": "in",
                "id": "w93",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "546",
                "length": "2",
            },
            "w94": {
                "text": "the",
                "id": "w94",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "550",
                "length": "3",
            },
            "w95": {
                "text": "documents",
                "id": "w95",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "554",
                "length": "9",
            },
            "w96": {
                "text": ".",
                "id": "w96",
                "sent": "8",
                "para": "1",
                "page": "1",
                "offset": "563",
                "length": "1",
            },
            "w97": {
                "text": "It",
                "id": "w97",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "565",
                "length": "2",
            },
            "w98": {
                "text": "can",
                "id": "w98",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "568",
                "length": "3",
            },
            "w99": {
                "text": "also",
                "id": "w99",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "572",
                "length": "4",
            },
            "w100": {
                "text": "work",
                "id": "w100",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "577",
                "length": "4",
            },
            "w101": {
                "text": "well",
                "id": "w101",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "582",
                "length": "4",
            },
            "w102": {
                "text": "for",
                "id": "w102",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "587",
                "length": "3",
            },
            "w103": {
                "text": "categorising",
                "id": "w103",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "591",
                "length": "12",
            },
            "w104": {
                "text": "and",
                "id": "w104",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "604",
                "length": "3",
            },
            "w105": {
                "text": "organising",
                "id": "w105",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "608",
                "length": "10",
            },
            "w106": {
                "text": "the",
                "id": "w106",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "619",
                "length": "3",
            },
            "w107": {
                "text": "documents",
                "id": "w107",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "623",
                "length": "9",
            },
            "w108": {
                "text": "themselves",
                "id": "w108",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "634",
                "length": "10",
            },
            "w109": {
                "text": ".",
                "id": "w109",
                "sent": "9",
                "para": "1",
                "page": "1",
                "offset": "644",
                "length": "1",
            },
        }

        self.doc_formats = [
            {
                "length": "652",
                "offset": "0",
                "textboxes": [
                    {
                        "textlines": [
                            {
                                "texts": [
                                    {
                                        "font": "Arial-BoldMT",
                                        "size": "10.560",
                                        "length": "27",
                                        "offset": "0",
                                        "text": "Natural language processing",
                                    },
                                    {
                                        "font": "ArialMT",
                                        "size": "10.560",
                                        "length": "2",
                                        "offset": "27",
                                        "text": " (",
                                    },
                                    {
                                        "font": "Arial-BoldMT",
                                        "size": "10.560",
                                        "length": "3",
                                        "offset": "29",
                                        "text": "NLP",
                                    },
                                    {
                                        "font": "ArialMT",
                                        "size": "10.560",
                                        "length": "2",
                                        "offset": "32",
                                        "text": ") ",
                                    },
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "55",
                                        "offset": "34",
                                        "text": "is a subfield of linguistics. It is also a subfield of ",
                                    },
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "93",
                                        "offset": "90",
                                        "text": ("computer science and artificial intelligence. It concerns "
                                                 "the interactions between computers "),
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "86",
                                        "offset": "184",
                                        "text": ("and human language. It is about how to program computers to "
                                                 "process and analyze large "),
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "88",
                                        "offset": "271",
                                        "text": ('amounts of natural language data. The goal is a computer capable '
                                                 'of "understanding" the '),
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "92",
                                        "offset": "360",
                                        "text": ("contents of documents. This include the contextual nuances of "
                                                 "the language within them. The "),
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "96",
                                        "offset": "453",
                                        "text": ("technology can then accurately extract information. This applies "
                                                 "also for insights contained in "),
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "83",
                                        "offset": "550",
                                        "text": ("the documents. It can also work well for categorising and "
                                                 "organising the documents "),
                                    }
                                ]
                            },
                            {
                                "texts": [
                                    {
                                        "font": "TimesNewRomanPSMT",
                                        "size": "12.000",
                                        "length": "12",
                                        "offset": "634",
                                        "text": "themselves. ",
                                    }
                                ]
                            },
                        ]
                    }
                ],
                "figures": [],
                "headers": [],
                "tables": [],
            }
        ]

    @parameterized.expand(
        [(
            "sentence in fist textline",
            0,
            1,
            ("Natural language processing (NLP) is a subfield of linguistics. It is also a subfield of "
             "\ncomputer science and artificial intelligence. It concerns the interactions between computers ")
        ),
            (
            "sentence in one textline",
            5,
            2,
            ("and human language. It is about how to program computers to process and analyze large \namounts of "
             "natural language data. The goal is a computer capable of \"understanding\" the \ncontents of documents. "
             "This include the contextual nuances of the language within them. The \ntechnology can then accurately "
             "extract information. This applies also for insights contained in \nthe documents. It can also work well "
             "for categorising and organising the documents ")
        ),
            (
            "sentence split over two lines",
            4,
            1,
            ("and human language. It is about how to program computers to process and analyze large \namounts "
             "of natural language data. The goal is a computer capable of \"understanding\" the \ncontents of "
             "documents. This include the contextual nuances of the language within them. The ")
        ),
            (
            "sentence in last textlines",
            -1,
            2,
            ("contents of documents. This include the contextual nuances of the language within them. The \ntechnology "
             "can then accurately extract information. This applies also for insights contained in \nthe documents. It "
             "can also work well for categorising and organising the documents \nthemselves. ")
        )
        ])
    def test_get_textlines(self, name, idx_sentence, context_range, expected_text):
        actual_text = get_textlines(self.doc_sentences[idx_sentence], self.doc_words, self.doc_formats, context_range)

        self.assertEqual(actual_text, expected_text)

    def test_dataframe2naf(self):
        """
        This function evaluates metadata and reruns files with naf error.
        Input:
            df_meta: the dataframe containing the meta data for the NAF files.
            overwrite_existing_naf: if True then existing NAF files are overwritten (default = False)
            rerun_files_with_naf_errors: if True then documents that produced NAF errors are run again (default = False)
            engine: name of the NLP processor to be used (default = None)
            naf_version: NAF version to be used
            dtd_validation: perform validation of each NAF file (default = False)
            params: additional parameters for NAF conversion
        Level: 0
        Scenarios:
            missing dc:language
            missing dc:source
            rerun_files_with_naf_errors True
            overwrite_existing_naf True
        """
        pass

    def test_load_dtd(self):
        """
        This function loads dtd
        Input:
            dtd_url: the location of the dtd file
        Level: 0
        Scenarios:
            check if dtd has been loaded
        """
        pass

    def test_time_in_correct_format(self):
        """
        This function returns the current time (UTC) as a string
        Input:
            datetime_obj: the input to be converted
        Level: 0
        Scenarios:
            check if conversion is correctly done
        """
        pass

    def test_normalize_token_orth(self):
        """
        This function normalizes the token text
        Input:
            orth: the token text to be normalized
        Level: 1
        Scenarios:
            orth with \n
            orth wihout \n
        """
        pass

    def test_prepare_comment_text(self):
        """
        This function prepares comment text for xml
        Input:
            text: comment to be converted to xml comment
        Level: 0
        Scenarios:
            text with --
            text ending with -
            text without -- or -
        """
        pass

    def test_remove_illegal_chars(self):
        """
        This function removes illegal characters in text
        Input:
            text: string from which illegal characters need to be removed
        Level: 0
        Scenarios:
            text is None
            text contains an illegal character
        """
        pass

    def test_remove_control_characters(self):
        """
        This function strips invalid XML characters that `lxml` cannot parse.
        Input:
            html: text from which control characters need to be removed
        Level: 1
        Scenarios:
            text with a non-ascii character, such as an emoji
        """
        pass

    def test_strip_illegal_xml_characters(self):
        """
        This function compares the "invalid XML character range" numerically
        (needs to be unembedded - out of scope)
        Input:
            s
            def test_ult
            base
        Level: 0
        Scenarios:
            n containing an invalid XML character range
            n not containing an invalid XML character range
        """
        pass

    def test_sublist_indices(self):
        """
        This function returns a list of indices of the full list that contain the sub list
        Input:
            sub: list of words to search in the full list
            full: list of words in which the words of sublist are searched
        Level: 0
        Scenarios:
            sub list with 2 different words
            sub list with 1 word being found twice
            sub list in which words of sublist do not occur
        """
        pass

    def test_remove_sublists(self):
        """
        OUTDATED - CHECK TO REMOVE
        This function returns a list where all sublists are removed
        Input:
            lst: list with lists
        Level: 0
        Scenarios:
            see examples in function
        """
        pass

    def test_evaluate_sentence(self):
        """
        OUTDATED - CHECK TO REMOVE
        This function evaluates a sentence on occurrence of mandatory terms and non occurrence of
        term to avoid
        Input:
        Level: 
        Scenarios: 
        """
        pass

    def test_lemmatize(self):
        """
        OUTDATED - CHECK TO REMOVE
        This function lemmatizes text in onject
        Input:
            o: the object with text to be lemmatized
            language: language used for lemmatization
            nlp: dictionary of nlp processors
        Level: 0
        Scenarios:
            string
            list
            dict
            series
            dataframe
        """
        pass

    def test_lowercase(self):
        """
        OUTDATED - CHECK TO REMOVE
        This function
        Input:
        Level:
        Scenarios:
        """
        pass

    def test_lemmatize_sentence(self):
        """
        OUTDATED - CHECK TO REMOVE
        This function lemmatizes a naf sentence
        Input:
            sentence: dict of sentence (naf)
            terms: list of terms dict (naf)
        Level: 0
        Scenarios:
            sentence to be lemmatized
        """
        pass

    def test_glue_terms_separated_by_soft_hyphens(self):
        """
        NOT BEING USED IN NAFIGATOR - CHECK USAGE OTHER PACKAGES
        This function glues terms that are separated by soft hyphens
        Input:
            doc: the NafDocument
            language: language used for lemmatization
            nlp: dictionary of nlp processors
        Level: 0
        Scenarios:
            NafDocument with soft hyphens
        """
        pass

    def test_glue_terms_separated_by_hard_hyphens(self):
        """
        NOT BEING USED IN NAFIGATOR - CHECK USAGE OTHER PACKAGES
        This function glues terms that are separated by hard hyphens
        Input:
            doc: the NafDocument
            language: language used for lemmatization
            nlp: dictionary of nlp processors
        Level: 0
        Scenarios:
            NafDocument with hard hyphens
        """
        pass

    def test_glue_sentences_separated_by_colons(self):
        """
        NOT BEING USED IN NAFIGATOR - CHECK USAGE OTHER PACKAGES
        This function glues sentences that are separated by colons
        Input:
            doc: the NafDocument
            language: language used for lemmatization
            nlp: dictionary of nlp processors    
        Level: 0
        Scenarios:
            NafDocument with colons
        """
        pass

    def test_get_context_rows(self):
        """
        This function retrieves the line where word has been found with option to also retreive sentences/paragraphs
            before and after
        Input:
            ref_text: a sentence or paragraph from the sentences or paragraphs layer as a dictionary to retrieve extra
                context for
            naf: a NafDocument.sentences or NafDocument.paragaphs (can be rewritten with search_level as extra input)
            context_range: amount of context lines around ref_text
        Level: 0
        Scenarios:
            context range = 0
            context range = 2
            sentence
            paragraph

        """
        pass

    def test_get_textlines(self):
        """
        test already written above. Move below to follow seem order as in utils.py
        This function
        Input:
        Level:
        Scenarios:
        """
        pass
