import argparse
import json
import logging
from datetime import datetime, timezone

import valohai

log = logging.getLogger(__file__)


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-uri", type=str, required=True)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    try:
        main(model_uri=args.model_uri)
    except Exception as e:
        log.exception(e)


def main(model_uri: str) -> None:
    log.info("Creating an output file for the model...")
    model_path = valohai.outputs().path("model.txt")
    now = datetime.now(tz=timezone.utc).isoformat()
    with open(model_path, "w") as fp:
        fp.write(f"This is my model created at {now}.")
    log.info(f"Output file created: {model_path}")

    log.info("Defining that the file is a model...")
    metadata = {
        "valohai.model-versions": [
            {
                "model_uri": model_uri,
                "model_version_tags": ["red", "blue", "green", "yellow", "pink"],
                "model_release_note": "100% freshly squeezed unicorn juice 🌈",
            }
        ]
    }
    metadata_path = f"{model_path}.metadata.json"
    with open(metadata_path, "w") as fp:
        json.dump(metadata, fp)
    log.info(f"Model description added: {metadata_path}")


if __name__ == "__main__":
    cli()
