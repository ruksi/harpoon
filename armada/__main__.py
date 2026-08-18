import json
import logging
import os
import socket
import socketserver
import sys
import threading
import time

log = logging.getLogger(__file__)


def main() -> None:
    config_dir = os.environ.get("VH_CONFIG_DIR")
    if not config_dir:
        raise Exception("Invalid VH_CONFIG_DIR; is this on Valohai?")

    my_member_id = os.environ.get("VH_DIST_MEMBER_ID")
    if not my_member_id:
        raise Exception("Invalid VH_DIST_MEMBER_ID; is this a distributed task?")

    with open(os.path.join(config_dir, "distributed.json")) as fp:
        cfg = json.load(fp)

    peers = {
        m["member_id"]: m["network"]["local_ips"][0]
        for m in cfg["members"]
        if m["member_id"] != my_member_id
    }
    log.info(
        f"I am member {my_member_id} of {cfg['config']['required_count']}; peers: {peers}"
    )

    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.sendall(f"hello from {my_member_id}".encode())

    port = 8888
    server = socketserver.ThreadingTCPServer(("0.0.0.0", port), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()

    for member_id, ip in peers.items():
        for attempt in range(1, 11):  # peers may not be listening the instant we are
            try:
                with socket.create_connection((ip, port), timeout=5) as sock:
                    log.info(
                        f"{my_member_id} <- {member_id}: {sock.recv(1024).decode()}"
                    )
                break
            except OSError as err:
                log.warning(f"attempt {attempt} to {member_id} ({ip}): {err}")
                time.sleep(3)
        else:
            raise SystemExit(f"could not reach {member_id} at {ip}:{port}")

    time.sleep(15)  # stay up so slower peers can still reach us
    log.info(f"member {my_member_id} done")


def cli() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main()
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    cli()
