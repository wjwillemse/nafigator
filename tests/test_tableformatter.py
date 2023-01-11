from nafigator.nafdocument import NafDocument
from nafigator.postprocessor.tableformatter import TableFormatter
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class TestTableFormatter(unittest.TestCase):
    # @TODO: substantial refactoring can be done when/after refactoring formats layer
    """
    The basic class that inherits unittest.TestCase
    """

    def test_1_xml2table(self):
        doc = NafDocument().open('tests/tests/test1_tabel.naf.xml')
        table_formatter = TableFormatter(doc, 'dummy_path')
        actual_dict = table_formatter.xml2table(False)
        actual_df = table_formatter.xml2table(True)

        assert isinstance(actual_dict, list)
        assert isinstance(actual_df, list)

        # check actual_dict:
        assert isinstance(actual_dict[0], tuple)
        assert isinstance(actual_dict[0][0], dict)

        # check actual_df:
        assert isinstance(actual_df[0], tuple)
        assert isinstance(actual_df[0][0], pd.DataFrame)
        assert isinstance(actual_df[0][1], dict)
        assert actual_df[0][0].shape == (2, 3)

        exp_output_dict = [({0: [None, 'Kolom 1', 'Kolom 2'],
                           1: ['Rij', 'Cell met tekst', 'Cell met tekens: 1!@'],
                           2: ['Rij', 'Volgende cell is leeg', None]},
                            {'page': '1', 'order': '1', 'shape': '(3, 3)',
                            '_bbox': '(71.98548972188634, 463.68, 439.351438935913, 686.64)',
                             'cols': ('[(72.21044437726724, 194.6007738814994), (194.6007738814994, 316.7361547762999)'
                                      ', (316.7361547762999, 439.2314631197098)]')})]

        assert actual_dict == exp_output_dict, ("expected: " + str(exp_output_dict) + ", actual: " + str(actual_dict))

    def test_2_xml2table(self):

        doc = NafDocument().open('tests/tests/test2_tabel.naf.xml')
        table_formatter = TableFormatter(doc, 'tests/tests/test2_tabel.pdf')  # initiate the TableFormatter class
        actual_dict = table_formatter.xml2table(False)
        actual_df = table_formatter.xml2table(True)

        assert isinstance(actual_dict, list)
        assert isinstance(actual_df, list)

        # check actual_dict:
        assert isinstance(actual_dict[0], tuple)
        assert isinstance(actual_dict[0][0], dict)

        # check actual_df:
        assert isinstance(actual_df[0], tuple)
        assert isinstance(actual_df[0][0], pd.DataFrame)
        assert isinstance(actual_df[0][1], dict)
        assert actual_df[0][0].shape == (5, 4)

        exp_output_dict = [({0: [None, None, None, None],
                            1: [None, None, None, None],
                             2: [None, None, None, None],
                             3: [None, None, None, None],
                             4: [None, None, None, None],
                             5: [None, None, None, None]},
                            {'page': '1', 'order': '1', 'shape': '(6, 4)',
                             '_bbox': '(71.98548972188634, 607.68, 439.351438935913, 691.68)',
                             'cols': ('[(72.22356673216446, 163.88696493349457), (163.88696493349457, 255.7884401451028'
                                      '), (255.7884401451028, 347.4499637243047), (347.4499637243047, '
                                      '439.2314631197098)]')})]

        assert actual_dict == exp_output_dict, ("expected: " + str(exp_output_dict) + ", actual: " + str(actual_dict))

    def test_3_xml2table(self):
        doc = NafDocument().open('tests/tests/test3_tabel.naf.xml')
        table_formatter = TableFormatter(doc, 'tests/tests/test3_tabel.pdf')  # initiate the TableFormatter class
        actual_dict = table_formatter.xml2table(False)
        actual_df = table_formatter.xml2table(True)

        assert isinstance(actual_dict, list)
        assert isinstance(actual_df, list)

        # check actual_dict:
        assert isinstance(actual_dict[0], tuple)
        assert isinstance(actual_dict[0][0], dict)

        # check actual_df:
        assert isinstance(actual_df[0], tuple)
        assert isinstance(actual_df[0][0], pd.DataFrame)
        assert isinstance(actual_df[0][1], dict)
        assert actual_df[0][0].shape == (3, 3)
        assert actual_df[1][0].shape == (1, 3)

        exp_output_dict = [
            (
                {0: [None, 'Kolom 1', 'Kolom 2'],
                 1: ['Rij 1', 'Eerste cell', 'Tweede cell'],
                 2: ['Rij 2', 'Derde cell', 'Vierde cell'],
                 3: ['Rij 3', 'Vijfde cell', 'Zesde cell']},
                {'page': '1', 'order': '1', 'shape': '(4, 3)',
                 '_bbox': '(71.98548972188634, 154.56, 439.351438935913, 731.52)',
                 'cols': ('[(72.21794286577993, 194.6007738814994), (194.6007738814994, 316.7361547762999), '
                          '(316.7361547762999, 439.2314631197098)]')}),
            ({0: ['Rij 4', 'Zevende cell', 'Achtste cell'],
              1: ['Rij 5', 'Negende cell', 'Tiende cell']},
             {'page': '2', 'order': '1', 'shape': '(2, 3)',
              '_bbox': '(71.98548972188634, 394.8, 439.351438935913, 714.24)',
              'cols': ('[(72.19544740024185, 194.6007738814994), (194.6007738814994, 316.7361547762999), '
                       '(316.7361547762999, 439.2314631197098)]')})]

        assert actual_dict == exp_output_dict, ("expected: " + str(exp_output_dict) + ", actual: " + str(actual_dict))

    def test_4_xml2table(self):
        doc = NafDocument().open('tests/tests/test4_tabel.naf.xml')
        table_formatter = TableFormatter(doc, 'tests/tests/test3_tabel.pdf')  # initiate the TableFormatter class
        actual_dict = table_formatter.xml2table(False)
        actual_df = table_formatter.xml2table(True)

        assert isinstance(actual_dict, list)
        assert isinstance(actual_df, list)
        exp_output_dict = []

        assert actual_dict == exp_output_dict, ("expected: " + str(exp_output_dict) + ", actual: " + str(actual_dict))

    def test_1_extract_table(self):
        table_formatter = TableFormatter(NafDocument(), 'mock_path')
        mock_table = {'page': '11', 'order': '1', 'shape': '(4, 1)',
                      '_bbox': '(71.98548972188634, 394.8, 439.351438935913, 714.24)',
                      'cols': ('[(72.19544740024185, 194.6007738814994), (194.6007738814994, 316.7361547762999), '
                               '(316.7361547762999, 439.2314631197098)]'),
                      'table': [{'row': [{'index': '0'}, {'cell': 'A'}]},
                                {'row': [{'index': '1'}, {'cell': 'B'}]},
                                {'row': [{'index': '2'}, {'cell': 'C'}]},
                                {'row': [{'index': '3'}, {'cell': 'D'}]}]}

        datadict, metadatadict = table_formatter.extract_table(mock_table)

        assert metadatadict['page'] == mock_table['page']
        assert datadict == {0: ['A'], 1: ['B'], 2: ['C'], 3: ['D']}

    def test1_is_joint_table(self):
        doc = NafDocument().open('tests/tests/test3_tabel.naf.xml')
        pdf_path = 'tests/tests/test3_tabel.pdf'
        table_formatter = TableFormatter(doc, pdf_path)

        # test where tables are joint
        metadata_table1_t = ({0: [None, 'Kolom 1', 'Kolom 2'], 1: ['Rij 1', 'Eerste cell', 'Tweede cell'],
                              2: ['Rij 2', 'Derde cell', 'Vierde cell'], 3: ['Rij 3', 'Vijfde cell', 'Zesde cell']},
                             {'page': '1', 'order': '1',
                              'shape': '(4, 3)', '_bbox': '(71.98548972188634, 154.56, 439.351438935913, 731.52)',
                              'cols': ('[(72.21794286577993, 194.6007738814994), (194.6007738814994, 316.7361547762999)'
                                       ',(316.7361547762999, 439.2314631197098)]')})
        metadata_table2_t = ({0: ['Rij 4', 'Zevende cell', 'Achtste cell'],
                              1: ['Rij 5', 'Negende cell', 'Tiende cell']},
                             {'page': '2', 'order': '1', 'shape': '(2, 3)',
                              '_bbox': '(71.98548972188634, 394.8, 439.351438935913, 714.24)',
                              'cols': ('[(72.19544740024185, 194.6007738814994), (194.6007738814994, 316.7361547762999)'
                                       ', (316.7361547762999, 439.2314631197098)]')})

        actual_true = table_formatter.is_joint_table(metadata_table1_t, metadata_table2_t)
        assert actual_true

    def test2_is_joint_table(self):
        doc = NafDocument().open('tests/tests/test5_tabel.naf.xml')
        pdf_path = 'tests/tests/test5_tabel.pdf'
        table_formatter = TableFormatter(doc, pdf_path)

        # test where tables are joint
        metadata_table1_f = ({0: ['T       1 Rij 1', 'T1 cell 1', 'T1 cell 1', 'T1 cell 1'],
                              1: ['T                 1 Rij 2', 'T1 cell 1', 'T1 cell 1', 'T1 cell 1'],
                              2: ['T         1 Rij 3', 'T1 cell 1', 'T1 cell 1', 'T1 cell 1']},
                             {'page': '1', 'order': '1',
                              'shape': '(3, 4)', '_bbox': '(71.98548972188634, 72.96, 523.3345102781137, 545.04)',
                              'cols': ('[(72.21044437726724, 185.0027085852479), (185.0027085852479, 297.5400241837969)'
                                       ', (297.5400241837969, 410.31729141475216), (410.31729141475216,'
                                       ' 523.2145344619105)]')})
        metadata_table2_f = ({0: ['T       2 Rij 1', 'T2 Cell 1', 'T2 Cell 2', None],
                              1: ['T                   2 Rij 2',
                                  'T2 Cell 3', 'T2 Cell 4', None]},
                             {'page': '2', 'order': '1', 'shape': '(2, 4)',
                              '_bbox': '(71.98548972188634, 423.59999999999997, 523.3345102781137, 747.36)',
                              'cols': ('[(72.19544740024185, 135.8126239419589), (135.8126239419589, 297.5400241837969)'
                                       ', (297.5400241837969, 490.22118500604597), (490.22118500604597, '
                                       '523.2145344619105)]')})

        actual_false = table_formatter.is_joint_table(metadata_table1_f, metadata_table2_f)
        assert not actual_false

    # @TODO: zit nog een bug in bij naf generatie van test6_tabel.pdf. Deze zit ergens in het tabellen gedeelte.

    def test_join_split_tables(self):
        doc = NafDocument().open('tests/tests/test3_tabel.naf.xml')
        pdf_path = 'tests/tests/test3_tabel.pdf'
        table_formatter = TableFormatter(doc, pdf_path)
        tables = [
            (
                {0: [None, 'Kolom 1', 'Kolom 2'],
                 1: ['Rij 1', 'Eerste cell', 'Tweede cell'],
                 2: ['Rij 2', 'Derde cell', 'Vierde cell'],
                 3: ['Rij 3', 'Vijfde cell', 'Zesde cell']},
                {'page': '1', 'order': '1', 'shape': '(4, 3)',
                 '_bbox': '(71.98548972188634, 154.56, 439.351438935913, 731.52)',
                 'cols': ('[(72.21794286577993, 194.6007738814994), (194.6007738814994, 316.7361547762999), '
                          '(316.7361547762999, 439.2314631197098)]')}),
            ({0: ['Rij 4', 'Zevende cell', 'Achtste cell'],
              1: ['Rij 5', 'Negende cell', 'Tiende cell']},
             {'page': '2', 'order': '1', 'shape': '(2, 3)',
              '_bbox': '(71.98548972188634, 394.8, 439.351438935913, 714.24)',
              'cols': ('[(72.19544740024185, 194.6007738814994), (194.6007738814994, 316.7361547762999), '
                       '(316.7361547762999, 439.2314631197098)]')})]

        actual = table_formatter.join_split_tables(tables, headers=False)
        exp_output = pd.DataFrame({0: {0: None, 1: 'Kolom 1', 2: 'Kolom 2', 3: 'Rij 4', 4: 'Zevende cell',
                                       5: 'Achtste cell'},
                                  1: {0: 'Rij 1', 1: 'Eerste cell', 2: 'Tweede cell', 3: 'Rij 5', 4: 'Negende cell',
                                  5: 'Tiende cell'},
                                  2: {0: 'Rij 2', 1: 'Derde cell', 2: 'Vierde cell', 3: np.nan, 4: np.nan, 5: np.nan},
                                  3: {0: 'Rij 3', 1: 'Vijfde cell', 2: 'Zesde cell', 3: np.nan, 4: np.nan, 5: np.nan}})
        assert_frame_equal(actual[0], exp_output)

        actual_h = table_formatter.join_split_tables(tables, headers=True)[0].to_dict()
        exp_output_h = {None: {1: 'Kolom 1', 2: 'Kolom 2', 3: 'Rij 4', 4: 'Zevende cell', 5: 'Achtste cell'}, 'Rij 1':
                        {1: 'Eerste cell', 2: 'Tweede cell', 3: 'Rij 5', 4: 'Negende cell',
                         5: 'Tiende cell'}, 'Rij 2': {1: 'Derde cell', 2: 'Vierde cell', 3: np.nan, 4: np.nan,
                                                      5: np.nan},
                        'Rij 3': {1: 'Vijfde cell', 2: 'Zesde cell', 3: np.nan, 4: np.nan, 5: np.nan}}
        assert actual_h == exp_output_h
