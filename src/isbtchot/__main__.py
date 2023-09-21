from isbtchot import controller
from isbtchot.schemas.args import TypeTime
import argparse

parser = argparse.ArgumentParser(description="BTC Hotness Index", prog="isbtchot")

# Add an optional positional argument named 'year' with default value of 6
parser.add_argument(
    "-p",
    "--periods_back",
    type=int,
    default=85,
    help="Periods back to be processed. Defaults to 50 if not provided.",
)

parser.add_argument(
    "-t",
    "--time",
    type=TypeTime,
    default=TypeTime.WEEK,
    help="Candle stick time to use. Defaults to W (Weekly),"
)


def main():

    # Parse args
    args = parser.parse_args()
    time_grouping: TypeTime = args.time
    periods_back: int = args.periods_back

    controller.dashboard(periods_back=periods_back, time_grouping=time_grouping)

if __name__ == "__main__":
    main()
