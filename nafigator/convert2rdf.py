# coding: utf-8

"""Convert2rdf module."""

import sys
import click
from io import StringIO, BytesIO

from .nafdocument import NafDocument
from lxml import etree
import rdflib


@click.command()
@click.option(
    "--input", default="data/example.naf", prompt="input file", help="The input file"
)
@click.option(
    "--output", default="data/example.ttl", prompt="output file", help="The output file"
)
def opennaf(input: str, output: str):
    """ """
    naf = NafDocument().open(input)

    params: dict = dict()
    params["namespaces"]: dict = dict()
    params["provenanceNumber"]: int = 0
    params["depNumber"]: int = 0
    params["provenance"]: str = input

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

    params["out"]: StringIO = StringIO()

    params["prefix"] = printNamespaces(params)

    params["naf"] = NafDocument().open(input)

    processNaf(naf, params)

    file_content: StringIO = StringIO()
    file_content.write("# RDF triples (turtle syntax)\n\n")
    file_content.write("# NAF URI  '" + input + "'\n")
    file_content.write("\n")
    file_content.write(params["prefix"])
    file_content.write("\n\n")
    file_content.write(params["out"].getvalue().replace("\u2264", ""))

    content = file_content.getvalue()

    if output:
        fh = open(output, "w", encoding="utf-8")
        fh.write(content)
        fh.close()

    g = rdflib.Graph()
    g.parse(data=content, format="turtle")
    content = BytesIO()
    content.write(g.serialize(format="xml"))
    fh = open("".join(output.split(".")[0:-1]) + ".rdf", "wb")
    fh.write(content.getvalue())
    fh.close()


def isHttpUrl(url):
    return isinstance(url, str) and (
        url.startswith("http://") or url.startswith("https://")
    )


def addNamespace(prefix, uri, params):
    namespaces = params["namespaces"]
    found = namespaces.get(uri, None)
    if found:
        if prefix != found:
            return -1
        del namespaces[uri]
    namespaces[uri] = prefix
    return 0


def printNamespaces(params):
    namespaces = params["namespaces"]
    res: str = ""
    for uri in namespaces:
        if uri[-1] != "#":
            res += "@prefix " + namespaces[uri] + ": <" + uri + "#>.\n"
        else:
            res += "@prefix " + namespaces[uri] + ": <" + uri + ">.\n"
    return res


def processNaf(naf, params):

    provenance = genProvenanceName(params)

    for child in params["naf"].getroot():
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


def attrib2pred(s):
    return "has" + s[0].upper() + s[1:]


def processHeader(element, params):

    output = params["out"]
    output.write("_:nafHeader\n")
    for item in element:
        if item.tag == "fileDesc":
            output.write("    naf-base:hasFileDesc [\n")
            for key in item.attrib.keys():
                if key in ["filename", "filetype"]:
                    output.write(
                        "        naf-fileDesc:"
                        + attrib2pred(key)
                        + ' "'
                        + item.attrib[key]
                        + '"^^rdf:XMLLiteral ;\n'
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
                    + ' "'
                    + item.attrib[key]
                    + '"^^rdf:XMLLiteral ;\n'
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


def processSpan(element, params):
    output = params["out"]
    for span in element:
        output.write("    naf-base:hasSpan [\n")
        for target in span:
            if target.tag == "target":
                output.write("        naf-base:ref _:" + target.attrib["id"] + "\n")
        output.write("    ] .\n")


def processEntities(element, params):

    output = params["out"]
    for entity in element:
        eid = entity.attrib.get("id", None)
        output.write("_:" + eid + "\n")
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


def processRaw(element, params):

    output = params["out"]
    output.write("_:raw\n")
    output.write("    xl:type naf-base:raw ;\n")
    output.write('    naf-base:hasRaw """' + element.text + '"""^^rdf:XMLLiteral ;\n')
    output.write(" .\n")


def processTerms(element, params):

    output = params["out"]
    for term in element:
        tid = term.attrib.get("id", None)
        output.write("_:" + tid + "\n")
        output.write("    xl:type naf-base:term ;\n")
        for key in term.attrib.keys():
            if key != "id":
                if key == "lemma":
                    output.write(
                        "    naf-base:"
                        + attrib2pred(key)
                        + ' "'
                        + term.attrib[key]
                        + '" ;\n'
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
                        + " _:"
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


def processText(element, params):

    output = params["out"]
    for wf in element:
        wid = wf.attrib.get("id", None)
        output.write("_:" + wid + "\n")
        output.write("    xl:type naf-base:wordform ;\n")
        output.write('    naf-base:hasText """' + wf.text + '"""^^rdf:XMLLiteral ;\n')
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


def processDeps(element, params):

    output = params["out"]
    for dep in element:
        if dep.tag == "dep":
            # depname = genDepName(params)
            # output.write("    xl:type naf-base:dep ;\n")
            rfunc = dep.attrib["rfunc"]
            to_term = dep.attrib["to_term"]
            from_term = dep.attrib["from_term"]
            output.write(
                "_:" + from_term + " " + "naf-rfunc:" + rfunc + " _:" + to_term + "\n"
            )
            # for key in dep.attrib.keys():
            #     if (key != "id"):
            #         if key == "rfunc":
            #             output.write("    naf-base:"+attrib2pred(key)+' naf-base:'+dep.attrib[key]+' ;\n')
            #         else:
            #             output.write("    naf-base:"+attrib2pred(key)+' _:'+dep.attrib[key]+' ;\n')
            output.write(" .\n")


def genProvenanceName(params: dict) -> str:
    output = params["out"]
    params["provenanceNumber"] += 1
    name: str = "_:provenance" + str(params["provenanceNumber"])
    output.write("# provenance for data from same naf-file\n")
    output.write(name + " \n")
    output.write('    xl:instance "' + params["provenance"] + '".\n\n')
    return name


def genDepName(params: dict) -> str:
    output = params["out"]
    params["depNumber"] += 1
    name: str = "_:dep" + str(params["depNumber"])
    output.write(name + " \n")


if __name__ == "__main__":
    sys.exit(opennaf())
