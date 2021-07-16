# coding: utf-8

"""Main module."""

import sys
import click
import logging
import os
import re
from datetime import datetime
from socket import getfqdn

from .nafdocument import NafDocument
from .linguisticprocessor import stanzaProcessor
from .linguisticprocessor import spacyProcessor
from .preprocessprocessor import convert_pdf
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
from .const import udpos2olia
from .const import hidden_table
from .utils import normalize_token_orth
from .utils import remove_illegal_chars

FORMATS_LAYER_TAG = "formats"


@click.command()
@click.option(
    "--input", default="data/example.pdf", prompt="input file", help="The input file"
)
@click.option(
    "--output", default="data/example.naf.xml", prompt="output file", help="The output file"
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
    log_file: str = os.path.splitext(input)[0] + ".log"
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

    params = create_params(
        input=input,
        engine=engine,
        language=language,
        naf_version=naf_version,
        dtd_validation=dtd_validation,
        params=params,
        nlp=nlp,
    )

    params["tree"] = NafDocument()
    params["tree"].generate(params)

    process_preprocess_steps(params)

    process_linguistic_steps(params)

    evaluate_naf(params)

    return params["tree"]


def create_params(
    input: str = None,
    engine: str = None,
    language: str = None,
    naf_version: str = None,
    dtd_validation: bool = False,
    params: dict = {},
    nlp=None,
):
    """ """
    params["naf_version"] = naf_version
    params["dtd_validation"] = bool(dtd_validation)
    params["language"] = language
    params["engine_name"] = engine
    params["nlp"] = nlp

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
    elif os.path.splitext(input)[1].lower() == ".html":
        params["fileDesc"]["filetype"] = "text/html"
        params["public"]["format"] = "text/html"
    elif os.path.splitext(input)[1].lower() == ".pdf":
        params["fileDesc"]["filetype"] = "application/pdf"
        params["public"]["format"] = "application/pdf"

    # set default linguistic parameters
    if "linguistic_layers" not in params.keys():
        params["linguistic_layers"] = [
            "text",
            "terms",
            "entities",
            "deps",
            "raw",
            "multiwords",
        ]
    if params.get("cdata", None) is None:
        params["cdata"] = True
    if params.get("map_udpos2olia", None) is None:
        params["map_udpos2olia"] = False
    if params.get("layer_to_attributes_to_ignore", None) is None:
        params["layer_to_attributes_to_ignore"] = {"terms": {}}
    if params.get("replace_hidden_characters", None) is None:
        params["replace_hidden_characters"] = True
    if params.get("comments", None) is None:
        params["comments"] = True

    return params


def evaluate_naf(params: dict):
    """ """
    # verify alignment between raw layer and document text
    doc_text = params["engine"].document_text(params["doc"])
    raw = params["tree"].raw
    if len(raw) != len(doc_text):
        logging.error(
            "raw length ("
            + str(len(raw))
            + ") != doc length ("
            + str(len(doc_text))
            + ")"
        )
    # verify alignment between raw layer and text
    text_to_use = params["text"]
    if len(raw) != len(text_to_use):
        logging.error(
            "raw length ("
            + str(len(raw))
            + ") != text to use ("
            + str(len(text_to_use))
            + ")"
        )
    # verify alignment between raw layer and text layer
    for wf in params["tree"].text:
        start = int(wf.get("offset"))
        end = start + int(wf.get("length"))
        token = raw[start:end]
        if wf.get("text", None) != token:
            logging.error(
                "mismatch in alignment of wf element ["
                + str(wf.text)
                + "] ("
                + str(wf.get("id"))
                + ") with raw layer text ["
                + str(token)
                + "] (expected length "
                + str(wf.get("length"))
                + ")"
            )

    # validate naf tree
    if params["dtd_validation"]:
        params["tree"].validate()


def norm_spaces(s):
    """Normalize spaces, splits on all kinds of whitespace and rejoins"""
    return s
    # return " ".join((x for x in re.split(r"\s+", s) if x))


def process_preprocess_steps(params: dict):
    """ """
    input = params["fileDesc"]["filename"]
    if input[-3:].lower() == "txt":
        with open(input) as f:
            params["text"] = f.read()
    elif input[-4:].lower() == "html":
        with open(input) as f:
            doc = lxml.html.document_fromstring(f.read())
            params["text"] = doc.text_content()
    elif input[-3:].lower() == "pdf":
        convert_pdf(input, format="xml", params=params)
        convert_pdf(input, format="text", params=params)
        params["text"] = params["pdftotext"]

    text = params["text"].rstrip()
    if params["replace_hidden_characters"]:
        text_to_use = norm_spaces(text.translate(hidden_table))
    else:
        text_to_use = norm_space(text)

    # if len(text) != len(text_to_use):
    #     logging.error("len text != len text.translate")

    params["text"] = text_to_use


def process_linguistic_steps(params: dict):
    """ """
    engine_name = params["engine_name"]
    nlp = params["nlp"]
    language = params["language"]
    if engine_name.lower() == "stanza":
        params["engine"] = stanzaProcessor(nlp, language)
    elif engine_name.lower() == "spacy":
        params["engine"] = spacyProcessor(nlp, language)
    else:
        logging.error("unknown engine")
        return None

    params["beginTimestamp"] = datetime.now()
    params["doc"] = params["engine"].nlp(params["text"])
    params["endTimestamp"] = datetime.now()

    if "pdftoxml" in params.keys():
        add_formats_layer(params)

    process_linguistic_layers(params)


def process_linguistic_layers(params: dict):

    layers = params["linguistic_layers"]

    if "entities" in layers:
        add_entities_layer(params)

    if "text" in layers:
        add_text_layer(params)

    if "terms" in layers:
        add_terms_layer(params)

    if "deps" in layers:
        add_deps_layer(params)

    if "multiwords" in layers:
        add_multiwords_layer(params)

    if "chunks" in layers:
        add_chunks_layer(params)

    if "raw" in layers:
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
        comment = remove_illegal_chars(chunk.orth_.replace("\n", " "))
        yield ChunkElement(
            id="c" + str(i),
            head="t" + str(chunk.root.i),
            phrase=phrase,
            case=None,
            span=["t" + str(tok.i) for tok in chunk],
            comment=comment,
        )


def prepare_comment_text(text: str):
    """ """
    text = text.replace("--", "DOUBLEDASH")
    if text.endswith("-"):
        text = text[:-1] + "SINGLEDASH"
    return text


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
        from_orth = engine.token_orth(engine.token_head(sentence, token))
        to_orth = engine.token_orth(token)

        comment = rfunc + "(" + from_orth + "," + to_orth + ")"
        comment = prepare_comment_text(comment)

        dep_data = DependencyRelation(
            from_term=from_term,
            to_term=to_term,
            rfunc=rfunc,
            case=None,
            comment=comment,
        )
        deps.append(dep_data)
        token = engine.token_head(sentence, token)
    return deps


def add_entities_layer(params: dict):
    """ """
    lp = ProcessorElement(
        name="entities",
        version=params["engine"].model_version,
        model=params["engine"].processor("entities").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("entities", lp)

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
                    status=None,
                    source=None,
                    span=current_entity,
                    ext_refs=list(),
                    comment=current_entity_orth,
                )

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
                    next_entity = Entity(start=None, end=None, type=None)

        if engine.token_reset() is False:
            current_token = token_number + 1
            total_tokens = 0
        else:
            current_token = 1
            total_tokens += token_number

    return None


def add_text_layer(params: dict):
    """ """
    lp = ProcessorElement(
        name="text",
        version=params["engine"].model_version,
        model=params["engine"].processor("text").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("text", lp)

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

            wf_id = "w" + str(token_number + total_tokens)
            wf_data = WordformElement(
                id=wf_id,
                sent=str(sentence_number),
                para=None,
                page=str(current_page),
                offset=str(engine.token_offset(token)),
                length=str(len(token.text)),
                xpath=None,
                text=token.text,
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
    lp = ProcessorElement(
        name="terms",
        version=params["engine"].model_version,
        model=params["engine"].processor("terms").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("terms", lp)

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
            token_pos = engine.token_pos(token)
            # :param bool map_udpos2naf_pos: if True, we use "udpos2nafpos_info"
            # to map the Universal Dependencies pos (https://universaldependencies.org/u/pos/)
            # to the NAF pos tagset
            if params["map_udpos2olia"]:
                if token_pos in udpos2olia.keys():
                    pos_type = udpos2olia[token_pos]["class"]
                    token_pos = udpos2olia[token_pos]["olia"]
                else:
                    logging.info("unknown token pos: " + str(token_pos))
                    pos_type = "open"
                    token_pos = "unknown"
            else:
                pos_type = "open"

            term_data = TermElement(
                id=tid,
                type=pos_type,
                lemma=remove_illegal_chars(engine.token_lemma(token)),
                pos=token_pos,
                morphofeat=engine.token_tag(token),
                netype=None,
                case=None,
                head=None,
                component_of=None,
                compound_type=None,
                span=current_term,
                ext_refs=list(),
                comment=current_term_orth,
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
    lp = ProcessorElement(
        name="deps",
        version=params["engine"].model_version,
        model=params["engine"].processor("deps").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("deps", lp)

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

    return None


def get_next_mw_id(params):
    """ """
    layer = params["tree"].find("multiwords")
    if layer is None:
        layer = etree.SubElement(params["tree"].getroot(), "multiwords")
    mw_ids = [int(mw_el.get("id")[2:]) for mw_el in layer.xpath("mw")]
    if mw_ids:
        next_mw_id = max(mw_ids) + 1
    else:
        next_mw_id = 1
    return f"mw{next_mw_id}"


def create_separable_verb_lemma(verb, particle, language):
    """ """
    if language == "nl":
        lemma = particle + verb
    if language == "en":
        lemma = f"{verb}_{particle}"
    return lemma


def add_multiwords_layer(params: dict):
    """ """
    lp = ProcessorElement(
        name="multiwords",
        version=params["engine"].model_version,
        model=params["engine"].processor("multiwords").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("multiwords", lp)

    engine = params["engine"]

    if params["naf_version"] == "v3":
        logging.info("add_multi_words function only applies to naf version 4")

    supported_languages = {"nl", "en"}
    if params["language"] not in supported_languages:
        logging.info(
            f"add_multi_words function only implemented for {supported_languages}, not for supplied {language}"
        )

    tid_to_term = {
        term.get("id"): term for term in params["tree"].findall("terms/term")
    }

    for dep in params["tree"].deps:

        if dep.get("rfunc") == "compound:prt":

            next_mw_id = get_next_mw_id(params)

            idverb = dep.get("from_term")
            idparticle = dep.get("to_term")

            verb_term_el = tid_to_term[idverb]
            verb = verb_term_el.attrib.get("lemma")
            verb_term_el.set("component_of", next_mw_id)

            particle_term_el = tid_to_term[idparticle]
            particle = particle_term_el.attrib.get("lemma")
            particle_term_el.set("component_of", next_mw_id)

            separable_verb_lemma = create_separable_verb_lemma(
                verb, particle, params["language"]
            )
            multiword_data = MultiwordElement(
                id=next_mw_id,
                lemma=separable_verb_lemma,
                pos="VERB",
                morphofeat=None,
                case=None,
                status=None,
                type="phrasal",
                components=[],
            )

            components = [
                (f"{next_mw_id}.c1", idverb),
                (f"{next_mw_id}.c2", idparticle),
            ]

            for c_id, t_id in components:
                component_data = ComponentElement(
                    id=c_id,
                    type=None,
                    lemma=None,
                    pos=None,
                    morphofeat=None,
                    netype=None,
                    case=None,
                    head=None,
                    span=[t_id],
                )
                multiword_data.components.append(component_data)

            params["tree"].add_multiword_element(multiword_data)

            # component = etree.SubElement(
            #     mw_element, "component", attrib={"id": c_id}
            # )
            # span = etree.SubElement(component, "span")
            # etree.SubElement(span, "target", attrib={"id": t_id})

    # params["tree"].add_multi_words(params["naf_version"], params["language"])


def add_raw_layer(params: dict):
    """ """
    lp = ProcessorElement(
        name="raw",
        version=params["engine"].model_version,
        model=params["engine"].processor("raw").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("raw", lp)

    wordforms = params["tree"].text

    delta = int(wordforms[0]["offset"])
    tokens = [" " * delta + wordforms[0]["text"]]

    for prev_wf, cur_wf in zip(wordforms[:-1], wordforms[1:]):
        prev_start = int(prev_wf["offset"])
        prev_end = prev_start + int(prev_wf["length"])
        cur_start = int(cur_wf["offset"])
        delta = cur_start - prev_end
        # no chars between two token (for example with a dot .)
        if delta == 0:
            leading_chars = ""
        elif delta >= 1:
            # 1 or more characters between tokens -> n spaces added
            leading_chars = " " * delta
        elif delta < 0:
            logging.warning(
                "please check the offsets of "
                + str(prev_wf["text"])
                + " and "
                + str(cur_wf["text"])
                + " (delta of "
                + str(delta)
                + ")"
            )
        tokens.append(leading_chars + cur_wf["text"])

    if params["cdata"]:
        raw_text = etree.CDATA("".join(tokens))
    else:
        raw_text = "".join(tokens)

    raw_data = RawElement(text=raw_text)

    params["tree"].add_raw_text_element(raw_data)


def add_chunks_layer(params: dict):
    """ """
    lp = ProcessorElement(
        name="chunks",
        version=params["engine"].model_version,
        model=params["engine"].processor("chunks").get('model', ''),
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("chunks", lp)

    for chunk_data in chunk_tuples_for_doc(params["doc"], params):
        params["tree"].add_chunk_element(chunk_data, params["comments"])


def add_formats_layer(params: dict):
    """ """
    lp = ProcessorElement(
        name="formats",
        version=params["engine"].model_version,
        model=None,
        timestamp=None,
        beginTimestamp=params["beginTimestamp"],
        endTimestamp=params["endTimestamp"],
        hostname=getfqdn(),
    )

    params["tree"].add_processor_element("formats", lp)

    params["tree"].add_formats_element(params["pdftoxml"])


if __name__ == "__main__":
    sys.exit(nafigator())
