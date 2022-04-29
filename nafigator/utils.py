# -*- coding: utf-8 -*-

"""
Utils module.

This module contains utility functions for nafigator package

"""

import io
import re
import os
from lxml import etree
import pandas as pd
import logging
from nafigator import parse2naf
from .const import TermElement
import docx
from docx.enum.dml import MSO_THEME_COLOR_INDEX
import datetime
from typing import Union
import nafigator

def dataframe2naf(
    df_meta: pd.DataFrame,
    overwrite_existing_naf: bool = False,
    rerun_files_with_naf_errors: bool = False,
    engine: str = None,
    naf_version: str = None,
    dtd_validation: bool = False,
    params: dict = {},
    nlp=None,
) -> pd.DataFrame:
    """Batch processor for NAF

    Args:
        df_meta: the dataframe containing the meta data for the NAF files.
        overwrite_existing_naf: if True then existing NAF files are overwritten (default = False)
        rerun_files_with_naf_errors: if True then documents that produced NAF errors are run again (default = False)
        engine: name of the NLP processor to be used (default = None)
        naf_version: NAF version to be used
        dtd_validation: perform validation of each NAF file (default = False)
        params: additional parameters for NAF conversion

    Returns:
        pd.DataFrame: the dataframe with (updated) metadata

    """
    if "naf:status" not in df_meta.columns:
        df_meta["naf:status"] = ""

    for row in df_meta.index:

        if "dc:language" in df_meta.columns:
            dc_language = df_meta.loc[row, "dc:language"].lower()
        else:
            dc_language = None
            df_meta.loc[row, "naf:status"] = "ERROR, no dc:language in DataFrame"

        if "dc:source" in df_meta.columns:
            dc_source = df_meta.loc[row, "dc:source"]
        else:
            dc_source = None
            df_meta.loc[row, "naf:status"] = "ERROR, no dc:source in DataFrame"

        if "naf:source" in df_meta.columns and not pd.isna(
            df_meta.loc[row, "naf:source"]
        ):
            output = df_meta.loc[row, "naf:source"]
        else:
            if dc_source is not None:
                output = os.path.splitext(dc_source)[0] + ".naf.xml"

        if dc_source and dc_language and output:

            # logging per processed file
            log_file: str = os.path.splitext(dc_source)[0] + ".log"
            logging.basicConfig(filename=log_file, level=logging.WARNING, filemode="w")

            if os.path.exists(output) and not overwrite_existing_naf:
                # the NAF file exists and we should not overwrite existing naf
                # files -> skip
                df_meta.loc[row, "naf:status"] = "OK"
                df_meta.loc[row, "naf:source"] = output
                continue
            elif (
                "error" in df_meta.loc[row, "naf:status"].lower()
                and not rerun_files_with_naf_errors
            ):
                # the status is ERROR and we should not rerun files with errors
                # -> skip
                continue
            else:
                # put columns in params
                params = {
                    col: df_meta.loc[row, col]
                    for col in df_meta.columns
                    if col not in ["naf:source", "naf:status"]
                }
                try:
                    doc = parse2naf.generate_naf(
                        input=dc_source,
                        engine=engine,
                        language=dc_language,
                        naf_version=naf_version,
                        dtd_validation=dtd_validation,
                        params=params,
                        nlp=nlp,
                    )
                    if not os.path.exists(output):
                        doc.write(output)
                    else:
                        if overwrite_existing_naf:
                            doc.write(output)
                    df_meta.loc[row, "naf:status"] = "OK"
                    df_meta.loc[row, "naf:source"] = output
                except:
                    df_meta.loc[row, "naf:status"] = "ERROR, generate_naf"

    return df_meta


def load_dtd(dtd_url: str) -> etree.DTD:
    """Utility function to load the dtd

    Args:
        dtd_url: the location of the dtd file

    Returns:
        etree.DTD: the dtd object to be used for validation

    """
    dtd = None
    r = open(dtd_url)
    if r:
        dtd_file_object = io.StringIO(r.read())
        dtd = etree.DTD(dtd_file_object)
    if dtd is None:
        logging.error("failed to load dtd from" + str(dtd_url))
    else:
        logging.info("Succesfully to load dtd from" + str(dtd_url))
    return dtd


def time_in_correct_format(datetime_obj: datetime.datetime) -> str:
    """
    Function that returns the current time (UTC)

    Args:
        datetime_obj: the input to be converted

    Returns:
        str: the time in correct format

    """
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


def normalize_token_orth(orth: str) -> str:
    """
    Function that normalizes the token text

    Args:
        orth: the token text to be normalized

    Returns:
        str: the normalized token text

    """
    if "\n" in orth:
        return "NEWLINE"
    else:
        return remove_control_characters(orth)


def prepare_comment_text(text: str) -> str:
    """
    Function to prepare comment text for xml

    Args:
        text: comment to be converted to xml comment

    Returns:
        str: converted comment text

    """
    text = text.replace("--", "DOUBLEDASH")
    if text.endswith("-"):
        text = text[:-1] + "SINGLEDASH"
    return text


# def remove_illegal_chars(text):
#     return re.sub(illegal_pattern, "", text)

# Only allow legal strings in XML:
# http://stackoverflow.com/a/25920392/2899924
# illegal_pattern = re.compile(
#     "[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+"
# )
# improved version:

# A regex matching the "invalid XML character range"
ILLEGAL_XML_CHARS_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]"
)


def remove_illegal_chars(text: str) -> str:
    """
    Function to remove illegal characters in text

    Args:
        text: string from which illegal characters need to be removed

    Returns:
        str: string with removed illegal characters

    """
    if text is not None:
        return re.sub(ILLEGAL_XML_CHARS_RE, "", text)
    else:
        return None


def remove_control_characters(html: str) -> str:
    """
    Function to strip invalid XML characters that `lxml` cannot parse.

    type: (t.Text) -> t.Text

    See: https://github.com/html5lib/html5lib-python/issues/96

    The XML 1.0 spec defines the valid character range as:
    Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]

    We can instead match the invalid characters by inverting that range into:
    InvalidChar ::= #xb | #xc | #xFFFE | #xFFFF | [#x0-#x8] | [#xe-#x1F] | [#xD800-#xDFFF]

    Sources:
    https://www.w3.org/TR/REC-xml/#charsets,
    https://lsimons.wordpress.com/2011/03/17/stripping-illegal-characters-out-of-xml-in-python/

    Args:
        html: text from which control characters need to be removed

    Returns:
        str: string with removed control characters

    """

    def strip_illegal_xml_characters(s, default, base=10):
        # Compare the "invalid XML character range" numerically
        n = int(s, base)
        if (
            n in (0xB, 0xC, 0xFFFE, 0xFFFF)
            or 0x0 <= n <= 0x8
            or 0xE <= n <= 0x1F
            or 0xD800 <= n <= 0xDFFF
        ):
            return ""
        return default

    # We encode all non-ascii characters to XML char-refs, so for example "💖" becomes: "&#x1F496;"
    # Otherwise we'd remove emojis by mistake on narrow-unicode builds of
    # Python
    html = html.encode("ascii", "xmlcharrefreplace").decode("utf-8")
    html = re.sub(
        r"&#(\d+);?",
        lambda c: strip_illegal_xml_characters(c.group(1), c.group(0)),
        html,
    )
    html = re.sub(
        r"&#[xX]([0-9a-fA-F]+);?",
        lambda c: strip_illegal_xml_characters(c.group(1), c.group(0), base=16),
        html,
    )
    html = ILLEGAL_XML_CHARS_RE.sub("", html)
    return html


def sublist_indices(sub, full):
    """
    Returns a list of indices of the full list that contain the sub list
    :param sub: list
    :param full: list
    :return: list

    >>> sublist_indices(['Felix'], ['De', 'kat', 'genaamd', 'Felix', 'eet', 'geen', 'Felix'])
    [[3], [6]]
    >>> sublist_indices(
            ['Felix', 'Maximiliaan'],
            ['De', 'kat', 'genaamd', 'Felix', 'Maximiliaan', 'eet', 'geen', 'Felix']
        )
    [[3, 4]]
    """
    if sub == []:
        return []
    if full == []:
        return []
    found = []
    for idx, item in enumerate(full):
        if item == sub[0]:
            if len(sub) == 1:
                found.append([idx])
            else:
                match = True
                for i, s in enumerate(sub[1:]):
                    if len(full) > idx + i + 1:
                        if s != full[idx + i + 1]:
                            match = False
                    else:
                        match = False
                if match:
                    found.append(list(range(idx, idx + len(sub))))
    return found


def remove_sublists(lst):
    """
    Returns a list where all sublists are removed
    :param lst: list
    :return: list

    >>> remove_sublists([[1, 2, 3], [1, 2]])
    [[1, 2, 3]]
    >>> remove_sublists([[1, 2, 3], [1]])
    [[1, 2, 3]]
    >>> remove_sublists([[1, 2, 3], [1, 2], [1]])
    [[1, 2, 3]]
    >>> remove_sublists([[1, 2, 3], [2, 3, 4], [2, 3], [3, 4]])
    [[1, 2, 3], [2, 3, 4]]
    """
    curr_res = []
    result = []
    for elem in sorted(map(set, lst), key=len, reverse=True):
        if not any(elem <= req for req in curr_res):
            curr_res.append(elem)
            r = list(elem)
            result.append(r)
    return result


def evaluate_sentence(sentence: str, mandatory_terms: list, avoid_terms: list):
    """
    Evaluate sentence on occurrence of mandatory terms and non occurrence of
    term to avoid

    Args:
        sentence: sentence to be assessed
        mandatory_terms: list of terms that must be in sentence
        avoid_terms: list of terms that must not be in sentence

    Returns:
        True is mandatory terms are in sentence and avoid terms are not

    """
    # if all mandatory words are in the sentence and none of the avoid_terms
    # then signal
    if (
        all([sublist_indices(t.split(" "), sentence) != [] for t in mandatory_terms])
        is True
    ):
        if not any(
            [sublist_indices(t.split(" "), sentence) != [] for t in avoid_terms]
        ):
            return True
    return False


def lemmatize(
    o: Union[str, list, dict, pd.Series, pd.DataFrame],
    language: Union[str, pd.Series],
    nlp: dict,
) -> Union[str, list, dict, pd.Series, pd.DataFrame]:
    """
    lemmatize text in object
    Args:
        o: the object with text to be lemmatized
        language: language used for lemmatization
        nlp: dictionary of nlp processors
    Returns:
        object with lemmatized text
    """
    if isinstance(o, str):
        return " ".join([word.lemma for word in nlp[language](o).sentences[0].words])
    elif isinstance(o, list):
        return [lemmatize(item, language, nlp) for item in o]
    elif isinstance(o, dict):
        return {
            lemmatize(key, language, nlp): lemmatize(o[key], language, nlp) for key in o
        }
    elif isinstance(o, pd.Series):
        for this_language in set(language):
            o_list = [item for item in o[language == this_language]]
            o[language == this_language] = pd.Series(
                lemmatize(o_list, this_language, nlp),
                index=o[language == this_language].index,
            )
        return o
    elif isinstance(o, pd.DataFrame):
        return pd.DataFrame(
            {col: lemmatize(o[col], language, nlp) for col in o.columns}, index=o.index
        )
    elif pd.isna(o):
        return ""


def lowercase(
    o: Union[str, list, dict, pd.DataFrame, pd.Series]
) -> Union[str, list, dict, pd.DataFrame, pd.Series]:
    """
    Lowercase text in object
    Args:
        o: the object with text to be lowercased
    Returns:
        object with lowercased text
    """
    if isinstance(o, list):
        return [lowercase(item) for item in o]
    elif isinstance(o, dict):
        return {key.lower(): lowercase(o[key]) for key in o}
    elif isinstance(o, str):
        return o.lower()
    elif isinstance(o, pd.Series):
        return pd.Series([lowercase(item) for item in o], index=o.index)
    elif isinstance(o, pd.DataFrame):
        return pd.DataFrame(
            {col: lowercase(o[col]) for col in o.columns}, index=o.index
        )


def lemmatize_sentence(sentence: dict, terms: dict):
    """
    Lemmatize naf sentence

    Args:
        sentence: dict of sentence (naf)
        terms: list of terms dict (naf)

    Returns:
        lemmatized sentences as string

    """
    return [terms[term["id"]]["lemma"] for term in sentence["terms"]]


def glue_terms_separated_by_soft_hyphens(doc, language: str, nlp: dict):
    """
    Glue terms that are separated by soft hyphens

    Args:
        doc: the NafDocument
        language: language used for lemmatization
        nlp: dictionary of nlp processors
    Returns:
        NafDocument where terms are glued
    """

    SOFT_HYPHEN = "\xad"

    doc_words = {word["id"]: word for word in doc.text}
    terms = doc.terms
    terms_to_skip = []
    new_terms = []
    for idx, term in enumerate(terms):

        term_text = "".join([doc_words[s["id"]]["text"] for s in term["span"]])
        term_lemma = term["lemma"]
        term_pos = term["pos"]
        term_morphofeat = term.get("morphofeat", None)
        term_span = term["span"]

        if SOFT_HYPHEN in term_text:

            if term_text == SOFT_HYPHEN:
                # term equals a soft hyphen
                # so we glue terms[idx-1], terms[idx] and terms[idx+1]
                term_span = (
                    terms[idx - 1]["span"] + term["span"] + terms[idx + 1]["span"]
                )
                terms_to_skip.append(terms[idx - 1]["id"])
                terms_to_skip.append(terms[idx + 1]["id"])
            elif term_text[-1] == SOFT_HYPHEN:
                # term ends with a soft hyphen
                # so we glue terms[idx] and terms[idx+1]
                term_span = term["span"] + terms[idx + 1]["span"]
                terms_to_skip.append(terms[idx + 1]["id"])

            # the new term text is derived from the new span where soft hyphens are deleted
            term_text = "".join(
                [doc_words[s["id"]]["text"] for s in term_span]
            ).replace(SOFT_HYPHEN, "")

            # we need to determine again the linguistical properties of the resulting term
            data = nlp["nl"](term_text).sentences[0].words[0]
            term_lemma = data.lemma
            term_pos = data.pos
            term_morphofeat = data.feats

        term_data = TermElement(
            id=term["id"],
            type="open",
            lemma=term_lemma,
            pos=term_pos,
            morphofeat=term_morphofeat,
            netype=None,
            case=None,
            head=None,
            component_of=None,
            compound_type=None,
            span=[s["id"] for s in term_span],
            ext_refs=list(),
            comment=[term_text],
        )
        new_terms.append(term_data)

    # reset the terms layer with the new terms
    doc.remove_layer_elements("terms")
    for term_data in new_terms:
        if term_data.id not in terms_to_skip:
            doc.add_term_element(
                term_data, layer_to_attributes_to_ignore={"terms": {}}, comments=True
            )

    return doc

def glue_terms_separated_by_hard_hyphens(doc, language: str, nlp: dict):
    """
    Glue terms that are separated by hard hyphens

    Args:
        doc: the NafDocument
        language: language used for lemmatization
        nlp: dictionary of nlp processors
    Returns:
        NafDocument where terms are glued
    """

    formats = doc.find("formats")
    hyphen_offsets = [
        int(text.get("offset")) + len(text.text.strip()) - 1
        for page in formats
        for textbox in page
        for textline in textbox
        for text in textline
        if text.text.strip()[-1] == "-"
    ]

    HARD_HYPHEN = "-"

    doc_words = {word["id"]: word for word in doc.text}
    terms = doc.terms
    terms_to_skip = []
    new_terms = []
    for idx, term in enumerate(terms):

        term_text = "".join([doc_words[s["id"]]["text"] for s in term["span"]])
        term_lemma = term["lemma"]
        term_pos = term["pos"]
        term_morphofeat = term.get("morphofeat", None)
        term_span = term["span"]

        if term_text[-1] == HARD_HYPHEN and not term_text == HARD_HYPHEN:
            # term ends with a hard hyphen
            word = doc_words[term_span[-1]["id"]]
            word_hyphen_offset = int(word["offset"]) + len(word["text"].strip()) - 1

            next_term_text = "".join(
                [doc_words[s["id"]]["text"] for s in terms[idx + 1]["span"]]
            )
            if word_hyphen_offset in hyphen_offsets and next_term_text not in [
                "en",
                "of",
                ",",
                "en/of",
            ]:

                if next_term_text[-1] != HARD_HYPHEN:
                    term_span = term["span"] + terms[idx + 1]["span"]
                    terms_to_skip.append(terms[idx + 1]["id"])
                else:
                    term_span = (
                        term["span"] + terms[idx + 1]["span"] + terms[idx + 2]["span"]
                    )
                    terms_to_skip.append(terms[idx + 1]["id"])
                    terms_to_skip.append(terms[idx + 2]["id"])

                # the new term text is derived from the new span where soft hyphens are deleted
                term_text = "".join([doc_words[s["id"]]["text"] for s in term_span])

                # we need to determine again the linguistical properties of the resulting term
                data = nlp["nl"](term_text).sentences[0].words[0]
                term_lemma = data.lemma
                term_pos = data.pos
                term_morphofeat = data.feats

        term_data = TermElement(
            id=term["id"],
            type="open",
            lemma=term_lemma,
            pos=term_pos,
            morphofeat=term_morphofeat,
            netype=None,
            case=None,
            head=None,
            component_of=None,
            compound_type=None,
            span=[s["id"] for s in term_span],
            ext_refs=list(),
            comment=[term_text],
        )
        new_terms.append(term_data)

    # reset the terms layer with the new terms
    doc.remove_layer_elements("terms")
    for term_data in new_terms:
        if term_data.id not in terms_to_skip:
            doc.add_term_element(
                term_data, layer_to_attributes_to_ignore={"terms": {}}, comments=True
            )

    return doc


def glue_sentences_separated_by_colons(doc, language: str, nlp: dict):
    """
    Glue sentences that are separated by colons

    Args:
        doc: the NafDocument
        language: language used for lemmatization
        nlp: dictionary of nlp processors
    Returns:
        NafDocument where sentences with colons are glued
    """

    COLON = ":"

    doc_words = {word["id"]: word for word in doc.text}

    for idx, sentence in enumerate(doc.sentences):

        if sentence["text"][-1] == COLON:
            print(sentence["text"])
            print(doc.sentences[idx + 1]["text"])
            print("--")

    #     term_text = "".join([doc_words[s["id"]]["text"] for s in term["span"]])
    #     term_lemma = term["lemma"]
    #     term_pos = term["pos"]
    #     term_morphofeat = term.get("morphofeat", None)
    #     term_span = term["span"]

    #     if term_text[-1] == HARD_HYPHEN and not term_text==HARD_HYPHEN:
    #         # term ends with a hard hyphen
    #         word = doc_words[term_span[-1]['id']]
    #         word_hyphen_offset = int(word['offset'])+len(word['text'].strip())-1

    #         next_term_text = "".join([doc_words[s["id"]]["text"] for s in terms[idx+1]["span"]])
    #         if word_hyphen_offset in hyphen_offsets and next_term_text not in ["en", "of", ",", "en/of"]:

    #             if next_term_text[-1] != HARD_HYPHEN:
    #                 term_span = term["span"] + terms[idx + 1]["span"]
    #                 terms_to_skip.append(terms[idx + 1]["id"])
    #             else:
    #                 term_span = term["span"] + terms[idx + 1]["span"] + terms[idx + 2]['span']
    #                 terms_to_skip.append(terms[idx + 1]["id"])
    #                 terms_to_skip.append(terms[idx + 2]["id"])

    #             # the new term text is derived from the new span where soft hyphens are deleted
    #             term_text = "".join(
    #                 [doc_words[s["id"]]["text"] for s in term_span]
    #             )

    #             # we need to determine again the linguistical properties of the resulting term
    #             data = nlp["nl"](term_text).sentences[0].words[0]
    #             term_lemma = data.lemma
    #             term_pos = data.pos
    #             term_morphofeat = data.feats

    #     term_data = TermElement(
    #         id=term["id"],
    #         type="open",
    #         lemma=term_lemma,
    #         pos=term_pos,
    #         morphofeat=term_morphofeat,
    #         netype=None,
    #         case=None,
    #         head=None,
    #         component_of=None,
    #         compound_type=None,
    #         span=[s["id"] for s in term_span],
    #         ext_refs=list(),
    #         comment=[term_text],
    #     )
    #     new_terms.append(term_data)

    # # reset the terms layer with the new terms
    # doc.remove_layer_elements("terms")
    # for term_data in new_terms:
    #     if term_data.id not in terms_to_skip:
    #         doc.add_term_element(
    #             term_data, layer_to_attributes_to_ignore={"terms": {}}, comments=True
    #         )

    return doc

def get_context_rows(ref_text: dict, naf_layer, context_range: int) -> str:
    """
    Retrieves the line where word has been found with option to also retreive sentences/paragraphs before and after
    Args:
        ref_text: a sentence or paragraph from the sentences or paragraphs layer as a dictionary to retrieve extra
        context for
        naf: a NafDocument.sentences or NafDocument.paragaphs (can be rewritten with search_level as extra input)
        context_range: amount of context lines around ref_text
    Returns:
        result: the sentence/paragraph with surrounding context lines
    """
    for idx, text in enumerate(naf_layer):
        if ref_text == text:
            text_idx = idx

    if text_idx - context_range >= 0:
        idx_min = text_idx - context_range
    else:
        idx_min = 0

    if text_idx + context_range < len(naf_layer):
        idx_max = text_idx + context_range
    else:
        idx_max = len(naf_layer) - 1

    context_idxs = [idx for idx in range(idx_min, idx_max+1, 1)]

    result_w_context = ''
    for idx in context_idxs:
        result_w_context = result_w_context + naf_layer[idx]['text']

    return result_w_context
