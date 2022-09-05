# -*- coding: utf-8 -*-

from rdflib import Graph, URIRef, Literal
import rdflib
from lxml import etree
import logging
import iribaker
import uuid

from .nafdocument import NafDocument
from .convert2rdf import UD2OLIA_mappings, mapobject

RDF = rdflib.namespace.RDF
RDFS = rdflib.namespace.RDFS
XSD = rdflib.namespace.XSD
DCTERMS = rdflib.namespace.DCTERMS
NIF = rdflib.Namespace('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#')
NIF_ONTOLOGY = 'http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/2.1'
OLIA = rdflib.Namespace("http://purl.org/olia/olia.owl#")

class NifBase(object):

    def __init__(self, uri: str=None):
        self._uri = uri

    @property
    def uri(self):
        if self._uri is not None:
            return URIRef(iribaker.to_iri(self._uri))
        else:
            return None

    def set_uri(self, uri: str=None):
        self._uri = uri

class NifString(NifBase):

    def __init__(self,
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 offsetBasedString: bool=True,
                 uri: str=None):
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        self.referenceContext = referenceContext
        self.anchorOf = anchorOf
        self.offsetBasedString = offsetBasedString
        if offsetBasedString:
            super().__init__(uri=uri+"#offset_"+str(beginIndex)+"_"+str(endIndex))
        else:
            super().__init__(uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            if self.offsetBasedString:
                yield (self.uri, RDF.type, NIF.OffsetBasedString)
            else:
                yield (self.uri, RDF.type, NIF.String)
            if self.beginIndex is not None:
                yield (self.uri, NIF.beginIndex, Literal(self.beginIndex, datatype=XSD.nonNegativeInteger))
            if self.endIndex is not None:
                yield (self.uri, NIF.endIndex, Literal(self.endIndex, datatype=XSD.nonNegativeInteger))
            if self.referenceContext is not None:
                yield (self.uri, NIF.referenceContext, self.referenceContext.uri)
            if self.anchorOf is not None:
                yield (self.uri, NIF.anchorOf, Literal(self.anchorOf, datatype=XSD.string))


class NifContext(NifString):

    def __init__(self,
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 isString: str=None,
                 offsetBasedString: bool=True,
                 firstSentence: str=None,
                 lastSentence: str=None,
                 uri: str=None):
        self.isString = isString
        self.firstSentence = firstSentence
        self.lastSentence = lastSentence
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext, 
                         anchorOf=anchorOf, 
                         offsetBasedString=offsetBasedString,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Context)
            if self.isString is not None:
                yield (self.uri, NIF.isString, Literal(self.isString, datatype=XSD.string))
            if self.firstSentence is not None:
                yield (self.uri, NIF.firstSentence, self.firstSentence.uri)
            if self.lastSentence is not None:
                yield (self.uri, NIF.lastSentence, self.lastSentence.uri)

            for triple in super().triples():
                yield triple


class NifStructure(NifString):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 anchorOf: str=None,
                 offsetBasedString: bool=True,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            for triple in super().triples():
                yield triple

class NifPhrase(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Phrase)
            for triple in super().triples():
                yield triple


class NifSentence(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 nextSentence: str=None,
                 previousSentence: str=None,
                 firstWord: str=None,
                 lastWord: str=None,
                 uri: str=None):
        self.nextSentence = nextSentence
        self.previousSentence = previousSentence
        self.firstWord = firstWord
        self.lastWord = lastWord
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Sentence)
            for triple in super().triples():
                yield triple
            if self.nextSentence is not None:
                yield (self.uri, NIF.nextSentence, self.nextSentence.uri)
            if self.previousSentence is not None:
                yield (self.uri, NIF.previousSentence, self.previousSentence.uri)
            if self.firstWord is not None:
                yield (self.uri, NIF.firstWord, self.firstWord.uri)
            if self.lastWord is not None:
                yield (self.uri, NIF.lastWord, self.lastWord.uri)

class NifParagraph(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Paragraph)
            for triple in super().triples():
                yield triple

class NifPage(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 anchorOf: str=None,
                 uri: str=None):
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Page)
            for triple in super().triples():
                yield triple

# class NifTitle(NifStructure):

#     def __init__(self, uri: str=None):
#         super().__init__(uri)

class NifWord(NifStructure):

    def __init__(self, 
                 beginIndex: int=None,
                 endIndex: int=None,
                 referenceContext: str=None,
                 offsetBasedString: bool=True,
                 nifsentence: str=None,
                 anchorOf: str=None,
                 lemma: str=None,
                 pos: str=None,
                 morphofeats:list=[],
                 nextWord: str=None,
                 previousWord: str=None,
                 uri: str=None):
        self.nifsentence = nifsentence
        self.lemma = lemma
        self.pos = pos
        self.morphofeats = morphofeats
        self.nextWord = nextWord
        self.previousWord = previousWord
        self.dependency = []
        self.dependencyRelationType = None
        super().__init__(beginIndex=beginIndex, 
                         endIndex=endIndex, 
                         referenceContext=referenceContext,
                         offsetBasedString=offsetBasedString,
                         anchorOf=anchorOf,
                         uri=uri)

    def add_dependency(self, dependency: str=None):
        self.dependency.append(dependency)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.Word)
            if self.nifsentence is not None:
                yield (self.uri, NIF.sentence, self.nifsentence.uri)
            for triple in super().triples():
                yield triple
            if self.lemma is not None:
                yield (self.uri, NIF.lemma, Literal(self.lemma, datatype=XSD.string))
            if self.pos is not None:
                yield (self.uri, NIF.oliaLink, OLIA[self.pos])
            if self.morphofeats is not None and self.morphofeats != []:
                for morphofeat in self.morphofeats:
                    yield (self.uri, NIF.oliaLink, OLIA[morphofeat])
            if self.nextWord is not None:
                yield (self.uri, NIF.nextWord, self.nextWord.uri)
            if self.previousWord is not None:
                yield (self.uri, NIF.previousWord, self.previousWord.uri)
            if self.dependencyRelationType is not None:
                yield (self.uri, NIF.dependencyRelationType, Literal(self.dependencyRelationType, datatype=XSD.string))
            for dep in self.dependency:
                yield (self.uri, NIF.dependency, dep.uri)

class NifContextCollection(NifBase):

    def __init__(self,
                 hasContext: list=[],
                 uri: str=None):
        self.hasContext = hasContext
        super().__init__(uri)

    def add_context(self, context: NifContext=None):
        if context is not None:
            self.hasContext.append(context)

    def triples(self):
        """
        Generates all the triples
        """
        if self.uri is not None:
            yield (self.uri, RDF.type, NIF.ContextCollection)
            yield (self.uri, DCTERMS.conformsTo, URIRef(NIF_ONTOLOGY))
            for context in self.hasContext:
                yield (self.uri, NIF.hasContext, context.uri)

class naf2nif(object):

    def __init__(self,
                 uri: str=None,
                 doc: NafDocument=None):
        self.graph = Graph()
        self.graph.bind("nif", NIF)
        self.graph.bind("olia", "http://purl.org/olia/olia.owl#")

        doc_uri = doc.header['public']['{http://purl.org/dc/elements/1.1/}uri']

        doc_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, doc_uri))

        nif_context = NifContext(beginIndex=0,
                       endIndex=len(doc.raw),
                       isString=doc.raw,
                       offsetBasedString=True,
                       uri=uri+"/"+doc_uuid)
        nif_context.referenceContext = nif_context

        nif_collection = NifContextCollection(uri=uri+"/collection")
        nif_collection.add_context(nif_context)

        words = {word['id']: word for word in doc.text}
        terms = {term['id']: term for term in doc.terms}

        nif_sentences = []
        nif_words = []
        nif_terms = []
        doc_sentences = doc.sentences
        for sent_idx, sentence in enumerate(doc_sentences):
            beginIndex = int(words[sentence['span'][0]['id']]['offset'])
            endIndex = (int(words[sentence['span'][-1]['id']]['offset'])+
                       int(words[sentence['span'][-1]['id']]['length']))
            anchorOf = " ".join([words[s['id']]['text'] for s in sentence['span']])
            nif_sentence = NifSentence(beginIndex=beginIndex,
                                       endIndex=endIndex,
                                       referenceContext=nif_context,
                                       offsetBasedString=True,
                                       anchorOf=anchorOf,
                                       # annotation reference missing
                                       uri=uri+"/"+doc_uuid)
            sentence['nif'] = nif_sentence
            nif_sentences.append(nif_sentence)

            if sent_idx == 0:
                nif_context.firstSentence = nif_sentence
            if sent_idx == len(doc_sentences) - 1:
                nif_context.lastSentence = nif_sentence

            for word_idx, word_id in enumerate(sentence['span']):
                word = words[word_id['id']]
                beginIndex = int(word['offset'])
                endIndex = (int(word['offset'])+int(word['length']))
                anchorOf = word['text']
                nif_word = NifWord(beginIndex=beginIndex,
                                   endIndex=endIndex,
                                   referenceContext=nif_context,
                                   offsetBasedString=True,
                                   anchorOf=anchorOf,
                                   nifsentence=nif_sentence,
                                   # annotation reference missing
                                   uri=uri+"/"+doc_uuid)
                word['nif'] = nif_word
                nif_words.append(nif_word)

            # Add nextWord and previousWord
            for word_idx, word_id in enumerate(sentence['span']):
                word = words[word_id['id']]
                # add firstWord to sentence
                if word_idx == 0:
                    nif_sentence.firstWord = word['nif']
                # add lastWord to sentence
                if word_idx == len(sentence['span']) - 1:
                    nif_sentence.lastWord = word['nif']
                if word_idx < len(sentence['span']) - 1:
                    word['nif'].nextWord = words[sentence['span'][word_idx + 1]['id']]['nif']
                if word_idx > 0:
                    word['nif'].previousWord = words[sentence['span'][word_idx - 1]['id']]['nif']

            for term in sentence['terms']:
                term_words = [s['id'] for s in terms[term['id']]['span']]
                beginIndex = int(words[term_words[0]]['offset'])
                endIndex = (int(words[term_words[-1]]['offset'])+
                            int(words[term_words[-1]]['length']))
                term_lemma = terms[term['id']].get('lemma', None)
                term_pos = terms[term['id']].get('pos', None)
                term_pos = mapobject("pos", term_pos.lower()).replace("olia:", "")

                term_morphofeats = []
                morphofeats = terms[term['id']].get('morphofeat', None)
                print(str(term['id']) + ": " + str(morphofeats)) 
                if morphofeats is not None:
                    for feat in morphofeats.split("|"):

                        if (
                            feat.split("=")[0] == "Poss" #in ["Foreign", "Reflex", "Poss", "Abbr"]
                            and feat.split("=")[1] == "Yes"
                        ):
                            print("  " + str(feat))
                            term_morphofeats.append("PossessivePronoun")
                        else:
                            term_morphofeats.append(mapobject(feat.split("=")[0], feat.split("=")[1]).replace("olia:", ""))

                nif_term = NifWord(beginIndex=beginIndex,
                                   endIndex=endIndex,
                                   offsetBasedString=True,
                                   lemma=term_lemma,
                                   pos=term_pos,
                                   morphofeats=term_morphofeats,
                                   # annotation reference missing
                                   uri=uri+"/"+doc_uuid)
                terms[term['id']]['nif'] = nif_term
                nif_terms.append(nif_term)

        # store nif_pages
        nif_pages = []
        page_number = int(doc.text[0]['page'])
        page_start = int(doc.text[0]['offset'])
        page_end = int(doc.text[0]['offset'])
        for word in doc.text:
            if int(word['page']) != page_number:
                nif_page = NifPage(beginIndex=page_start,
                                   endIndex=page_end,
                                   referenceContext=nif_context,
                                   offsetBasedString=True,
                                   uri=uri+"/"+doc_uuid)
                page_start = int(word['offset'])
                page_end = int(word['offset']) + int(word['length'])
                nif_pages.append(nif_page)
                page_number += 1
            page_end = int(word['offset']) + int(word['length'])
        nif_page = NifPage(beginIndex=page_start,
                           endIndex=page_end,
                           referenceContext=nif_context,
                           offsetBasedString=True,
                           uri=uri+"/"+doc_uuid)
        nif_pages.append(nif_page)

        # add collection of sentences to nif:Context
        seq_element = rdflib.term.BNode()
        self.graph.add((nif_context.uri, NIF.hasSentences, seq_element))
        rdflib.collection.Collection(self.graph, seq_element, [sentence['nif'].uri for sentence in doc_sentences])

        # add collection of words to each nif:Sentence
        for sentence in doc_sentences:
            seq_element = rdflib.term.BNode()
            self.graph.add((sentence['nif'].uri, NIF.hasWords, seq_element))
            rdflib.collection.Collection(self.graph, seq_element, [words[word_id['id']]['nif'].uri for word_id in sentence['span']])

        # Add dependencies:
        for dep in doc.deps:
            from_term = dep['from_term']
            to_term = dep['to_term']
            rfunc = dep['rfunc']
            terms[from_term]['nif'].add_dependency(terms[to_term]['nif'])
            terms[from_term]['nif'].dependencyRelationType = rfunc

        # Add nextSentence and previousSentence to make graph traversable
        for sent_idx, nif_sentence in enumerate(nif_sentences):
            if sent_idx < len(nif_sentences) - 1:
                nif_sentence.nextSentence = nif_sentences[sent_idx + 1]
            if sent_idx > 0:
                nif_sentence.previousSentence = nif_sentences[sent_idx - 1]

        nif_paragraphs = []
        for paragraph in doc.paragraphs:
            beginIndex = int(words[paragraph['span'][0]['id']]['offset'])
            endIndex = (int(words[paragraph['span'][-1]['id']]['offset'])+
                       int(words[paragraph['span'][-1]['id']]['length']))
            anchorOf = " ".join([words[s['id']]['text'] for s in paragraph['span']])
            nif_paragraph = NifParagraph(beginIndex=beginIndex,
                                         endIndex=endIndex,
                                         referenceContext=nif_context,
                                         offsetBasedString=True,
                                         # annotation reference missing
                                         uri=uri+"/"+doc_uuid)
            nif_paragraphs.append(nif_paragraph)

        for triple in nif_context.triples():
            self.graph.add(triple)

        for triple in nif_collection.triples():
            self.graph.add(triple)

        for nif_page in nif_pages:
            for triple in nif_page.triples():
                self.graph.add(triple)

        for nif_sentence in nif_sentences:
            for triple in nif_sentence.triples():
                self.graph.add(triple)

        for nif_paragraph in nif_paragraphs:
            for triple in nif_paragraph.triples():
                self.graph.add(triple)

        for nif_word in nif_words + nif_terms:
            for triple in nif_word.triples():
                self.graph.add(triple)


