from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server as Layer
from diagrams.aws.network import APIGateway
from diagrams.aws.network import CloudFront
from diagrams.programming.language import Python
from diagrams.programming.framework import React
from diagrams.onprem.client import Client
from constants import GRAPH_ATTR, OUTPUT_PATH, OUTPUT_FORMAT


def frontend(
    graph_attr: dict = GRAPH_ATTR,
    output_format: str = OUTPUT_FORMAT,
    output_path: str = OUTPUT_PATH,
) -> str:
    """ Generates frontend diagrams """
    output = f"{output_path}/frontend"

    with Diagram(
        "Frontend",
        show=False,
        outformat=output_format,
        # graph_attr=graph_attr,
        filename=output,
    ):

        client = Client("client")

        with Cluster("Serverless"):

            with Cluster("UI"):
                with Cluster("cache"):
                    web_cdn = CloudFront("CDN\nUI")

                with Cluster("static"):
                    web_host = S3("web")
                    react = React("app")

            with Cluster("Static Assets"):
                with Cluster("cache"):
                    assets_cdn = CloudFront("CDN\nassets")
                    assets_apigw = APIGateway("API Gateway")

                assets = S3("assets\nimages")

                with Cluster("media processing"):
                    assets_gen = Lambda("generate image")
                    layers = Layer("layer\nImageMagick")

        web_cdn << react << web_host
        assets_cdn << assets_apigw << assets_gen << layers << assets
        client - Edge(color="orange") << assets_cdn
        client - Edge(color="orange") << web_cdn
        assets_apigw >> assets_gen
        assets_cdn >> assets_apigw

    return f"{output}.{output_format}"
