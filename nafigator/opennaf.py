# coding: utf-8

"""Main module."""

import sys
import click
from .nafdocument import NafDocument
from .const import MultiwordElement
from .const import ProcessorElement
from .const import EntityElement


@click.command()
@click.option(
    "--input",
    default="data/example.naf.xml",
    prompt="input file",
    help="The input file",
)
def opennaf(input: str):
    """ """
    naf = NafDocument().open(input)
    # print(naf.header)
    # print(naf.version)
    # print(naf.raw)
    # print(naf.text)
    # print(naf.terms)

    # entity_data = EntityElement(
    #     id="test_id",
    #     type="PERSON",
    #     status=None,
    #     source="source",
    #     span=["t1"],
    #     ext_refs=[
    #         {"resource": "res", "reference": "https:ref"},
    #         {"resource": "res2", "reference": "https:ref2"},
    #     ],
    #     comment=["comment"],
    # )
    # naf.add_entity_element(data=entity_data, naf_version="v3.1", comments=True)
    print(naf.entities)

    # print(naf.deps)
    # print(naf.formats)
    # print(naf.multiwords)
    # naf.remove_layer_elements("multiwords")
    # print(naf.multiwords)
    # print(naf.paragraphs)

    # lp = ProcessorElement(
    #     name="processorname",
    #     version="1.0",
    #     timestamp=None,
    #     beginTimestamp=None,
    #     endTimestamp=None,
    #     hostname=None,
    # )

    # naf.add_processor_element("recommendations", lp)

    # layer = naf.layer("recommendations")

    # data_recommendation = {
    #     "id": "recommendation1",
    #     "subjectivity": 0.5,
    #     "polarity": 0.25,
    #     "span": ["t37", "t39"],
    # }

    # element = naf.subelement(
    #     element=layer, tag="recommendation", data=data_recommendation
    # )

    # naf.add_span_element(element=element, data=data_recommendation)

    # print(naf.recommendations)

    # print(naf.sentences)


if __name__ == "__main__":
    sys.exit(opennaf())
