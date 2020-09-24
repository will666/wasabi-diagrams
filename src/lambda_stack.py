from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server as Layer
from diagrams.programming.language import Python
from constants import GRAPH_ATTR, OUTPUT_PATH, OUTPUT_FORMAT


def lambda_stack() -> tuple:
    """ Runs generate of S3 events and media processing diagrams """
    e = s3_events_to_db()
    m = process_media()
    return (e, m)


def s3_events_to_db(
    graph_attr: dict = GRAPH_ATTR,
    output_format: str = OUTPUT_FORMAT,
    output_path: str = OUTPUT_PATH,
) -> str:
    """ Generates S3 events to DB diagrams """
    output = f"{output_path}/event_processing"

    with Diagram(
        "Event Processing",
        show=False,
        outformat=output_format,
        # graph_attr=graph_attr,
        filename=output,
    ):
        with Cluster("Serverless"):
            source = S3("S3 events")

            with Cluster("Event Flows"):
                with Cluster("Concurrent Processing"):
                    handlers = [Lambda("Python"), Lambda("Python"), Lambda("Python")]

            dw = Dynamodb("S3 metadata index")

            source >> handlers
            handlers >> dw

    return f"{output}.{output_format}"


def process_media(
    graph_attr: dict = GRAPH_ATTR,
    output_format: str = OUTPUT_FORMAT,
    output_path: str = OUTPUT_PATH,
) -> str:
    """ Generates media processing diagrams """
    output = f"{output_path}/media_processing"

    with Diagram(
        "Media Processing",
        show=False,
        outformat=output_format,
        # graph_attr=graph_attr,
        filename=output,
    ):
        cli = Python("CLI")

        with Cluster("Serverless"):
            source = SQS("tasks queue")

            with Cluster("Concurrent Processing"):
                handlers = Lambda("convert image\nencode video")

                with Cluster("Lambda layers"):
                    [Layer("ImageMagic"), Layer("ffmpeg")]

            src = S3("input\nmedia files")
            dest = S3("output\nmedia files")

            cli >> source >> handlers << src
            handlers >> dest

    return f"{output}.{output_format}"
