import argparse
import json
import logging
import sys

log = logging.getLogger(__file__)


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beep-count", type=int, required=True)
    parser.add_argument("--boop-count", type=int, required=True)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main(beep_count=args.beep_count, boop_count=args.boop_count)
    except Exception as e:
        log.exception(e)


def main(beep_count: int, boop_count: int) -> None:
    log.info(f"Creating {beep_count} beeps and {boop_count} boops!")
    beeps = [f"{x}-beep" for x in range(1, beep_count + 1)]
    boops = [f"{x}-boop" for x in range(1, boop_count + 1)]
    print(json.dumps({"beeps": beeps, "boops": boops}))


if __name__ == "__main__":
    cli()
