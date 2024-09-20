import logging
import signal
import sys
from argparse import ArgumentParser

import systemd.daemon  # type: ignore
from rpyc.utils.server import ThreadedServer  # type: ignore

from k3ng import K3NGService

logger = logging.getLogger(__name__)


def graceful_exit(signum, _):
    systemd.daemon.notify("STOPPING=1")
    logger.info("Received signal %s, stopping!", signal.Signals(signum).name)
    sys.exit(0)


def do_daemon(ser_port: str, rpc_port: int) -> None:
    # TODO: make this more secure!
    t = ThreadedServer(
        K3NGService(ser_port),
        port=rpc_port,
        protocol_config={
            "allow_public_attrs": True,
        },
    )
    systemd.daemon.notify("READY=1")
    t.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("rpyc").setLevel(logging.WARNING)
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    parser = ArgumentParser(
        prog="rpc_daemon", description="Start an RPC daemon for distributed control"
    )

    parser.add_argument(
        "serial_port", help="Serial port connected to the K3NG rotator Arduino"
    )
    parser.add_argument(
        "rpc_port",
        type=int,
        nargs="?",
        default=K3NGService.DEFAULT_PORT,
        help="Port for RPC to bind to",
    )

    args = parser.parse_args()

    do_daemon(args.serial_port, args.rpc_port)
