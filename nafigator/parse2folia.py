# coding: utf-8

"""Main module."""

from datetime import datetime
import sys
import click
import logging
import os
import re

from .linguisticprocessor import stanzaProcessor
from .linguisticprocessor import spacyProcessor

from nafigator import __version__

import folia.main as folia

from lxml import etree
import lxml.html

from .const import ProcessorElement
from .const import Entity
from .const import WordformElement
from .const import TermElement
from .const import EntityElement
from .const import DependencyRelation
from .const import ChunkElement
from .const import RawElement
from .const import MultiwordElement
from .const import ComponentElement
from .const import udpos2nafpos_info
from .const import hidden_table
from .utils import normalize_token_orth
from .utils import remove_illegal_chars

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

SETPREFIX = (
    "https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/spacy/spacy"
)

FORMATS_LAYER_TAG = "formats"


@click.command()
@click.option(
    "--input", default="data/example.pdf", prompt="input file", help="The input file"
)
@click.option(
    "--output",
    default="data/example.folia.xml",
    prompt="output file",
    help="The output file",
)
@click.option(
    "--engine",
    default="stanza",
    prompt="NLP-package",
    help="The package to parse the text",
)
@click.option(
    "--language", default="en", prompt="language", help="The language of the input file"
)
def nafigator(input: str, output: str, engine: str, language: str):
    """ """
    log_file: str = "".join(output.split(".")[0:-1]) + ".log"
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode="w")
    foliadoc = generate_folia(input=input, engine=engine, language=language)
    foliadoc.save(output)


def generate_folia(
    input: str = None,
    engine: str = None,
    language: str = None,
    params: dict = {},
    nlp=None,
):
    """ """
    if (input is None) or not (os.path.isfile(input)):
        logging.error("no or non-existing input specified")
        return None
    if engine is None:
        logging.error("no engine specified")
        return None
    if language is None:
        logging.error("no language specified")
        return None

    params = create_params(
        input=input,
        engine=engine,
        language=language,
        params=params,
        nlp=nlp,
    )

    process_preprocess_steps(params)

    process_linguistic_steps(params)

    return params["folia"]


def create_params(
    input: str = None,
    engine: str = None,
    language: str = None,
    params: dict = {},
    nlp=None,
):
    """ """
    params["engine_name"] = engine
    params["nlp"] = nlp

    if "metadata" not in params.keys():
        params["metadata"] = dict()

    if params["metadata"].get("identifier", None) is None:
        docid = ".".join(os.path.basename(input).replace(" ", "_").split(".")[:-1])
        if not folia.isncname(docid):
            if docid[0].isnumeric():
                docid = "D" + docid
            docid = docid.replace(":", "_").replace(" ", "_")
        params["metadata"]["identifier"] = docid

    if params["metadata"].get("source", None) is None:
        params["metadata"]["source"] = input
    if params["metadata"].get("language", None) is None:
        params["metadata"]["language"] = language

    params["no_paragraphs"] = False
    params["debug"] = False
    params["setprefix"] = SETPREFIX

    # # set default linguistic parameters
    # if "linguistic_layers" not in params.keys():
    #     params["linguistic_layers"] = [
    #         "text",
    #         "terms",
    #         "entities",
    #         "deps",
    #         "raw",
    #         "multiwords",
    #     ]
    # if params.get("cdata", None) is None:
    #     params["cdata"] = True
    # if params.get("map_udpos2naf_pos", None) is None:
    #     params["map_udpos2naf_pos"] = False
    # if params.get("layer_to_attributes_to_ignore", None) is None:
    #     params["layer_to_attributes_to_ignore"] = {"terms": {}}
    if params.get("replace_hidden_characters", None) is None:
        params["replace_hidden_characters"] = True
    # if params.get("comments", None) is None:
    #     params["comments"] = True

    return params


def process_preprocess_steps(params: dict):
    """ """
    input = params["metadata"]["source"]
    if input[-3:].lower() == "txt":
        params["metadata"]["format"] = "text/plain"
        with open(input) as f:
            params["text"] = f.read()
    elif input[-4:].lower() == "html":
        params["metadata"]["format"] = "text/html"
        with open(input) as f:
            doc = lxml.html.document_fromstring(f.read())
            params["text"] = doc.text_content()
    elif input[-3:].lower() == "pdf":
        params["metadata"]["format"] = "application/pdf"
        convert_pdf(input, format="xml", params=params)
        params["text"] = convert_pdf(input, format="text", params=params)

    text = params["text"].rstrip()
    if params["replace_hidden_characters"]:
        text_to_use = text.translate(hidden_table)
    else:
        text_to_use = text

    # if len(text) != len(text_to_use):
    #     logging.error("len text != len text.translate")

    params["text"] = text_to_use


def process_linguistic_steps(params: dict):
    """ """

    engine_name = params["engine_name"]
    nlp = params["nlp"]
    language = params["metadata"]["language"]
    if engine_name.lower() == "stanza":
        params["engine"] = stanzaProcessor(nlp, language)
        # params['default_tokenizer'] = params['engine'].tokenizer
    elif engine_name.lower() == "spacy":
        params["engine"] = spacyProcessor(nlp, language)
        # params['default_tokenizer'] = params['engine'].tokenizer
    else:
        logging.error("unknown engine")
        return None

    start_time = datetime.now()
    params["doc"] = params["engine"].nlp(params["text"])
    end_time = datetime.now()

    params["lp"] = ProcessorElement(
        name=params["engine"].model_name,
        version=params["engine"].model_version,
        timestamp=None,
        beginTimestamp=start_time,
        endTimestamp=end_time,
        hostname=None,
    )

    if "pdftoxml" in params.keys():
        add_formats_layer(params)

    process_linguistic_layers(params)


def convert_pdf(path, format="text", codec="utf-8", password="", params=None):

    start_time = datetime.now()

    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    laparams = LAParams()
    if format == "text":
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == "html":
        device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    elif format == "xml":
        device = XMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    else:
        raise ValueError("provide format, either text, html or xml!")
    fp = open(path, "rb")
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos = set()
    pages = 0
    for page in PDFPage.get_pages(
        fp,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=False,
    ):
        interpreter.process_page(page)
        pages += 1

    fp.close()
    device.close()

    text = retstr.getvalue().decode()
    retstr.close()

    end_time = datetime.now()
    params["pages"] = pages

    pp = ProcessorElement(
        name="pdfminer-pdf2" + format,
        version=f"pdfminer_version-{pdfminer.__version__}",
        timestamp=None,
        beginTimestamp=start_time,
        endTimestamp=end_time,
        hostname=None,
    )

    # params["tree"].add_processor_element("pdfto" + format, pp)

    # params["pdfto" + format] = text

    return text


def process_linguistic_layers(params: dict):

    doc = params["doc"]
    document_id = params["metadata"]["identifier"]

    processor = params["engine_name"]
    setprefix = params["setprefix"]
    do_paragraphs = params["no_paragraphs"]

    """Convert a spacy document to a FoLiA document"""

    processor = get_processor(params)

    params["folia"] = folia.Document(
        id=document_id,
        autodeclare=True,
        processor=processor,
        debug=params.get("debug", 0),
    )

    foliadoc = params["folia"]

    node = etree.Element("metadata", attrib={"type": "dc"})
    nsmap = {"dc": "http://purl.org/dc/elements/1.1/"}
    foreign_data = etree.SubElement(node, "foreign-data", nsmap=nsmap)
    for key in params["metadata"].keys():
        item = etree.SubElement(
            foreign_data, etree.QName("{" + nsmap["dc"] + "}" + key, key)
        )
        item.text = params["metadata"][key]

    foliadoc.metadata = folia.ForeignData(doc=foliadoc, node=node)

    body = foliadoc.append(folia.Text(foliadoc, id=document_id + ".text"))

    newparagraph = True
    if do_paragraphs and newparagraph:
        paragraph = body.append(folia.Paragraph)
        anchor = paragraph
    else:
        anchor = body

    for sentence in params["engine"].document_sentences(doc):
        anchor = process_sentence(sentence, anchor, None, params)

    if do_paragraphs:  # ensure last paragraph isn't empty
        try:
            anchor.text()
        except folia.NoSuchText:
            body.remove(anchor)

    params["folia"] = foliadoc


def get_processor(params: dict):

    """Get FoLiA processors given the provided spacy model (for provenance)"""

    model = params["engine"]
    processor = folia.Processor.create(name="nafigator", version=__version__)

    for p in params["engine"].nlp.processors.keys():
        subprocessor = folia.Processor(name=p, version=params["engine"].model_version)
        processor.append(subprocessor)

    if model is not None and hasattr(model, "meta"):
        datasource = folia.Processor(
            name=model.meta["lang"] + "_" + model.meta["name"],
            type=folia.ProcessorType.DATASOURCE,
            version=model.meta["version"],
        )
        subprocessor.append(datasource)
        for key, value in model.meta.items():
            if key not in ("name", "lang", "version"):  # we already covered those
                if isinstance(value, str):
                    datasource.metadata[key] = value
                elif isinstance(value, (list, tuple)) and all(
                    isinstance(x, str) for x in value
                ):
                    datasource.metadata[key] = ",".join(value)
        setprefix += (
            "-" + model.meta["lang"] + "_" + model.meta["name"].replace(" ", "_")
        )
    # else:
    #     if spacydoc is not None and spacydoc.lang_:
    #         setprefix += "-" + spacydoc.lang_
    #     else:
    #         setprefix += "-unknown"
    return processor


def process_token(word, foliaword, params):
    """ """
    setprefix = params["setprefix"]
    engine = params["engine"]
    if engine.token_tag(word):  # word.tag_:
        foliaword.append(
            folia.PosAnnotation,
            set=setprefix + "-pos",
            cls=params["engine"].token_tag(word),
        )
    if engine.token_pos(word):
        foliaword.append(
            folia.PosAnnotation,
            set="https://raw.githubusercontent.com/proycon/folia/master/setdefinitions/universal-pos.foliaset.ttl",
            cls=engine.token_pos(word),
        )
    if engine.token_lemma(word):
        foliaword.append(
            folia.LemmaAnnotation,
            set=setprefix + "-lemma",
            cls=engine.token_lemma(word),
        )


def process_sentence(sentence, anchor, foliasentence, params: dict):
    """ """
    foliadoc = params["folia"]
    setprefix = params["setprefix"]
    do_paragraphs = params["no_paragraphs"]

    pretokenized = False

    if (foliasentence is None) and (anchor is not None):
        foliasentence = anchor.append(folia.Sentence)

    body = foliadoc.data[0]
    assert isinstance(body, (folia.Text, folia.Speech))

    tokens = params["engine"].sentence_tokens(sentence)

    if not pretokenized:
        foliawords = (
            []
        )  # will map 1-1 to the spacy tokens, may contain None elements for linebreaks
        foliaword = None
        # tokens = list(sentence)
        for i, word in enumerate(tokens):
            text = word.text
            if text == "\n":
                if foliaword is not None and i < len(tokens) - 1:
                    foliasentence.append(folia.Linebreak)
                    foliaword.space = True  # in case a linebreak occurs in a sentence
                elif do_paragraphs:
                    anchor = body.append(folia.Paragraph)
                else:
                    body.append(folia.Whitespace)
                foliawords.append(None)
            elif text.strip():
                # space = word.whitespace_ != ""
                space = False
                foliaword = foliasentence.append(folia.Word, text.strip(), space=space)
                process_token(word, foliaword, params)
                foliawords.append(foliaword)
    else:
        foliawords = list(foliasentence.words())
        # tokens = list(sentence)
        for word, foliaword in zip(tokens, foliawords):
            process_token(word, foliaword, setprefix)

    # if isinstance(sentence, spacy.tokens.doc.Doc):
    #     start = 0
    #     end = len(sentence)
    # else:
    #     start = sentence.start
    #     end = sentence.end

    # end = len(sentence)

    for entity in params["engine"].sentence_entities(sentence):
        ent_start = (
            params["engine"].token_index(params["engine"].entity_token_start(entity))
            - 1
        )
        ent_end = (
            params["engine"].token_index(params["engine"].entity_token_end(entity)) - 1
        )
        spanwords = [w for w in foliawords[ent_start : ent_end + 1] if w is not None]
        foliaentity = foliasentence.add(
            folia.Entity,
            *spanwords,
            set=setprefix + "-namedentitities",
            cls=params["engine"].entity_type(entity),
        )

    # for chunk in sentence.noun_chunks:
    #     spanwords = [ w for w in foliawords[chunk.start-start:chunk.end-end] if w is not None ]
    #     foliaentity = foliasentence.add(folia.Chunk, *spanwords, set=setprefix+"-nounchunks", cls=chunk.label_)

    for i, word in enumerate(tokens):
        depword = foliawords[i]
        deprel = params["engine"].token_dependency(word)
        if deprel != "root":
            word_head_id = (
                params["engine"].token_index(
                    params["engine"].token_head(sentence, word)
                )
                - 1
            )
            headword = foliawords[word_head_id]
            dependency = foliasentence.add(
                folia.Dependency,
                set=setprefix + "-dependencies",
                cls=params["engine"].token_dependency(word),
            )
            dependency.append(folia.DependencyHead, headword)
            dependency.append(folia.DependencyDependent, depword)

    return anchor


def convert_folia(
    foliadoc: folia.Document, model, default_tokenizer=None, **kwargs
) -> folia.Document:
    """Process an existing folia document with spacy"""
    if default_tokenizer is not None:
        model.tokenizer = default_tokenizer
    if not foliadoc.processor or foliadoc.processor.name != "spacy2folia":
        foliadoc.processor = get_processor(
            model, None, kwargs.get("setprefix", SETPREFIX)
        )
    pretokenized = False
    if foliadoc.declared(folia.Sentence):
        print(
            "Sentence annotation is present in "
            + foliadoc.id
            + ", annotating on the sentence level",
            file=sys.stderr,
        )
        if foliadoc.declared(folia.Word):
            print(
                "Token annotation is already present in "
                + foliadoc.id
                + ", disabling SpaCy's tokeniser and working on the existing tokens!",
                file=sys.stderr,
            )
            model.tokenizer = WhitespaceTokenizer(model.vocab)
            pretokenized = True

        for sentence in foliadoc.sentences():
            text = (
                sentence.text(retaintokenisation=pretokenized)
                .replace("\n", " ")
                .strip()
            )
            doc = model(text)
            process_sentence(
                foliadoc,
                doc,
                None,
                sentence,
                kwargs.get("setprefix", SETPREFIX),
                do_paragraphs=False,
                pretokenized=pretokenized,
            )

    elif foliadoc.declared(folia.Paragraph):
        print(
            "Paragraph annotation is present in "
            + foliadoc.id
            + ", annotating on the paragraph level",
            file=sys.stderr,
        )

        for paragraph in foliadoc.paragraphs():
            text = paragraph.text().replace("\n", " ").strip()
            doc = model(text)
            for sentence in doc.sents:
                process_sentence(
                    foliadoc,
                    sentence,
                    paragraph,
                    None,
                    kwargs.get("setprefix", SETPREFIX),
                    do_paragraphs=False,
                    pretokenized=pretokenized,
                )

    else:
        print(
            "Nothing to do for document "
            + foliadoc.id
            + "? Couldn't find any existing structural basis to annotate.",
            file=sys.stderr,
        )

    return foliadoc


class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(" ")
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return spacy.tokens.doc.Doc(self.vocab, words=words, spaces=spaces)


if __name__ == "__main__":
    sys.exit(nafigator())
