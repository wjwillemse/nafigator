# coding: utf-8

"""Const module."""

from collections import namedtuple

ProcessorElement = namedtuple(
    "lp", "name version timestamp beginTimestamp endTimestamp hostname"
)

WordformElement = namedtuple("WfElement", "page sent id length wordform offset")

TermElement = namedtuple("TermElement", "id lemma pos type morphofeat targets text")

Entity = namedtuple("Entity", "start end type")

EntityElement = namedtuple("EntityElement", "id type targets text ext_refs")

DependencyRelation = namedtuple(
    "DependencyRelation", "from_term to_term from_orth to_orth rfunc"
)

ChunkElement = namedtuple("ChunkElement", "cid head phrase text targets")

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
