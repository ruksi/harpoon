import argparse
import json
import logging
import sys
import time
import uuid

import valohai

log = logging.getLogger(__file__)


def main(*, dataset_name: str, file_count: int, package: bool) -> None:
    log.info(f"Creating dataset version under '{dataset_name}' with {file_count} files")

    dataset_version_name = f"{int(time.time())}-{file_count}"
    dataset_version_ref = f"dataset://{dataset_name}/{dataset_version_name}"
    log.info(f"Dataset version: {dataset_version_ref}")

    metadata_path = valohai.outputs().path("valohai.metadata.jsonl")

    with open(metadata_path, "w") as metadata_file:
        for i in range(file_count):
            id = str(uuid.uuid4())

            file_name = f"file-{id}.txt"
            file_path = valohai.outputs().path(file_name)
            with open(file_path, "w") as f:
                f.write(f"ID: {id}\n")
                f.write(f"Generated file {i + 1}/{file_count}\n")

            dataset_version_entry: dict[str, str | bool] = {"uri": dataset_version_ref}
            if package:
                dataset_version_entry["packaging"] = True

            metadata_content = {
                "valohai.dataset-versions": [dataset_version_entry],
            }

            metadata_entry = {
                "file": file_name,
                "metadata": metadata_content,
            }
            json.dump(metadata_entry, metadata_file)
            metadata_file.write("\n")

    log.info(f"Created {file_count} files for {dataset_version_ref}")
    if package:
        log.info("... with packaging enabled!")

    log.info(f"Metadata saved to {metadata_path}")


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-name", type=str, default="verses")
    parser.add_argument("--file-count", type=int, default=50)
    parser.add_argument("--package", action="store_true", default=False)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main(**args.__dict__)
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
