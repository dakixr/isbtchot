# isbtchot: BTC Hotness Index Dashboard

The `isbtchot` package provides a minimalist terminal dashboard for BTC's hotness index. It uses historical BTC data to create both BTC's price and Hotness Index visualizations right in your terminal.

# Demo

![BTC Hotness Index Dashboard Demo](media/demo.png)

## Features:

- BTC monthly candlestick plot with log scale.
- Hotness index based on PI with buy/sell signals.
- Data is cached to speed up subsequent requests.

## Installation

```bash
pip install isbtchot
```

## Usage

You can run the main dashboard with:

```bash
isbtchot [-periods_back P] [-time T]
```

- `-periods_back` or `--p`: Specifies the number of periods (e.g., weeks, months) of data you want to visualize. By default, it uses 85 periods.
- `-time` or `--t`: Specifies the candlestick time to use (e.g., Daily, Weekly). By default, it uses Weekly.

### Command Line Arguments

| Argument        | Short Form | Description                                                | Default               |
|-----------------|------------|------------------------------------------------------------|-----------------------|
| `--periods_back`| `-p`       | Number of periods to be processed.                         | 85                    |
| `--time`        | `-t`       | Candlestick time to use (e.g., D for Daily, W for Weekly). | W                     |

## Notes

- Ensure the terminal window is maximized for optimal visualization.
- Data is fetched from CryptoCompare API and cached locally for performance.

## Contributions

Please raise an issue or provide a pull request for any enhancements, bug fixes or features you'd like to add.
