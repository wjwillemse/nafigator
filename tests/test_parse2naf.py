import unittest
import pandas as pd
import numpy as np


unittest.TestLoader.sortTestMethodsUsing = None


class TestParse2naf(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    def test_create_params(self):
        """
        This function tests whether the input params are updated
        input:  str, str, str, str, bool, params dict, any
        level: 0
        scenarios: input = nafdocument or something else
        """
        pass

    def test_evaluate_naf(self):
        """
        This function tests whether the expected logging errors occur
        input: dict
        level: 1
        scenarios: check all logging
        """
        pass

    def test_process_preprocess_steps(self):
        """
        tests whether the input is encoded correctly and
        tests if the right conversion of input document is used
        input: dict
        level: 1 (imports from preprocessor)
        scenarios: check generated text
        """
        pass

    def test_process_linguistic_layers(self):
        """
        test for multiple layers add
        input: dict
        level: 1
        scenarios: check output preprocess layer
        """
        pass

    def test_process_linguistic_steps(self):
        """
        test for multiple language input
        input: dict
        level: 1
        scenarios: check language and engine
        """
        pass

    def test_derive_text_from_formats_layer(self):
        """
        test for expected text return
        input: dict
        level: 0
        scenarios:  check text with formats
                    check text without formats
                    check for different spaces
        """
        pass

    def test_entities_generator(self):
        """tests if start and end are right
        input: str, dict
        level: 0
        scenarios: check entities for multiple input
        """
        pass

    def test_chunks_for_doc(self):
        """
        test if span is right
        input: str, dict
        level: 0
        scenarios:  check chunks for ADP
                    check chunks for not ADP
        """
        pass

    def test_chunk_tuples_for_doc(self):
        """
        test chunk element on ...?
        input: str, dict
        level: 0
        scenarios: check tuples for multiple input
        """
        pass

    def test_dependencies_to_add(self):
        """
        test output on dependencies that are added
        input: str, str, int, dict
        level: 0
        scenarios: check dependency list for multiple input
        """
        pass

    def test_add_entities_layer(self):
        """
        test if output entities layer = correct
        input: dict
        level: 1
        scenarios: check entities for multiple input
        """
        pass

    def test_add_text_layer(self):
        """
        test if output text layer = correct
        input: dict
        level: 1
        scenarios: check text layer vs text
        """
        pass

    def test_add_terms_layer(self):
        """
        test if output terms layer = correct
        input: dict
        level: 1
        scenarios: check terms layer vs terms
        """
        pass

    def test_add_deps_layer(self):
        """
        test if output deps layer = correct
        input: dict
        level: 1
        scenarios: check dependencies layer vs dependencies
        """
        pass

    def test_add_chunks_layer(self):
        """
        test if output chunks layer = correct
        input: dict
        level: 1
        scenarios: check chunks layer vs chunks
        """
        pass

    def test_add_formats_layer(self):
        """
        test if output formats layer = correct
        input: dict
        level: 1
        scenarios: check format elements layer vs format elements
        """
        pass

    def test_get_next_mw_id(self):
        """
        test multiword id output
        input: dict
        level: 0
        scenarios: check ids for multiple input
        """
        pass

    def test_add_multiwords_layer(self):
        """
        test multiword output data
        input: dict
        level: 1
        scenarios: check multiword layer vs multiword
        """
        pass

    def test_raw_layer(self):
        """
        test multiword output data
        input: dict
        level: 1
        scenarios: check multiword layer vs multiword
        """
        pass
