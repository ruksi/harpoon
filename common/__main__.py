import logging
import sys
import time

log = logging.getLogger(__file__)


def main() -> None:
    duration = 1.0
    log.info(f"I'll take a quick nap! ({duration}s)")
    time.sleep(duration)


def cli() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    log.info(f"Called 'common' with parameters: {sys.argv[1:]}")
    try:
        main()
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
