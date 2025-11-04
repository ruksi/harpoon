import argparse
import logging
import sys

log = logging.getLogger(__file__)


def main(*, dataset_name: str, file_count: int) -> None:
    log.info(
        f"TODO: functionality to generate a dataset version under '{dataset_name}' with {file_count} files"
    )


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-name", type=str, default="verses")
    parser.add_argument("--file-count", type=int, default=50)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main(**args.__dict__)
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
