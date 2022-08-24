# -*- coding: utf-8 -*-

"""
term extraction module.

This module contains term extraction functions for nafigator package

"""

import io
import re
import os
from lxml import etree
import pandas as pd
import logging
from nafigator import parse2naf
from .const import TermElement
from .utils import sublist_indices
import docx
from docx.enum.dml import MSO_THEME_COLOR_INDEX
import datetime
from typing import Union


def get_terms(pattern, doc):
    """
    Get terms from a NafDocument

    Args:
        pattern: list of pos, for example ["ADJ", "NOUN", "NOUN"]
        doc: nafDocument

    Returns:
        list of term satisfying the pattern

    """
    doc_terms = {term["id"]: term for term in doc.terms}
    doc_words = {word["id"]: word for word in doc.text}

    for term in doc_terms.keys():
        doc_terms[term]["text"] = " ".join(
            [doc_words[s["id"]]["text"] for s in doc_terms[term]["span"]]
        )

    doc_pos = [term["pos"] for term in doc.terms]
    doc_text = [term for term in doc_terms.values()]

    patterns = sublist_indices(pattern, doc_pos)

    result = [[doc_text[p]["text"].lower() for p in pattern] for pattern in patterns]

    return result


ILLEGAL_TERM_CHARACTERS = ["„", "”", ">", "<", ",", "α", "β", "σ", "ð", "þ", "%", "δ"]


def extract_terms(doc=None, patterns: list() = None, termNotes: dict() = None):
    """Function to extract terms from a NafDocument and add the terms to TbxDocument

    Args:
        output:

    Returns:
        None

    """
    if patterns is None:

        if doc.language in ["fr", "es"]:
            patterns = [
                ["ADJ", "NOUN"],
                ["ADJ", "NOUN", "NOUN"],
                ["ADJ", "ADJ", "NOUN"],
                ["NOUN"],
                ["NOUN", "ADP", "NOUN"],
                ["NOUN", "ADP", "NOUN", "ADP"],
                ["NOUN", "ADP", "NOUN", "ADP", "NOUN"],
                ["NOUN", "ADP", "NOUN", "ADJ"],
                ["NOUN", "ADP", "NOUN", "ADJ", "ADP", "NOUN"],
                ["NOUN", "ADJ"],
                ["NOUN", "ADJ", "ADJ"],
                ["NOUN", "ADJ", "ADP", "NOUN", "ADP", "NOUN", "ADP", "NOUN"], # moyenne pondérée des échelons de qualité de crédit
                ["NOUN", "DET", "NOUN", "ADP", "NOUN"],
                ["NOUN", "NOUN"],
                ["NOUN", "NOUN", "NOUN"],
                ["NOUN", "NOUN", "ADJ"],
                ["NOUN", "PUNCT", "NOUN"],
        ]
        else: #if doc.language in ["en", "de", "nl", "da", "sv"]:
            patterns = [
                ["NOUN"],
                ["ADJ", "NOUN"],
                ["NOUN", "NOUN"],
                ["NOUN", "PUNCT", "NOUN"],
                # ["NOUN", "DET", "NOUN"],
                ["NOUN", "ADJ", "NOUN"],
                ["NOUN", "ADJ", "DET", "NOUN"],
                ["NOUN", "ADP", "ADJ", "NOUN"],
                ["NOUN", "NOUN", "NOUN"],
                ["ADJ", "NOUN", "NOUN"],
                ["ADJ", "ADJ", "NOUN"],
                ["ADJ", "DET", "NOUN", "ADJ", "NOUN"], # für die Gruppenaufsicht zuständige Behörde
        ]

    if doc is not None:
        d = {}
        for pattern in patterns:
            terms = get_terms(pattern, doc)
            for term in terms:
                if (
                    not any(
                        [
                            ((s in component) or (s == component))
                            for component in term
                            for s in ILLEGAL_TERM_CHARACTERS
                        ]
                    )
                    and "\xad" != term[-1][-1]
                    and "-" != term[-1][-1]
                    and "-" != term[0][0]
                    and not any([len(component) == 1 and not component=="-" for component in term])
                ):
                    concept_text = " ".join(term)
                    concept_text = concept_text.replace(" \xad ", "")
                    concept_text = concept_text.replace("\xad ", "")
                    concept_text = concept_text.replace(" \xad", "")
                    concept_text = concept_text.replace("\xad", "")
                    # check is the length of the term corresponds to the length of the pattern
                    # (sometimes the nlp engine produces wordforms with two words)
                    if len(concept_text.split(" ")) == len(pattern): 
                        concept_text = concept_text.replace(" - ", "-")
                        if concept_text in d.keys():
                            d[concept_text]["frequency"][0] += 1
                        else:
                            d[concept_text] = {"dc:uri": [doc.header['public']['{http://purl.org/dc/elements/1.1/}uri']],
                                               "dc:format": doc.header['public']['{http://purl.org/dc/elements/1.1/}format'],
                                               "dc:language": doc.language, 
                                               "frequency": [1], 
                                               "partOfSpeech": ", ".join(pattern).lower()}
                        d[concept_text] = {**d[concept_text], **termNotes}
    return d
