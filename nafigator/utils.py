# coding: utf-8

"""Utils module."""

import io
import re
import os
from lxml import etree
import pandas as pd
import logging
from nafigator import parse2naf
import docx
from docx.enum.dml import MSO_THEME_COLOR_INDEX


def dataframe2naf(
    df_meta: pd.DataFrame,
    overwrite_existing_naf: bool = False,
    rerun_files_with_naf_errors: bool = False,
    engine: str = None,
    naf_version: str = None,
    dtd_validation: bool = False,
    params: dict = {},
    nlp=None,
):
    """ """
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

        if "naf:source" in df_meta.columns:
            output = df_meta.loc[row, "naf:source"]
        else:
            if dc_source is not None:
                output = os.path.splitext(dc_source)[0] + ".naf.xml"

        if dc_source and dc_language and output:

            # logging per processed file
            log_file: str = os.path.splitext(dc_source)[0] + ".log"
            logging.basicConfig(filename=log_file, level=logging.WARNING, filemode="w")

            if os.path.exists(output) and not overwrite_existing_naf:
                # the NAF file exists and we should not overwrite existing naf files -> skip
                df_meta.loc[row, "naf:status"] = "OK"
                df_meta.loc[row, "naf:source"] = output
                continue
            elif (
                "error" in df_meta.loc[row, "naf:status"].lower()
                and not rerun_files_with_naf_errors
            ):
                # the status is ERROR and we should not rerun files with errors -> skip
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


def load_dtd(dtd_url):
    """ """
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


def time_in_correct_format(datetime_obj):
    """
    Function that returns the current time (UTC)
    """
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


def normalize_token_orth(orth):
    if "\n" in orth:
        return "NEWLINE"
    else:
        return remove_control_characters(orth)


def prepare_comment_text(text: str):
    """ """
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


def remove_illegal_chars(text):
    return re.sub(ILLEGAL_XML_CHARS_RE, "", text)


def remove_control_characters(html):
    # type: (t.Text) -> t.Text
    """
    Strip invalid XML characters that `lxml` cannot parse.
    """
    # See: https://github.com/html5lib/html5lib-python/issues/96
    #
    # The XML 1.0 spec defines the valid character range as:
    # Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    #
    # We can instead match the invalid characters by inverting that range into:
    # InvalidChar ::= #xb | #xc | #xFFFE | #xFFFF | [#x0-#x8] | [#xe-#x1F] | [#xD800-#xDFFF]
    #
    # Sources:
    # https://www.w3.org/TR/REC-xml/#charsets,
    # https://lsimons.wordpress.com/2011/03/17/stripping-illegal-characters-out-of-xml-in-python/
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
    # Otherwise we'd remove emojis by mistake on narrow-unicode builds of Python
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


def add_hyperlink(paragraph, text, url):
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(
        url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True
    )

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement("w:hyperlink")
    hyperlink.set(
        docx.oxml.shared.qn("r:id"),
        r_id,
    )

    # Create a w:r element and a new w:rPr element
    new_run = docx.oxml.shared.OxmlElement("w:r")
    rPr = docx.oxml.shared.OxmlElement("w:rPr")

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    # Create a new Run object and add the hyperlink into it
    r = paragraph.add_run()
    r._r.append(hyperlink)

    # A workaround for the lack of a hyperlink style (doesn't go purple after using the link)
    # Delete this if using a template that has the hyperlink style in it
    r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
    r.font.size = Pt(8)
    r.font.underline = True

    return hyperlink
