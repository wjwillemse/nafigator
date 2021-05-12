# coding: utf-8

"""Const module."""

from collections import namedtuple

ProcessorElement = namedtuple(
    "lp", "name version timestamp beginTimestamp endTimestamp hostname"
)

WordformElement = namedtuple("WfElement", "id sent para page offset length xpath text")

TermElement = namedtuple("TermElement", "id type lemma pos morphofeat netype case head component_of compound_type span ext_refs comment")

Entity = namedtuple("Entity", "start end type")

EntityElement = namedtuple("EntityElement", "id type status source span ext_refs comment")

DependencyRelation = namedtuple(
    "DependencyRelation", "from_term to_term rfunc case comment"
)
          
ChunkElement = namedtuple("ChunkElement", "id head phrase case span comment")

RawElement = namedtuple("RawElement", "text")

MultiwordElement = namedtuple("MultiwordElement", "id lemma pos morphofeat case status type components")

ComponentElement = namedtuple("ComponentElement", "id type lemma pos morphofeat netype case head span")

hidden_characters = ["\a", "\b", "\t", "\n", "\v", "\f", "\r"]

hidden_table = {ord(hidden_character): " " for hidden_character in hidden_characters}

udpos2nafpos_info = {
    "ADJ": {"class": "open", "naf_pos": "G"},
    "ADP": {"class": "open", "naf_pos": "P"},
    "ADV": {"class": "open", "naf_pos": "A"},
    "AUX": {
        "class": "close",
        "naf_pos": "V",
    },
    "CCONJ": {"class": "close", "naf_pos": "C"},
    "DET": {"class": "close", "naf_pos": "D"},
    "INTJ": {"class": "open", "naf_pos": "O"},
    "NOUN": {"class": "open", "naf_pos": "N"},
    "NUM": {"class": "close", "naf_pos": "O"},
    "PART": {"class": "close", "naf_pos": "O"},
    "PRON": {"class": "close", "naf_pos": "O"},
    "PROPN": {"class": "open", "naf_pos": "R"},
    "PUNCT": {"class": "close", "naf_pos": "O"},
    "SCONJ": {"class": "close", "naf_pos": "O"},
    "SYM": {"class": "open", "naf_pos": "O"},
    "VERB": {"class": "open", "naf_pos": "V"},
    "X": {"class": "open", "naf_pos": "O"},
    "SPACE": {"class": "open", "naf_pos": "O"},
}
