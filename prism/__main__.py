import logging


log = logging.getLogger(__file__)


def main() -> None:
    log.info("HELLO WORLD!")


def cli() -> None:
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
