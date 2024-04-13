from isbtchot import controller
from isbtchot.schemas.args import TypeTime
import argparse

parser = argparse.ArgumentParser(description="BTC Hotness Index", prog="isbtchot")

parser.add_argument(
    "-p",
    "--periods_back",
    type=int,
    default=85,
    help="Periods back to be processed. Defaults to 85 if not provided.",
)

parser.add_argument(
    "-t",
    "--time",
    type=TypeTime,
    default=TypeTime.WEEK,
    help="Candle stick time to use: ME or W. Defaults to W (Weekly)",
)

parser.add_argument(
    "-d",
    "--dashboard",
    type=str,
    default="isbtchot",
    help="Dashboard to display: 'isbtchot' or 'power_law'. Defaults to 'isbtchot'.",
)


def main():

    # Parse args
    args = parser.parse_args()
    time_grouping: TypeTime = args.time
    periods_back: int = args.periods_back
    dashboard: str = args.dashboard

    if dashboard == "isbtchot":
        controller.dashboard_isbtchot(
            periods_back=periods_back, time_grouping=time_grouping
        )
    elif dashboard == "power_law":
        controller.dashboard_power_law(
            periods_back=periods_back, time_grouping=time_grouping
        )
    else:
        raise ValueError(f"Unknown dashboard: '{dashboard}'. Expected 'isbtchot' or 'power_law'.")

if __name__ == "__main__":
    main()
