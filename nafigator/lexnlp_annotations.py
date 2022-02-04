# -*- coding: utf-8 -*-

"""Lexnlp_annotations module.

This module contains functions to add lexnlp annotations to NafDocuments

"""

# import io
# import re
# import os
# from lxml import etree
# import pandas as pd
# import logging
from nafigator import parse2naf, NafDocument, EntityElement

# import datetime
# from typing import Union

try:
    import lexnlp

    LEXNLP = True
except:
    LEXNLP = False

if LEXNLP:
    import lexnlp.extract.en.acts
    import lexnlp.extract.en.amounts
    import lexnlp.extract.en.citations
    import lexnlp.extract.en.conditions
    import lexnlp.extract.en.constraints
    import lexnlp.extract.en.copyright
    import lexnlp.extract.en.courts
    import lexnlp.extract.en.cusip
    import lexnlp.extract.en.dates
    import lexnlp.extract.en.definitions
    import lexnlp.extract.en.distances
    import lexnlp.extract.en.durations
    import lexnlp.extract.en.geoentities
    import lexnlp.extract.en.money
    import lexnlp.extract.en.percents
    import lexnlp.extract.en.pii
    import lexnlp.extract.en.ratios
    import lexnlp.extract.en.regulations
    import lexnlp.extract.en.trademarks
    import lexnlp.extract.en.urls


def add_lexnlp(doc: NafDocument, annotations=list):
    if doc.language == "en":
        for annotation in annotations:
            if annotation == "acts":
                add_annotations(doc, lexnlp.extract.en.acts.get_acts_annotations)
            if annotation == "amount":
                add_annotations(doc, lexnlp.extract.en.amounts.get_amount_annotations)
            if annotation == "condition":
                add_annotations(
                    doc, lexnlp.extract.en.citations.get_citation_annotations
                )
            if annotation == "citation":
                add_annotations(
                    doc, lexnlp.extract.en.conditions.get_condition_annotations
                )
            if annotation == "constraint":
                add_annotations(
                    doc, lexnlp.extract.en.constraints.get_constraint_annotations
                )
            if annotation == "copyright":
                add_annotations(
                    doc, lexnlp.extract.en.copyright.get_copyright_annotations
                )
            if annotation == "court":
                add_annotations(doc, lexnlp.extract.en.courts.get_court_annotations)
            if annotation == "cusip":
                add_annotations(doc, lexnlp.extract.en.cusip.get_cusip_annotations)
            if annotation == "date":
                add_annotations(doc, lexnlp.extract.en.dates.get_date_annotations)
            if annotation == "definition":
                add_annotations(
                    doc, lexnlp.extract.en.definitions.get_definition_annotations
                )
            if annotation == "distance":
                add_annotations(
                    doc, lexnlp.extract.en.distances.get_distance_annotations
                )
            if annotation == "duration":
                add_annotations(
                    doc, lexnlp.extract.en.durations.get_duration_annotations
                )
            if annotation == "geoentities":
                add_annotations(
                    doc, lexnlp.extract.en.geoentities.get_geoentities_annotations
                )
            if annotation == "money":
                add_annotations(doc, lexnlp.extract.en.money.get_money_annotations)
            if annotation == "percents":
                add_annotations(
                    doc, lexnlp.extract.en.percents.get_percents_annotations
                )
            if annotation == "pii":
                add_annotations(doc, lexnlp.extract.en.pii.get_pii_annotations)
            if annotation == "ratios":
                add_annotations(doc, lexnlp.extract.en.ratios.get_ratio_annotations)
            if annotation == "regulations":
                add_annotations(
                    doc, lexnlp.extract.en.regulations.get_regulation_annotations
                )
            if annotation == "trademarks":
                add_annotations(
                    doc, lexnlp.extract.en.trademarks.get_trademark_annotations
                )
            if annotation == "urls":
                add_annotations(doc, lexnlp.extract.en.urls.get_url_annotations)


def add_annotations(doc: NafDocument, annotator):
    entity_number = len(doc.entities) + 1
    words = {word["id"]: word for word in doc.text}
    for amount in annotator(doc.raw):
        d = amount.to_dictionary()
        start, end = amount.coords
        # derive span
        # for span: check all words if in start-end of annotation
        span = []
        for word in doc.text:
            if int(word["offset"]) >= start - 1:
                if int(word["offset"]) <= end:
                    span.append(word["id"])
                else:
                    break
        entity_data = EntityElement(
            id="e" + str(entity_number),
            type=d["tags"]["Extracted Entity Type"],
            status=None,
            source=None,
            span=span,
            ext_refs=list(),
            comment=" ".join([words[s]["text"] for s in span]),
        )
        doc.add_entity_element(entity_data, naf_version="v3.1", comments="")
        entity_number += 1
