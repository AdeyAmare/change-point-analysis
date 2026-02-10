# `src`

This folder contains the main source code for **analyzing Brent oil price data**, including traditional time series diagnostics and Bayesian change point analysis. These tools provide a foundation for exploratory data analysis, statistical modeling, and economic interpretation.

---

## Modules

### `initial_analysis.py`

Provides the class **`BrentOilAnalysisFoundation`**, responsible for:

* Loading and validating Brent oil price data from CSV.
* Computing basic time series diagnostics:

  * Log prices
  * Price differences
  * Log returns
  * Rolling volatility
* Checking stationarity using the **Augmented Dickey-Fuller (ADF) test**, with visualizations.
* Compiling a structured dataset of major **geopolitical, OPEC, and macroeconomic events** affecting oil prices.
* Saving events data for downstream use.
* Executing a sequential pipeline for all the above steps.

**Usage Example:**

```python
from pathlib import Path
from initial_analysis import BrentOilAnalysisFoundation

foundation = BrentOilAnalysisFoundation(
    brent_data_path=Path("../data/raw/BrentOilPrices.csv"),
    events_output_path=Path("../data/processed/geopolitical_events.csv")
)

# Run the full pipeline
foundation.run_task_1_pipeline()
```

**Features:**

* Logging of key steps and statistics.
* Plots: price over time, rolling volatility, and stationarity checks.
* Error handling for missing files or columns.

**Assumptions & Limitations:**

* Input CSV must contain `Date` and `Price` columns.
* Rolling window of 30 days is used for stationarity checks.
* Event dataset is manually compiled; dates are approximate.

---

### `change_point_analysis.py`

Provides the class **`BrentOilChangePointAnalysis`**, responsible for:

* Loading and preparing Brent oil price data.
* Computing daily **log returns** and thinning datasets for performance.
* Building a **Bayesian change point model** using PyMC to detect regime shifts in log returns.
* Analyzing posterior distributions of:

  * Change point index (`tau`)
  * Mean log returns before (`mu_1`) and after (`mu_2`) the change point
* Plotting diagnostics for trace convergence, posterior distributions, and price series overlays.
* Quantifying the **impact of the change point** on mean log returns.
* Associating detected change points with relevant **historical events**.
* Exporting results for dashboards or downstream analyses.

**Usage Example:**

```python
from pathlib import Path
from change_point_analysis import BrentOilChangePointAnalysis

analysis = BrentOilChangePointAnalysis(
    csv_path=Path("../data/raw/BrentOilPrices.csv"),
    events_csv=Path("../data/processed/geopolitical_events.csv")
)

# Run the full analysis pipeline
analysis.run_full_analysis()

# Retrieve change point details
tau_idx, change_date = analysis.get_change_point_date()
impact = analysis.quantify_impact()
print(f"Change point at {change_date}, mean log return shifted by {impact['percentage_change']:.2f}%")
```

**Features:**

* Bayesian modeling with **PyMC** and posterior diagnostics with **ArviZ**.
* Plots: price series, log returns, posterior distributions, and change point overlays.
* Automatic detection and interpretation of regime shifts.
* Optional event association for contextual analysis.
* Results export for dashboard integration.
* Logging and error handling for reproducibility.

**Assumptions & Limitations:**

* Input CSV must contain `Date` and `Price` columns.
* Dataset is thinned to improve performance; very high-frequency data may require adjustment.
* Priors are narrow for faster convergence; results are sensitive to prior choices.
* Event dataset is optional; if provided, it must include `event_date`, `event_name`, and `description`.

---

### Common Features Across Modules

* Both modules support **logging**, **plots**, and **CSV output**.
* Designed for reproducibility and sequential pipelines.
* Data validation is enforced to catch missing or malformed columns.

---

### Recommended Workflow

1. **Start with `initial_analysis.py`** to perform exploratory data analysis, compute log returns, and compile events.
2. **Use `change_point_analysis.py`** to detect Bayesian change points, interpret their economic significance, and optionally associate with events.
3. **Export results** for dashboards or downstream modeling.

---
