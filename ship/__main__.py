import argparse
import random
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Literal, final


class ShipArgs(argparse.Namespace):
    subcommand: Literal["ahoy", "flaky", "greet"] = "ahoy"
    port: int = 0


def cli() -> None:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="subcommand", required=True)
    _ = subcommands.add_parser("ahoy")
    _ = subcommands.add_parser("flaky")

    greet_parser = subcommands.add_parser("greet")
    _ = greet_parser.add_argument("--port", type=int, required=True)

    args = parser.parse_args(namespace=ShipArgs())

    if args.subcommand == "ahoy":
        ahoy()
    elif args.subcommand == "flaky":
        flaky()
    elif args.subcommand == "greet":
        greet(args.port)


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


@final
class Greeter(BaseHTTPRequestHandler):
    def respond(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            _ = self.rfile.read(length)

        body = b"Hello World!"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        _ = self.wfile.write(body)

    do_GET = respond
    do_POST = respond


def greet(port: int) -> None:
    print(f"GREETING ON {port}", flush=True)
    HTTPServer(("", port), Greeter).serve_forever()


if __name__ == "__main__":
    cli()
