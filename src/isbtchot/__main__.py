from isbtchot import controller
import argparse

parser = argparse.ArgumentParser(description="BTC Hotness Index", prog="isbtchot")

# Add an optional positional argument named 'year' with default value of 6
parser.add_argument(
    "year",
    type=int,
    nargs="?",
    default=7,
    help="The year to be processed. Defaults to 6 if not provided.",
)

def main(year):
    controller.dashboard(months=12 * year)

if __name__ == "__main__":
    args = parser.parse_args()
    year = args.year
    main(year)
