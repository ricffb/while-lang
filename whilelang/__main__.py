from argparse import ArgumentParser
from .jit import run_jit
from .interpret import run
from .parse import PProgram
from pathlib import Path
import sys


def get_argparse():
    parser = ArgumentParser(prog="whilelang",
                            description="WHILE lang interpreter.")

    parser.add_argument(
        '-p',
        '--parse-only',
        action="store_true",
        help=
        "Only parse the file without running. Useful for testing if the file format is correct."
    )

    parser.add_argument("file",
                        action="store",
                        type=Path,
                        help="The File containing the Program")
    parser.add_argument(
        "-i",
        action="store_true",
        help="Run in interpret mode. (Don't JIT Compile the While Code)")
    parser.add_argument("x1",
                        action="store",
                        type=int,
                        default=0,
                        help="First argument.",
                        nargs="?")

    parser.add_argument("x2",
                        action="store",
                        type=int,
                        default=0,
                        help="Second argument.",
                        nargs="?")

    return parser


def _main(argv):
    parser = get_argparse()
    args = parser.parse_args(argv)

    if args.parse_only:
        print(PProgram.parse())
        return

    with args.file.open("r") as fd:
        if args.i:
            var = run(fd, args.x1, args.x2)
            res = var["x0"]
        else:
            res = run_jit(fd, args.x1, args.x2)

    print(f"Result: x0 = {res}")


def main():
    _main(sys.argv[1:])


if __name__ == "__main__":
    main()