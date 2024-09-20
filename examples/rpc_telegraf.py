import time
from argparse import ArgumentParser

import rpyc  # type: ignore

from k3ng import K3NGService

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="rpc_telegraf",
        description="Polls a K3NG rotator over RPC for basic telemetry",
    )
    parser.add_argument(
        "rpc_port",
        type=int,
        nargs="?",
        default=K3NGService.DEFAULT_PORT,
        help="Port of RPC server on localhost",
    )

    args = parser.parse_args()

    rot = rpyc.connect("localhost", args.rpc_port).root.K3NG

    az = rot.get_azimuth()
    el = rot.get_elevation()
    state = rot.get_tracking_status()

    # Format for Telegraf usage
    # Measurement
    measurement = "rotator,"
    # Tags
    measurement += f"satname={state.satname},sat_state={state.sat_state.name},"
    measurement += f"next_event={state.next_event.name} "
    # Fields
    measurement += f"next_event_mins={state.next_event_mins},"
    measurement += f"azimuth={az},"
    measurement += f"elevation={el},"
    measurement += f"is_tracking={int(state.is_tracking)} "
    # Timestamp
    measurement += str(time.time_ns())

    print(measurement)
