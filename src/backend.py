from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server as Layer
from diagrams.aws.network import APIGateway
from diagrams.programming.language import Python
from constants import GRAPH_ATTR, OUTPUT_PATH, OUTPUT_FORMAT


def backend(
    graph_attr: dict = GRAPH_ATTR,
    output_format: str = OUTPUT_FORMAT,
    output_path: str = OUTPUT_PATH,
) -> str:
    """ Generates backend diagrams """
    output = f"{output_path}/backend"

    with Diagram(
        "Backend",
        show=False,
        outformat=output_format,
        # graph_attr=graph_attr,
        filename=output,
    ):

        with Cluster("Serverless"):
            apigw = APIGateway("API Gateway")

            with Cluster("Concurrent Processing"):
                handlers = [
                    Lambda("API (FastAPI)"),
                    Lambda("API (FastAPI)"),
                    Lambda("API (FastAPI)"),
                ]

            db = Dynamodb("data store")

        apigw >> handlers >> db >> handlers >> apigw

    return f"{output}.{output_format}"
