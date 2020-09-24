import os

from scour import scour

from constants import OUTPUT_PATH, OUTPUT_FORMAT
from lambda_stack import lambda_stack
from backend import backend
from cli import cli
from frontend import frontend


if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)


def main(output_format: str = OUTPUT_FORMAT) -> None:
    """ Run generate on all modules """
    front = frontend()
    s3_events, process_medias = lambda_stack()
    output_backend = backend()
    output_cli = cli()

    if output_format == "svg":
        clean_svg()

    print(front, s3_events, process_medias, output_backend, output_cli)


def clean_svg(output_path: str = OUTPUT_PATH):
    """ Clean and fixes icon insert in created SVG files """

    svgs = os.listdir(output_path)

    for svg in svgs:
        item = f"{output_path}/{svg}"

        with open(item, "r") as r:
            src = r.read()

        data = scour.scourString(src)

        with open(item, "w") as w:
            w.write(data)


if __name__ == "__main__":
    main()
