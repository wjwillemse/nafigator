# coding: utf-8

"""Main module."""

from datetime import datetime
import sys
import click
import logging
import os

from .linguisticprocessor import stanzaProcessor
from .linguisticprocessor import spacyProcessor
from .preprocessprocessor import convert_pdf
from .nafdocument import NafDocument

from .const import ProcessorElement
from .const import Entity
from .const import WordformElement
from .const import TermElement
from .const import EntityElement
from .const import DependencyRelation
from .const import ChunkElement
from .const import udpos2nafpos_info
from .const import hidden_table
from .utils import normalize_token_orth
from .utils import remove_illegal_chars

FORMATS_LAYER_TAG = "formats"


@click.command()
@click.option(
    "--input", default="data/example.pdf", prompt="input file", help="The input file"
)
@click.option(
    "--output", default="data/example.naf", prompt="output file", help="The output file"
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
@click.option(
    "--naf_version",
    default="v3.1",
    prompt="naf version",
    help="NAF version to convert to",
)
@click.option(
    "--dtd_validation",
    default=False,
    prompt="dtd validation",
    help="Validate the NAF dtd",
)
def nafigator(
    input: str,
    output: str,
    engine: str,
    language: str,
    naf_version: str,
    dtd_validation: bool,
):
    """ """
    log_file: str = "".join(output.split(".")[0:-1]) + ".log"
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode="w")
    tree = generate_naf(
        input=input,
        engine=engine,
        language=language,
        naf_version=naf_version,
        dtd_validation=dtd_validation,
    )
    tree.write(output)


def generate_naf(
    input: str = None,
    engine: str = None,
    language: str = None,
    naf_version: str = None,
    dtd_validation: bool = False,
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
    if naf_version is None:
        logging.error("no naf version specified")
        return None

    params["naf_version"] = naf_version
    params["dtd_validation"] = bool(dtd_validation)
    params["language"] = language
    params["engine_name"] = engine
    params["nlp_object"] = nlp

    if "fileDesc" not in params.keys():
        params["fileDesc"] = dict()
    params["fileDesc"]["creationtime"] = datetime.now()
    params["fileDesc"]["filename"] = input

    if "public" not in params.keys():
        params["public"] = dict()
    params["public"]["uri"] = input
    if os.path.splitext(input)[1].lower() == ".txt":
        params["fileDesc"]["filetype"] = "text/plain"
        params["public"]["format"] = "text/plain"
    elif os.path.splitext(input)[1] == ".pdf":
        params["fileDesc"]["filetype"] = "application/pdf"
        params["public"]["format"] = "application/pdf"

    # set default linguistic parameters
    if "linguistic_layers" not in params.keys():
        params["linguistic_layers"] = ["text", "terms", "entities", "deps", "raw"]
    if params.get("cdata", None) is None:
        params["cdata"] = True
    if params.get("map_udpos2naf_pos", None) is None:
        params["map_udpos2naf_pos"] = False
    if params.get("layer_to_attributes_to_ignore", None) is None:
        params["layer_to_attributes_to_ignore"] = {"terms": {}}
    if params.get("replace_hidden_characters", None) is None:
        params["replace_hidden_characters"] = True
    if params.get("add_mws", None) is None:
        params["add_mws"] = False
    if params.get("comments", None) is None:
        params["comments"] = True
    if params["add_mws"]:
        linguistic_layers.append("multiwords")
    
    params["tree"] = NafDocument()
    params["tree"].generate(params)

    process_preprocess_steps(params)

    process_linguistic_steps(params)

    # check it lengths match
    doc_text = params["engine"].document_text(params["doc"])
    raw = params["tree"].raw
    text_to_use = params["text"]
    if raw.strip() != doc_text.strip():
        logging.error("raw length ("+str(len(raw))+") != doc length ("+str(len(doc_text))+")")
    if raw.strip() != text_to_use.strip():
        logging.error("raw length ("+str(len(raw))+") != text to use ("+str(len(text_to_use))+")")

    # validate naf tree
    if params["dtd_validation"]:
        params["tree"].validate()

    return params["tree"]


def process_preprocess_steps(params: dict):
    """ """
    input = params["fileDesc"]["filename"]

    if input[-3:].lower() == "txt":
        with open(input) as f:
            params["text"] = f.read()
    elif input[-3:].lower() == "pdf":
        convert_pdf(input, format="xml", params=params)
        convert_pdf(input, format="text", params=params)

    if params.get("pages", None) is not None:
        params["fileDesc"]["pages"] = params["pages"]

    text = params["pdftotext"]
    if params["replace_hidden_characters"]:
        text_to_use = text.translate(hidden_table)
    else:
        text_to_use = text
    if len(text) != len(text_to_use):
        logging.info("len text != len text.translate")
    params["text"] = text_to_use


def process_linguistic_steps(params: dict):
    """ """
    engine_name = params["engine_name"]
    nlp = params["nlp_object"]
    language = params["language"]
    if engine_name.lower() == "stanza":
        params["engine"] = stanzaProcessor(nlp, language)
    elif engine_name.lower() == "spacy":
        params["engine"] = spacyProcessor(nlp, language)
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

    layers = params["linguistic_layers"]

    if params.get("pdftoxml", None) is not None:
        add_formats_layer(params)

    for layer in layers:
        add_layer(layer, params)


def add_layer(layer: str, params: dict):

    if layer == "entities":
        add_entities_layer(params)

    if layer == "text":
        add_text_layer(params)

    if layer == "terms":
        add_terms_layer(params)

    if layer == "deps":
        add_deps_layer(params)

    if layer == "chunks":
        add_chunks_layer(params)

    if layer == "raw":
        add_raw_layer(params)


def entities_generator(doc, params: dict):
    """ """
    engine = params["engine"]
    for ent in engine.document_entities(doc):
        yield Entity(
            start=engine.entity_span_start(ent),
            end=engine.entity_span_end(ent),
            type=engine.entity_type(ent),
        )


def chunks_for_doc(doc, params: dict):
    """ """
    for chunk in params["engine"].document_noun_chunks(doc):
        if chunk.root.head.pos_ == "ADP":
            span = doc[chunk.start - 1 : chunk.end]
            yield (span, "PP")
        yield (chunk, "NP")


def chunk_tuples_for_doc(doc, params: dict):
    """ """
    for i, (chunk, phrase) in enumerate(chunks_for_doc(doc, params)):
        chunk_text = remove_illegal_chars(chunk.orth_.replace("\n", " "))
        yield ChunkElement(
            cid="c" + str(i),
            head="t" + str(chunk.root.i),
            phrase=phrase,
            text=chunk_text,
            targets=["t" + str(tok.i) for tok in chunk],
        )


def dependencies_to_add(sentence, token, total_tokens: int, params: dict):
    """ """
    engine = params["engine"]
    deps = list()
    cor = engine.offset_token_index()

    while engine.token_head_index(sentence, token) != engine.token_index(token):
        from_term = "t" + str(
            engine.token_head_index(sentence, token) + total_tokens + cor
        )
        to_term = "t" + str(engine.token_index(token) + total_tokens + cor)
        rfunc = engine.token_dependency(token)
        from_orth = engine.token_orth(token)
        to_orth = engine.token_orth(engine.token_head(sentence, token))
        dep_data = DependencyRelation(
            from_term=from_term,
            to_term=to_term,
            rfunc=rfunc,
            from_orth=from_orth,
            to_orth=to_orth,
        )
        deps.append(dep_data)
        token = engine.token_head(sentence, token)
    return deps


def add_entities_layer(params: dict):
    """ """
    params["tree"].add_processor_element("entities", params["lp"])

    doc = params["doc"]
    engine = params["engine"]

    current_entity = list()  # Use a list for multiword entities.
    current_entity_orth = list()  # id.

    current_token: int = 1  # Keep track of the token number.
    term_number: int = 1  # Keep track of the term number.
    entity_number: int = 1  # Keep track of the entity number.
    total_tokens: int = 0

    parsing_entity: bool = False

    for sentence_number, sentence in enumerate(engine.document_sentences(doc), start=1):

        entity_gen = entities_generator(sentence, params)
        try:
            next_entity = next(entity_gen)
        except StopIteration:
            next_entity = Entity(start=None, end=None, type=None)

        for token_number, token in enumerate(
            engine.sentence_tokens(sentence), start=current_token
        ):
            # Do we need a state change?

            if token_number == next_entity.start:
                parsing_entity = True

            tid = "t" + str(term_number)
            if parsing_entity:
                current_entity.append(tid)
                current_entity_orth.append(
                    normalize_token_orth(engine.token_orth(token))
                )

            # Move to the next term
            term_number += 1

            if parsing_entity and token_number == next_entity.end:
                # Create new entity ID.
                entity_id = "e" + str(entity_number)
                # Create Entity data:
                entity_data = EntityElement(
                    id=entity_id,
                    type=next_entity.type,
                    targets=current_entity,
                    text=current_entity_orth,
                    ext_refs=list(),
                )  # entity linking currently not part of spaCy

                params["tree"].add_entity_element(
                    entity_data, params["naf_version"], params["language"]
                )

                entity_number += 1
                current_entity = list()
                current_entity_orth = list()
                # Move to the next entity
                parsing_entity = False
                try:
                    next_entity = next(entity_gen)
                except StopIteration:
                    # No more entities...
                    next_entity = Entity(start=None, end=None, type=None)

        # At the end of the sentence, add all the dependencies to the XML structure.
        if engine.token_reset() is False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None


def add_text_layer(params: dict):
    """ """
    params["tree"].add_processor_element("text", params["lp"])

    root = params["tree"].getroot()

    pages_offset = None
    formats = root.find(FORMATS_LAYER_TAG)
    if formats is not None:
        pages_offset = [int(page.get("offset")) for page in formats]

    doc = params["doc"]
    engine = params["engine"]

    current_token: int = 1
    total_tokens: int = 0
    current_page: int = 0

    for sentence_number, sentence in enumerate(engine.document_sentences(doc), start=1):

        for token_number, token in enumerate(
            engine.sentence_tokens(sentence), start=current_token
        ):

            if (pages_offset is not None) and (current_page < len(pages_offset)):
                if engine.token_offset(token) >= pages_offset[current_page]:
                    current_page += 1

            wid = "w" + str(token_number + total_tokens)
            wf_data = WordformElement(
                page=str(current_page),
                sent=str(sentence_number),
                id=wid,
                length=str(len(token.text)),
                wordform=token.text,
                offset=str(engine.token_offset(token)),
            )

            params["tree"].add_wf_element(wf_data, params["cdata"])

        if engine.token_reset() is False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None


def add_terms_layer(params: dict):
    """ """
    params["tree"].add_processor_element("terms", params["lp"])

    doc = params["doc"]
    engine = params["engine"]

    current_term = list()  # Use a list for multiword expressions.
    current_term_orth = list()  # id.

    current_token: int = 1  # Keep track of the token number.
    term_number: int = 1  # Keep track of the term number.
    total_tokens: int = 0

    for sentence_number, sentence in enumerate(engine.document_sentences(doc), start=1):

        for token_number, token in enumerate(
            engine.sentence_tokens(sentence), start=current_token
        ):

            wid = "w" + str(token_number + total_tokens)
            tid = "t" + str(term_number)

            current_term.append(wid)
            current_term_orth.append(normalize_token_orth(engine.token_orth(token)))

            # Create TermElement data:
            spacy_pos = engine.token_pos(token)
            # :param bool map_udpos2naf_pos: if True, we use "udpos2nafpos_info"
            # to map the Universal Dependencies pos (https://universaldependencies.org/u/pos/)
            # to the NAF pos tagset
            if params["map_udpos2naf_pos"]:
                if spacy_pos in udpos2nafpos_info:
                    pos = udpos2nafpos_info[spacy_pos]["naf_pos"]
                    pos_type = udpos2nafpos_info[spacy_pos]["class"]
                else:
                    pos = "O"
                    pos_type = "open"
            else:
                pos = spacy_pos
                pos_type = "open"

            term_data = TermElement(
                id=tid,
                lemma=remove_illegal_chars(engine.token_lemma(token)),
                pos=pos,
                type=pos_type,
                morphofeat=engine.token_tag(token),
                targets=current_term,
                text=current_term_orth,
            )

            params["tree"].add_term_element(
                term_data, params["layer_to_attributes_to_ignore"], params["comments"]
            )

            # Move to the next term
            term_number += 1
            current_term = list()
            current_term_orth = list()

        # At the end of the sentence,
        # add all the dependencies to the XML structure.
        if engine.token_reset() is False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None


def add_deps_layer(params: dict):
    """ """
    params["tree"].add_processor_element("deps", params["lp"])

    engine = params["engine"]

    current_token: int = 1
    total_tokens: int = 0

    for sent in engine.document_sentences(params["doc"]):

        dependencies_for_sentence = list()

        for token_number, token in enumerate(
            engine.sentence_tokens(sent), start=current_token
        ):
            for dep_data in dependencies_to_add(sent, token, total_tokens, params):
                if dep_data not in dependencies_for_sentence:
                    dependencies_for_sentence.append(dep_data)

        for dep_data in dependencies_for_sentence:
            params["tree"].add_dependency_element(dep_data, params["comments"])

        if engine.token_reset() is False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

        if params["add_mws"]:
            params["tree"].add_multi_words(params["naf_version"], params["language"])

    return None


def add_raw_layer(params: dict):
    """ """
    params["tree"].add_processor_element("raw", params["lp"])

    params["tree"].add_raw_text_element(params["cdata"])


def add_chunks_layer(params: dict):
    """ """
    params["tree"].add_processor_element("chunks", params["lp"])

    for chunk_data in chunk_tuples_for_doc(params["doc"], params):
        params["tree"].add_chunk_element(chunk_data, params["comments"])


def add_formats_layer(params: dict):
    """ """
    params["tree"].add_processor_element("formats", params["lp"])

    params["tree"].add_formats_element(params["pdftoxml"])


if __name__ == "__main__":
    sys.exit(nafigator())
