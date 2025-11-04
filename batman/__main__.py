import json
import logging
import random
import string
import sys
from datetime import datetime, timezone

import valohai

log = logging.getLogger(__file__)


def main() -> None:
    maybe_batman = "".join(random.choices(string.ascii_uppercase, k=6))
    chant = f"nana nana nana nana {maybe_batman}!"

    filename = "chant.txt"

    chant_path = valohai.outputs().path(filename)
    now = datetime.now(tz=timezone.utc).isoformat()
    with open(chant_path, "w") as fp:
        fp.write(f"{now}: {chant}")

    metadata = {"valohai.alias": "chant"}
    metadata_path = valohai.outputs().path(f"{filename}.metadata.json")
    with open(metadata_path, "w") as fp:
        json.dump(metadata, fp)

    log.info(chant)


def cli() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main()
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
