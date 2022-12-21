import unittest
import pandas as pd
import numpy as np


unittest.TestLoader.sortTestMethodsUsing = None


class TestParse2naf(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    def test_create_params():
        '''
        This function tests whether the input params are updated
        input:  str, str, str, str, bool, params dict, any
        level: 0
        scenarios: input = nafdocument or something else
        '''

    def test_evaluate_naf():
        '''
        This function tests whether the expected logging errors occur
        input: dict
        level: 1
        scenarios: check all logging
        '''

    def test_process_preprocess_steps():
        '''
        tests whether the input is encoded correctly and
        tests if the right conversion of input document is used
        input: dict
        level: 1 (imports from preprocessor)
        scenarios: check generated text
        '''

    def test_process_linguistic_layers():
        '''
        test for multiple layers add
        input: dict
        level: 1
        scenarios: check output preprocess layer
        '''

    def test_process_linguistic_steps():
        '''
        test for multiple language input
        input: dict
        level: 1
        scenarios: check language and engine
        '''

    def test_derive_text_from_formats_layer():
        '''
        test for expected text return
        input: dict
        level: 0
        scenarios:  check text with formats
                    check text without formats
                    check for different spaces
        '''

    def test_entities_generator():
        '''tests if start and end are right
        input: str, dict
        level: 0
        scenarios: check entities for multiple input
        '''

    def test_chunks_for_doc():
        '''
        test if span is right
        input: str, dict
        level: 0
        scenarios:  check chunks for ADP
                    check chunks for not ADP
        '''

    def test_chunk_tuples_for_doc():
        '''
        test chunk element on ...?
        input: str, dict
        level: 0
        scenarios: check tuples for multiple input
        '''

    def test_dependencies_to_add():
        '''
        test output on dependencies that are added
        input: str, str, int, dict
        level: 0
        scenarios: check dependency list for multiple input
        '''

    def test_add_entities_layer():
        '''
        test if output entities layer = correct
        input: dict
        level: 1
        scenarios: check entities for multiple input
        '''

    def test_add_text_layer():
        '''
        test if output text layer = correct
        input: dict
        level: 1
        scenarios: check text layer vs text
        '''

    def test_add_terms_layer():
        '''
        test if output terms layer = correct
        input: dict
        level: 1
        scenarios: check terms layer vs terms
        '''

    def test_add_deps_layer():
        '''
        test if output deps layer = correct
        input: dict
        level: 1
        scenarios: check dependencies layer vs dependencies
        '''

    def test_add_chunks_layer():
        '''
        test if output chunks layer = correct
        input: dict
        level: 1
        scenarios: check chunks layer vs chunks
        '''

    def test_add_formats_layer():
        '''
        test if output formats layer = correct
        input: dict
        level: 1
        scenarios: check format elements layer vs format elements
        '''

    def test_get_next_mw_id():
        '''
        test multiword id output
        input: dict
        level: 0
        scenarios: check ids for multiple input
        '''

    def test_add_multiwords_layer():
        '''
        test multiword output data
        input: dict
        level: 1
        scenarios: check multiword layer vs multiword
        '''

    def test_raw_layer():
        '''
        test multiword output data
        input: dict
        level: 1
        scenarios: check multiword layer vs multiword
        '''
