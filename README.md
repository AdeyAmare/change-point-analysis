# Brent Oil Market Change Point Analysis

This repository contains a time-series analysis project focused on understanding **structural changes in Brent oil prices** and how they relate to **major geopolitical, economic, and policy events**.

The project is developed in stages.
**Current submission covers foundational analysis only (Task 1).**

---

## Project Goal

* Identify periods where Brent oil price behavior changes significantly
* Relate detected changes to real-world events (e.g. conflicts, OPEC decisions, economic shocks)
* Support investment, policy, and operational decision-making using statistical analysis

---

## Current Scope (Task 1)

Implemented so far:

* Brent oil price data loading and validation
* Time-series diagnostics:

  * Trend behavior
  * Log returns
  * Volatility patterns
  * Stationarity checks (ADF + rolling statistics)
* Curated dataset of major geopolitical and economic events
* Reproducible notebooks for step-by-step analysis
* Basic unit tests for edge cases and failures

No change-point modeling or dashboards are included yet.

---

## Repository Structure

```
src/        Core analysis logic
notebooks/  Exploratory and step-by-step analysis
tests/      Unit tests
data/       Raw and processed datasets
```

Each directory has its own README with details.

---

## Data

* Daily Brent oil prices (USD per barrel)
* Time span: 1987–2022
* Event data compiled manually from historical sources

---

## Usage

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

### Run the analysis (recommended)

Open the step-by-step notebook:

```
notebooks/initial_analysis.ipynb
```

This notebook:

* Loads and validates Brent oil price data
* Computes time-series diagnostics
* Performs stationarity checks with visualizations
* Defines and saves the geopolitical events dataset

### Run tests

From the project root:

```bash
pytest tests/
```

### Use the analysis class in code

```python
from src.initial_analysis import BrentOilAnalysisFoundation

foundation = BrentOilAnalysisFoundation(
    brent_data_path="data/raw/BrentOilPrices.csv",
    events_output_path="data/processed/geopolitical_events.csv"
)

foundation.load_brent_data()
diagnostic_df = foundation.analyze_time_series_properties()
foundation.check_stationarity(diagnostic_df)
events_df = foundation.define_relevant_events()
foundation.save_events_dataset(events_df)
```

---

## Dependencies

All Python dependencies are listed in:

```
requirements.txt
```

---

## Next Steps

Planned work includes:

* Bayesian change point detection (PyMC)
* Quantifying before/after price regimes
* Event–change point alignment
* Interactive dashboard (Flask + React)

