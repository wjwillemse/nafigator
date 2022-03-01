# -*- coding: utf-8 -*-

"""Convert2rdf module.

This module contains RDF conversion functions for nafigator package

"""

import sys
import click
from io import StringIO, BytesIO

from .nafdocument import NafDocument
from lxml import etree
import rdflib
import logging
import os

@click.command()
@click.option(
    "--input", default="data/example.naf", prompt="input file", help="The input file"
)
@click.option(
    "--prefix", default="_", prompt="triple prefix", help="the prefix of the triples"
)
@click.option(
    "--format", default="turtle", prompt="output format (turtle/xml/json-ld/ntriples/n3/trig)", help="The format of the output"
)
def convert2rdf_cli(input: str, prefix: str, format: str) -> None:
    
    doc = NafDocument().open(input)

    graph = parse2rdf(doc = doc, params = {"handlerPrefix": prefix})

    if graph is not None:
        output, _ = os.path.splitext(input)
        if format == "turtle":
            extension = ".ttl"
        if format == "xml":
            extensopm = ".rdf.xml"
        fh = open(output+extension, "w", encoding="utf-8")
        fh.write(g.serialize(format=format))
        fh.close()

    return None


def parse2graph(doc: NafDocument, params: dict = {}) -> None:
    """Main function to convert NAF to RDF

    Args:
        doc: the naf document

    Returns:

    """
    create_params(doc, params)

    processNaf(doc, params)

    return generate_graph(params)


def create_params(doc: NafDocument, params: dict = {}):

    params["namespaces"] = dict()
    params["provenanceNumber"] = 0
    params["depNumber"] = 0
    params["provenance"] = doc.header['fileDesc']['filename'].replace('\\', "\\\\")

    addNamespace("dc", "http://purl.org/dc/elements/1.1/", params)
    addNamespace("xl", "http://www.xbrl.org/2003/XLink/", params)
    addNamespace("xsd", "http://www.w3.org/2001/XMLSchema/", params)
    addNamespace("naf-base", "https://dnb.nl/naf-base/", params)
    addNamespace("naf-entity", "https://dnb.nl/naf-entity/", params)
    addNamespace("naf-fileDesc", "https://dnb.nl/naf-fileDesc/", params)
    addNamespace("naf-morphofeat", "https://dnb.nl/naf-morphofeat/", params)
    addNamespace("naf-pos", "https://dnb.nl/naf-pos/", params)
    addNamespace("naf-rfunc", "https://dnb.nl/naf-rfunc/", params)
    addNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns/", params)
    addNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema/", params)
    
    if params.get("handlerPrefix", "_") != "_":
        addNamespace(params['handlerPrefix'], "http://dnb.nl/naf-data/"+params['handlerPrefix']+"/", params)

    params["out"] = StringIO()
    params["prefix"] = printNamespaces(params)
    params["doc"] = doc

def generate_graph(params: dict = {}):

    file_content: StringIO = StringIO()
    file_content.write("# RDF triples (turtle syntax)\n\n")
    file_content.write("# NAF URI  '" + params["provenance"] + "'\n")
    file_content.write("\n")
    file_content.write(params["prefix"])
    file_content.write("\n\n")
    file_content.write(params["out"].getvalue().replace("\u2264", ""))

    content = file_content.getvalue()

    graph = rdflib.Graph()

    try:
        graph.parse(data=content, format="turtle")
    except:
        logging.error("Parsing error")
        with open("doc.log", "w", encoding="utf-8") as fh:
            fh.write(content)
        graph = None

    return graph

def isHttpUrl(url: str) -> bool:
    """Check is url is http url

    Args:
        url: url to be checked

    Returns:
        bool: True is url is http or https url

    """
    return isinstance(url, str) and (
        url.startswith("http://") or url.startswith("https://")
    )


def addNamespace(prefix: str = None, uri: str = None, params: dict = {}) -> int:
    """Add namespace to list of namespaces

    Args:
        prefix: prefix of the uri
        uri: complete uri of the prefix
        params: dict of params containing the namespaces

    Returns:
        int: 0 if success

    """
    namespaces = params["namespaces"]
    found = namespaces.get(uri, None)
    if found:
        if prefix != found:
            return -1
        del namespaces[uri]
    namespaces[uri] = prefix
    return 0


def printNamespaces(params: dict = {}) -> str:
    """Get string of list of namespaces

    Args:
        params: dict of params containing the namespaces

    Returns:
        str: string of namespaces

    """
    namespaces = params["namespaces"]
    res: str = ""
    for uri in namespaces:
        if uri[-1] != "#":
            res += "@prefix " + namespaces[uri] + ": <" + uri + "#>.\n"
        else:
            res += "@prefix " + namespaces[uri] + ": <" + uri + ">.\n"
    return res


def processNaf(naf: etree.Element, params: dict = {}) -> None:
    """Function to process elements of NAF file to RDF

    Args:
        naf: etree.element
        params: dict of params to store results

    Returns:
        None

    """
    provenance = genProvenanceName(params)
    for child in params["doc"].getroot():
        child_name: str = etree.QName(child).localname
        if child_name == "nafHeader":
            processHeader(child, params)
        if child_name == "raw":
            processRaw(child, params)
        if child_name == "text":
            processText(child, params)
        # if child_name == "formats":
        #   processFormats(child, params)
        if child_name == "entities":
            processEntities(child, params)
        if child_name == "terms":
            processTerms(child, params)
        if child_name == "deps":
            processDeps(child, params)
        # if child_name == "multiwords":
        #   processMultiwords(child, params)
    return None


def attrib2pred(s: str) -> str:
    """Function to convert attribute to RDF predicate

    Args:
        s: the attribute

    Returns:
        str: the RDF predicate

    """
    return "has" + s[0].upper() + s[1:]


def processHeader(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF header layer to RDF

    Args:
        element: element containing the header layer
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    output.write(prefix+":nafHeader\n")
    for item in element:
        if item.tag == "fileDesc":
            output.write("    naf-base:hasFileDesc [\n")
            for key in item.attrib.keys():
                if key in ["filename", "filetype"]:
                    output.write(
                        "        naf-fileDesc:"
                        + attrib2pred(key)
                        + ' """'
                        + item.attrib[key].replace('\\', "\\\\")
                        + '"""^^rdf:XMLLiteral ;\n'
                    )
                elif key == "creationtime":
                    output.write(
                        "        naf-fileDesc:"
                        + attrib2pred(key)
                        + ' "'
                        + item.attrib[key]
                        + '"^^xsd:dateTime ;\n'
                    )
                else:
                    output.write(
                        "        naf-fileDesc:"
                        + attrib2pred(key)
                        + " naf-base:"
                        + item.attrib[key]
                        + " ;\n"
                    )
            output.write("    ]")
        elif item.tag == "public":
            output.write("    naf-base:hasPublic [\n")
            for key in item.attrib.keys():
                pred = etree.QName(key).localname
                output.write(
                    "        dc:"
                    + pred
                    + ' """'
                    + item.attrib[key].replace('\\', "\\\\")
                    + '"""^^rdf:XMLLiteral ;\n'
                )
            output.write("    ]")
        elif item.tag == "linguisticProcessors":
            output.write("    naf-base:hasLinguisticProcessors [\n")
            for key in item.attrib.keys():
                if key == "layer":
                    output.write(
                        "        naf-base:"
                        + attrib2pred(key)
                        + " naf-base:"
                        + item.attrib[key]
                        + " ;\n"
                    )
                    output.write("        naf-base:lp [\n")
                    for lp in item:
                        for key2 in lp.attrib.keys():
                            if key2 in ["beginTimestamp", "endTimestamp"]:
                                output.write(
                                    "            naf-base:"
                                    + attrib2pred(key2)
                                    + ' "'
                                    + lp.attrib[key2]
                                    + '"^^xsd:dateTime ;\n'
                                )
                            else:
                                text = lp.attrib[key2].replace("\\", "\\\\")
                                output.write(
                                    "            naf-base:"
                                    + attrib2pred(key2)
                                    + ' "'
                                    + text
                                    + '"^^rdf:XMLLiteral ;\n'
                                )
                    output.write("        ] ;\n")
            output.write("    ]")
        if item == element[-1]:
            output.write(" .\n")
        else:
            output.write(" ;\n")
    output.write("\n")
    return None


def processSpan(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF span to RDF

    Args:
        element: element containing the span
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    for span in element:
        output.write("    naf-base:hasSpan (\n")
        for target in span:
            if target.tag == "target":
                output.write("        "+prefix+":" + target.attrib["id"] + "\n")
        output.write("    ) .\n")
    return None


def processEntities(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF entities layer to RDF

    Args:
        element: element containing the entities layer

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    for entity in element:
        eid = entity.attrib.get("id", None)
        output.write(prefix+":" + eid + "\n")
        output.write("    xl:type naf-base:entity ;\n")
        for key in entity.attrib.keys():
            if key != "id":
                output.write(
                    "    naf-base:"
                    + attrib2pred(key)
                    + " naf-entity:"
                    + entity.attrib[key]
                    + " ;\n"
                )
        processSpan(entity, params)
        output.write("\n")
    return None


def processRaw(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF raw layer to RDF

    Args:
        element: element containing the raw layer
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    output.write(prefix+":raw\n")
    output.write("    xl:type naf-base:raw ;\n")
    element_text = str(element.text).replace("\\", "\\\\")
    output.write('    naf-base:hasRaw """' + element_text + '"""^^rdf:XMLLiteral ;\n')
    output.write(" .\n")
    return None


def processTerms(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF terms layer to RDF

    Args:
        element: element containing the terms layer
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    for term in element:
        tid = term.attrib.get("id", None)
        output.write(prefix+":" + tid + "\n")
        output.write("    xl:type naf-base:term ;\n")
        for key in term.attrib.keys():
            if key != "id":
                if key == "lemma":
                    output.write(
                        "    naf-base:"
                        + attrib2pred(key)
                        + ' """'
                        + term.attrib[key]
                        + '"""^^rdf:XMLLiteral ;\n'
                    )
                elif key == "morphofeat":
                    # output.write("    naf-base:"+attrib2pred(key)+'s [\n')
                    for feat in term.attrib[key].split("|"):
                        output.write(
                            "    naf-morphofeat:"
                            + attrib2pred(feat.split("=")[0])
                            + ' "'
                            + feat.split("=")[1]
                            + '" ;\n'
                        )
                    # output.write("        ] ;\n")
                elif key == "pos":
                    if isHttpUrl(term.attrib[key]):
                        output.write(
                            "    naf-base:"
                            + attrib2pred(key)
                            + " <"
                            + term.attrib[key]
                            + ">"
                            + " ;\n"
                        )
                    elif term.attrib[key][0] == "&":
                        output.write(
                            "    naf-base:"
                            + attrib2pred(key)
                            + ' "'
                            + term.attrib[key]
                            + '" '
                            + " ;\n"
                        )
                    else:
                        output.write(
                            "    naf-base:"
                            + attrib2pred(key)
                            + " naf-pos:"
                            + term.attrib[key]
                            + " ;\n"
                        )
                elif key == "component_of":
                    output.write(
                        "    naf-base:is"
                        + key[0].upper()
                        + key[1:]
                        + " "+prefix+":"
                        + term.attrib[key]
                        + " ;\n"
                    )
                else:
                    output.write(
                        "    naf-base:"
                        + attrib2pred(key)
                        + " naf-base:"
                        + term.attrib[key]
                        + " ;\n"
                    )
        processSpan(term, params)
        output.write("\n")
    return None


def processText(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF text layer to RDF

    Args:
        element: element containing the text layer
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    for wf in element:
        wid = wf.attrib.get("id", None)
        output.write(prefix+":" + wid + "\n")
        output.write("    xl:type naf-base:wordform ;\n")
        wf_text = wf.text.replace("\\", "\\\\")
        output.write('    naf-base:hasText """' + wf_text + '"""^^rdf:XMLLiteral ;\n')
        for key in wf.attrib.keys():
            if key != "id":
                output.write(
                    "    naf-base:"
                    + attrib2pred(key)
                    + ' "'
                    + wf.attrib[key]
                    + '"^^xsd:integer'
                )
                if key == list(wf.attrib.keys())[-1]:
                    output.write(" .\n")
                else:
                    output.write(" ;\n")
        output.write("\n")
    return None


def processDeps(element: etree.Element, params: dict = {}) -> None:
    """Function to NAF deps layer to RDF

    Args:
        element: element containing the deps layer
        params: dict of params to store results

    Returns:
        None

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    for dep in element:
        if dep.tag == "dep":
            # depname = genDepName(params)
            # output.write("    xl:type naf-base:dep ;\n")
            rfunc = dep.attrib["rfunc"]
            rfunc = rfunc.replace("<PAD>", "pad")

            to_term = dep.attrib["to_term"]
            from_term = dep.attrib["from_term"]

            output.write(
                prefix+":" + from_term + " " + "naf-rfunc:" + rfunc + " "+prefix+":" + to_term + " .\n"
            )
            # for key in dep.attrib.keys():
            #     if (key != "id"):
            #         if key == "rfunc":
            #             output.write("    naf-base:"+attrib2pred(key)+' naf-base:'+dep.attrib[key]+' ;\n')
            #         else:
            #             output.write("    naf-base:"+attrib2pred(key)+' _:'+dep.attrib[key]+' ;\n')
            output.write("\n")
    return None


def genProvenanceName(params: dict) -> str:
    """Function to produce the provenance in RDF

    Args:
        element: element containing the header layer
        params: dict of params to store results

    Returns:
        str: name of provenance

    """
    output = params["out"]
    params["provenanceNumber"] += 1
    prefix = params.get("handlerPrefix", "_")
    name: str = prefix+":provenance" + str(params["provenanceNumber"])
    output.write("# provenance for data from same naf-file\n")
    output.write(name + " \n")
    output.write('    xl:instance """' + params["provenance"] + '"""^^rdf:XMLLiteral.\n\n')
    return name


def genDepName(params: dict) -> str:
    """Function to generate dependency name in RDF

    Args:
        params: dict of params to store results

    Returns:
        str: name of dependency

    """
    output = params["out"]
    prefix = params.get("handlerPrefix", "_")
    params["depNumber"] += 1
    name: str = prefix+":dep" + str(params["depNumber"])
    output.write(name + " \n")
    return name


if __name__ == "__main__":
    sys.exit(convert2rdf())
