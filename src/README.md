# `src`

This folder contains the main source code for analyzing Brent oil price data. The code provides tools for **data loading, time series diagnostics, stationarity checks, and event compilation**, serving as a foundation for further analysis or modeling.

---

## Files

### `initial_analysis.py`

Contains the class:

**`BrentOilAnalysisFoundation`**

Responsibilities:

* Load and validate Brent oil price data from a CSV file.
* Compute basic time series diagnostics:

  * Log prices
  * Price differences
  * Log returns
  * Rolling volatility
* Check stationarity of the series using the Augmented Dickey-Fuller (ADF) test, with visualization.
* Compile a structured dataset of major geopolitical, OPEC, and macroeconomic events affecting oil prices.
* Save events data to a CSV for downstream use.
* Provide a pipeline to execute all of the above steps sequentially.

---

## Usage

```python
from pathlib import Path
from initial_analysis import BrentOilAnalysisFoundation

# Initialize class
foundation = BrentOilAnalysisFoundation(
    brent_data_path=Path("../data/raw/BrentOilPrices.csv"),
    events_output_path=Path("../data/processed/geopolitical_events.csv")
)

# Load data
foundation.run_task_1_pipeline()
```

---

## Features

* **Logging**: Key steps and statistics are logged for reproducibility.
* **Plots**:

  * Brent oil price over time
  * Rolling volatility
  * Stationarity check with rolling mean & standard deviation
* **Error handling**:

  * Raises `FileNotFoundError` if the data file is missing.
  * Raises `ValueError` if required columns (`Date`, `Price`) are missing.
  * Raises `RuntimeError` if operations are attempted before data is loaded.

---

## Assumptions & Limitations

* Input CSV must contain `Date` and `Price` columns.
* Time series diagnostics assume daily frequency but can handle irregular dates.
* Stationarity check uses a rolling window of 30 days.
* Event dataset is manually compiled from historical records; dates are approximate.

---
