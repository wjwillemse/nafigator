# coding: utf-8

"""Utils module."""

import io
import re
from lxml import etree


def load_dtd(dtd_url):

    dtd = None
    r = open(dtd_url)
    if r:
        dtd_file_object = io.StringIO(r.read())
        dtd = etree.DTD(dtd_file_object)
    if dtd is None:
        logging.error("failed to load dtd from"+str(dtd_url))
    else:
        logging.info("Succesfully to load dtd from"+str(dtd_url))
    return dtd


def time_in_correct_format(datetime_obj):
    """
    Function that returns the current time (UTC)
    """
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


# Only allow legal strings in XML:
# http://stackoverflow.com/a/25920392/2899924
illegal_pattern = re.compile(
    "[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+"
)


def remove_illegal_chars(text):
    return re.sub(illegal_pattern, "", text)


def normalize_token_orth(orth):
    if "\n" in orth:
        return "NEWLINE"
    else:
        return remove_illegal_chars(orth)
