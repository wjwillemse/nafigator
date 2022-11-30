# coding: utf-8

"""nif collection"""

import rdflib
import logging
from zipfile import ZipFile
from collections import defaultdict
import pandas as pd
import re

namespaces = {
    "rdf": rdflib.namespace.RDF,
    "dc": rdflib.namespace.DC,
    "dcterms": rdflib.namespace.DCTERMS,
    "rdfs": rdflib.namespace.RDFS,
    "xsd": rdflib.namespace.XSD,
    "nif": "http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#",
    "olia": "http://purl.org/olia/olia.owl#",
}

class NifGraph(rdflib.Graph):
    """
    The NifGraph class (subclass of a rdflib.Graph)
    """

    def __init__(
        self,
        file: str=None
    ):
        super().__init__()
        if file is not None:
            self.open(file)
        for key in namespaces:
            self.bind(key, namespaces[key])

    @property
    def context(self):
        """
        """
        # derive the conformsTo from the collection
        q = """
        SELECT ?s
        WHERE {
            ?a rdf:type nif:ContextCollection .
            ?a dcterms:conformsTo ?s
        }"""
        qres = self.query(q)
        dcterms_conformsTo = [row[0] for row in qres]

        # find all context in the graphs with corresponding data
        q = """SELECT ?s ?p ?o WHERE { ?s rdf:type nif:Context . ?s ?p ?o . }"""
        results = self.query(q)

        # construct DataFrame from query results
        d = defaultdict(dict)
        index = list()
        columns = set()
        for result in results:
            idx = result[0].n3(self.namespace_manager)
            col = result[1].n3(self.namespace_manager)
            if isinstance(result[2], rdflib.term.Literal):
                val = result[2].value
            else:
                val = result[2].n3(self.namespace_manager)
            if ("dc:" in col or "dcterms:" in col):
                d[idx][col] = val
                columns.add(col)
                index.append(idx)

        df = pd.DataFrame(
            index=index,
            columns=columns,
            data = [[d[idx][col] for col in columns] for idx in index] 
        )
        df['dcterms:conformsTo'] = [dcterms_conformsTo]*len(df.index)
        return df

    def natural_sort(self, l): 
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)

    @property
    def sentences(self):
        """
        """
        return self.extract(rdf_type="nif:Sentence")

    @property
    def sentences_no_accents(self):
        """
        """
        return self.extract(rdf_type="nif:Sentence", predicate="nif:anchorOf_no_accents")

    @property
    def sentences_no_diacritics(self):
        """
        """
        return self.extract(rdf_type="nif:Sentence", predicate="nif:anchorOf_no_diacritics")

    @property
    def words(self):
        """
        """
        return self.extract(rdf_type="nif:Word")

    @property
    def words_no_accents(self):
        """
        """
        return self.extract(rdf_type="nif:Word", predicate="nif:anchorOf_no_accents")

    @property
    def words_no_diacritics(self):
        """
        """
        return self.extract(rdf_type="nif:Word", predicate="nif:anchorOf_no_diacritics")

    @property
    def lemmas(self):
        """
        """
        return self.extract(rdf_type="nif:Word", predicate="nif:lemma")

    @property
    def lemmas_no_accents(self):
        """
        """
        return self.extract(rdf_type="nif:Word", predicate="nif:lemma_no_accents")

    @property
    def lemmas_no_diacritics(self):
        """
        """
        return self.extract(rdf_type="nif:Word", predicate="nif:lemma_no_diacritics")

    @property
    def olia_annotations(self):
        """
        """
        df = self.extract(rdf_type="nif:Word", predicate="nif:oliaLink").reset_index()
        df[1] = True
        df = df.pivot_table(index=['index'], columns=['nif:oliaLink'], values=True, fill_value=0)
        df.index = self.natural_sort(df.index)
        return df

    def extract(self, 
                rdf_type: str=None, 
                predicate: str="nif:anchorOf"):
        """
        """
        q = """
        SELECT ?a ?s
        WHERE {
            ?a rdf:type """+rdf_type+""" .
            ?a """+predicate+""" ?s .
        }"""
        qres = self.query(q)
        # construct DataFrame from query results
        index = [
            row[0].n3(self.namespace_manager) 
            for row in qres
        ]
        columns = [predicate]
        data = [
            row[1].value 
            if isinstance(row[1], rdflib.Literal) 
            else row[1].n3(self.namespace_manager) 
            for row in qres
        ]
        df = pd.DataFrame(
            index=index,
            columns=columns,
            data=data
        )
        # apply natural sort on indices (because they contain offsets without preceding zeros)
        df.index = self.natural_sort(df.index)
        df.index.name = "index"
        return df

    def open(self, 
             file: str=None):
        """
        """
        if file[-3:].lower() == "zip":
            with ZipFile(file, mode="r") as zipfile:
                logging.info("Reading zip file " + file)
                for filename in zipfile.namelist():
                    with zipfile.open(filename) as f:
                        logging.info(".. Parsing file " + filename + " from zip file")
                        self.parse(data=f.read().decode(), format='hext')
        elif file[-4:].lower() == "hext":
            with open(file, encoding='utf-8') as f:
                logging.info(".. Parsing file " + file + "")
                self.parse(data=f.read(), format='hext')
        elif file[-3:].lower() == "ttl":
            with open(file, encoding='utf-8') as f:
                logging.info(".. Parsing file " + file + "")
                self.parse(data=f.read(), format='ttl')

