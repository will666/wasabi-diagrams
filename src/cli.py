from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server as Layer
from diagrams.aws.network import APIGateway
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.onprem.compute import Server

from constants import GRAPH_ATTR, OUTPUT_PATH, OUTPUT_FORMAT


def cli(
    graph_attr: dict = GRAPH_ATTR,
    output_format: str = OUTPUT_FORMAT,
    output_path: str = OUTPUT_PATH,
) -> str:
    """ Generates CLI diagrams """
    output = f"{output_path}/cli"

    with Diagram(
        "CLI",
        show=False,
        outformat=output_format,
        # graph_attr=graph_attr,
        filename=output,
    ):
        cli = Python("CLI")

        with Cluster("targets"):

            with Cluster("local resources"):
                data = Storage("build objects\nassets")
                layers = Layer("build\nLambda layers")
                server = Server("media\nlocal build")

            with Cluster("cloud resources"):
                db = Dynamodb("create DB\nseed DB")
                s3 = S3("sync data")
                lbd = Lambda("resize images\nencode video")
                sqs = SQS("queue\nmedia generate\ntasks")

        cli >> data >> cli
        cli >> s3
        cli >> db
        cli >> lbd
        cli >> sqs
        cli >> layers
        cli >> server

    return f"{output}.{output_format}"
