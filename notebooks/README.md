# `notebooks` — Interactive Analysis Notebooks

This folder contains Jupyter notebooks for **exploring and analyzing Brent oil price data** interactively. The notebooks demonstrate step-by-step workflows using the source code from `src/`.

---

## Notebooks

### `initial_analysis.ipynb`

This notebook provides an **interactive walkthrough** of the Brent oil price analysis pipeline:

* **Imports and Setup**

  * Adds the project root to the Python path to import the `BrentOilAnalysisFoundation` class from `src`.
  * Defines paths for raw data (`data/raw/BrentOilPrices.csv`) and processed outputs (`data/processed/geopolitical_events.csv`).

* **Data Loading**

  * Loads and validates Brent oil price data.
  * Displays basic statistics and data structure.

* **Time Series Diagnostics**

  * Computes log prices, returns, differences, and rolling volatility.
  * Plots the price trend and volatility over time.

* **Stationarity Check**

  * Performs Augmented Dickey-Fuller (ADF) test on the log price series.
  * Visualizes log price with rolling mean and standard deviation to assess stationarity.

* **Event Compilation**

  * Defines a structured dataset of major geopolitical, OPEC, and macroeconomic events.
  * Displays the events dataset.
  * Saves the events dataset to a CSV for downstream analysis.

---

## Usage

Run the notebook step by step in Jupyter or VSCode:

```python
# Imports and setup
from src.initial_analysis import BrentOilAnalysisFoundation
from pathlib import Path

project_root = Path.cwd().resolve().parent
brent_data_path = project_root / "data/raw/BrentOilPrices.csv"
events_output_path = project_root / "data/processed/geopolitical_events.csv"

# Initialize the analysis class
foundation = BrentOilAnalysisFoundation(
    brent_data_path=brent_data_path,
    events_output_path=events_output_path
)

# Load data
df = foundation.load_brent_data()

# Analyze time series
diagnostic_df = foundation.analyze_time_series_properties()

# Check stationarity
foundation.check_stationarity(diagnostic_df)

# Compile and save events
events_df = foundation.define_relevant_events()
foundation.save_events_dataset(events_df)
```

---

## Features

* Step-by-step **interactive exploration** of Brent oil price data.
* Visualizations for:

  * Price trends
  * Rolling volatility
  * Stationarity check
* Integration with source code in `src/` for reusable and maintainable analysis.
* Exports processed event datasets for further analysis or modeling.

---
