import argparse
import random
import sys
import time


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand", choices=["ahoy", "flaky"])
    args = parser.parse_args()

    if args.subcommand == "ahoy":
        ahoy()
    elif args.subcommand == "flaky":
        flaky()


def ahoy() -> None:
    while True:
        print("AHOY", flush=True)
        time.sleep(3)


def flaky() -> None:
    while True:
        print("AHOY?", flush=True)
        if random.random() < 0.1:
            sys.exit(1)
        time.sleep(3)


if __name__ == "__main__":
    cli()
