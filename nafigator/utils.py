# coding: utf-8

"""Utils module."""

import io
import re
from lxml import etree


def load_dtd_as_file_object(dtd_url, verbose=0):

    dtd = None
    r = open(dtd_url)
    if r:
        dtd_file_object = io.StringIO(r.read())
        dtd = etree.DTD(dtd_file_object)
    if verbose >= 1:
        if dtd is None:
            print(f'failed to load dtd from {dtd_url}')
        else:
            print(f'succesfully loaded dtd from {dtd_url}')
    return dtd


def time_in_correct_format(datetime_obj):
    """
    Function that returns the current time (UTC)
    """
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


# Only allow legal strings in XML:
# http://stackoverflow.com/a/25920392/2899924
illegal_pattern = re.compile('[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+')


def remove_illegal_chars(text):
    return re.sub(illegal_pattern, '', text)


def normalize_token_orth(orth):
    if '\n' in orth:
        return 'NEWLINE'
    else:
        return remove_illegal_chars(orth)
