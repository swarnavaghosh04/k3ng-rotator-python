import logging
from argparse import ArgumentParser

from k3ng import K3NG


def program_tle_from_file(tle_file: str, ser_port: str, track: bool) -> None:
    rot = K3NG(ser_port)

    rot.set_time()
    sat = rot.load_tle_from_file(tle_file)
    rot.check_time()
    rot.select_satellite(sat)
    rot.enable_tracking()
    rot.get_tracking_status()


def main():
    parser = ArgumentParser(
        prog="load_and_track.py",
        description="Loads a TLE from a file and begins tracking it",
    )
    parser.add_argument(
        "port",
        help="Serial port connected to an Arduino (typically /dev/ttyACM0)",
    )
    parser.add_argument("tle_file", help="TLE file")

    logging.basicConfig(level=logging.DEBUG)

    args = parser.parse_args()

    program_tle_from_file(args.tle_file, args.port, False)


if __name__ == "__main__":
    main()
