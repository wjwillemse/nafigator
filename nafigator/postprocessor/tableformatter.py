from nafigator.nafdocument import NafDocument
from collections import defaultdict
import pandas as pd
from numpy import allclose
import ast
from PyPDF2 import PdfFileReader


class TableFormatter():
    def __init__(
        self,
        doc: NafDocument(),
        pdf_path: str
    ) -> None:
        self.doc = doc
        self.pdf_path = pdf_path
        self.tables_df = None
        self.tables_dict = None

    def get_dataframe(self, datadict):
        """
        Converts a table in dictionary format to dataframe.

        Args:
        datadict: dictionary with table data

        Return:
        df: dataframe with table
        """

        df = pd.DataFrame.from_dict(datadict, orient='index')
        df.columns = df.iloc[0]
        df = df[1:]
        return df

    def extract_table(self, table):
        """
        Extracts a single table from the format layer in a naf document.

        Args:
        table: dictionary of doc.formats with metadata and cell data

        Returns
        datadict: dictionary with key row number and values list with cells
        metadatadict: dictionary with keys:page, order, shape
        """

        datadict = defaultdict(list)
        metadatadict = {key: table[key] for key in ['page', 'order', 'shape', '_bbox', 'cols']}

        # fill per row the datadict dict
        for row in table['table']:
            rowlist = row['row']
            index = int(rowlist[0]['index'])
            values = [cell['cell'] for cell in rowlist[1::]]
            datadict[index] = values

        return datadict, metadatadict

    def xml2table(self, dataframe: bool = False):
        # TODO optimize to generate both dict as well as df, adding it as a attribute
        """
        Extract the tables in xml format from a naf file and returns the content and metadata as a list of tuples.

        Args
        dataframe: boolean value. Default is False, meaning that the table data and metadata is returned as
        a dictionary. If True it is returned as a dataframe

        Returns
        tables: list of tuples with dictionary with table and metadata
        """
        tables = []
        for f in self.doc.formats:
            if 'tables' in f.keys():
                for table in f['tables']:

                    # create dict for data and metadata
                    datadict, metadatadict = self.extract_table(table)

                    # change data to dict or dataframe
                    if dataframe:
                        data = self.get_dataframe(datadict)
                    else:
                        data = dict(datadict)

                    # fill list with tuple per table with data and metadata
                    tables.append((data, metadatadict))
            if dataframe:
                self.tables_df = tables
            else:
                self.tables_dict = tables

        return tables

    def is_joint_table(self, table1: tuple,
                       table2: tuple) -> bool:
        """
        Determines whether a table in the document belongs to the previous table on the previous page.

        Args:
            pdf_path: the path to the pdf file of these tables. The table is a tuple with two dictionaries,
            one with the content and one with the meta data.
            table1: The table before the table to be evaluated.
            table2: The table to be evaluated.

        Returns:
            True or False. True being belonging to the previous table on the previous page
        """
        page_table1 = int(table1[1]['page'])
        page_table2 = int(table2[1]['page'])
        if page_table2 == page_table1+1:
            # check if the tables have the same amount of columns
            if ast.literal_eval(table2[1]['shape'])[1] == ast.literal_eval(table1[1]['shape'])[1]:
                # Get page height
                pdf_doc = PdfFileReader(open(self.pdf_path, 'rb'))
                pageNr = page_table1
                _, _, _, page_height = pdf_doc.getPage(pageNr).mediaBox

                # Get the y coordinates of the tables
                _, y_bottom_table1, _, _ = ast.literal_eval(table1[1]['_bbox'])
                _, _, _, y_top_table2 = ast.literal_eval(table2[1]['_bbox'])

                # Evaluate if the first table ends in the last 15% of the page
                # and the second table starts in the first 15% of the page
                # @TODO: change to last row height & fist row height
                # @TODO: make cutoff variable by making it an argument
                if y_bottom_table1 < .20*round(page_height) and \
                        y_top_table2 > .80*round(page_height):

                    table1_cols_width = [col[1]-col[0] for col in ast.literal_eval(table1[1]['cols'])]
                    table2_cols_width = [col[1]-col[0] for col in ast.literal_eval(table2[1]['cols'])]

                # Evaluate if the column widths of the two tables are similar
                    return(allclose(table1_cols_width,
                                    table2_cols_width,
                                    atol=3,
                                    rtol=0))
                else:
                    return False
            else:
                return False
        else:
            return False

    def join_split_tables(self, tables: list, headers: bool = False):  # pdf_path: str,
        # TODO: optimize the table parameter. To be removed and added as an attribute.
        # Now the functions need to be called in series
        """
        Joins bordered tables that had been split during conversion of a pdf document to a naf file.

        Args:
            pdf_path: path to the pdf file
            tables: a list of tables extracted from a naf file in tuple format.
                The tuples contain the table content and the metadata.
            headers: if true, the first row is taken as headers

        Returns:
            a list with dataframes containing the tables extracted from the pdf file without split tables.
        """
        tables_df = [pd.DataFrame(table[0]) for table in tables]

        # Check if a table belong to the previous table
        check_joint_table = [self.is_joint_table(tables[i], tables[i+1])
                             for i in range(0, len(tables)-1)]

        # Create a table number list
        tableNr = 1
        tableNr_list = [1]
        for check in check_joint_table:
            if check is True:
                tableNr_list.append(tableNr)
            else:
                tableNr = tableNr + 1
                tableNr_list.append(tableNr)

        # Group tables belonging together
        grouped_tables = [[tables_df[count]
                           for count, check in enumerate([tableNr == i for tableNr in tableNr_list])
                           if check is True]
                          for i in range(1, max(tableNr_list)+1)]

        # Join grouped tables
        joint_tables = [pd.concat(grouped_tables[i], axis=0, ignore_index=True) for i in range(0, max(tableNr_list))]

        # Make first row header
        if headers:
            header_tables = []
            for joint_table in joint_tables:
                new_header = joint_table.iloc[0]
                joint_table = joint_table[1:]
                joint_table.columns = new_header
                header_tables.append(joint_table)
            joint_tables = header_tables.copy()

        return joint_tables
