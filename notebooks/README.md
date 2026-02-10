# `notebooks` — Interactive Analysis Notebooks

This folder contains Jupyter notebooks for **exploring and analyzing Brent oil price data** interactively. These notebooks demonstrate step-by-step workflows using the source code in `src/` and provide reproducible, visual, and interpretable analysis.

---

## Notebooks

### `initial_analysis.ipynb`

This notebook guides users through the **fundamentals of Brent oil price analysis**:

* **Imports and Setup**
  Prepares the environment to use classes from `src/` and defines paths for raw data and processed outputs.

* **Data Loading**
  Loads the Brent oil price CSV, validates the columns, and displays summary statistics. This ensures the data is structured correctly for analysis.

* **Time Series Diagnostics**
  Computes log prices, daily returns, differences, and rolling volatility. Visualizations show how prices and volatility evolve over time, helping identify trends and periods of high market activity.

* **Stationarity Check**
  Performs an **Augmented Dickey-Fuller (ADF) test** on log prices to determine if the series is stationary. Rolling mean and standard deviation plots provide a visual check for stationarity, which is important for statistical modeling.

* **Event Compilation**
  Manually compiles a dataset of major geopolitical, OPEC, and macroeconomic events. This dataset is saved for use in downstream analysis, enabling contextual interpretation of price changes.

**Purpose:**
This notebook is ideal for **exploratory analysis**, understanding the behavior of Brent oil prices, and preparing data and events for modeling.

---

### `change_point_analysis.ipynb`

This notebook performs a **Bayesian change point analysis** using `BrentOilChangePointAnalysis`:

* **Imports and Setup**
  Configures the environment to access the change point analysis class and defines the raw data location.

* **Data Preparation**
  Loads and processes the raw price data, computes **daily log returns**, and thins the dataset for computational efficiency. Visualizations of prices and log returns help identify periods of volatility or abrupt changes.

* **Bayesian Change Point Modeling**
  Builds a Bayesian model to detect a single structural break in the log returns. The model estimates separate mean returns for periods before and after the change point, while a single volatility parameter is shared. MCMC sampling produces full posterior distributions, allowing uncertainty in the timing and magnitude of the shift to be quantified.

* **Model Diagnostics**
  Trace plots and posterior densities are examined to ensure proper MCMC convergence and reliable estimates. Overlapping posteriors across chains indicate that the model has thoroughly explored the parameter space.

* **Posterior Analysis**
  The histogram of the change point shows the most likely dates for the structural shift. Posterior distributions of mean returns reveal subtle changes in daily price movements before and after the change point.

* **Event Association**
  Optionally associates the detected change point with historical events. For example, a U.S. Senate investigation on **2004-11-16** coincides with the detected shift, providing context for the market behavior.

* **Impact Quantification**
  Calculates the change in mean daily log returns and expresses it as a percentage. This quantifies the magnitude of the structural shift in economic terms.

* **Results Export**
  Saves processed price data and change point results for dashboards or further analysis.

**Purpose:**
This notebook is designed for **probabilistic modeling** of regime shifts in oil prices. It integrates statistical rigor with historical context to interpret market behavior and quantify structural changes.

---

## Overall Notebook Workflow

1. **Start with `initial_analysis.ipynb`** to explore the data, compute diagnostics, and compile relevant events.
2. **Use `change_point_analysis.ipynb`** to detect Bayesian change points, analyze uncertainty, and associate shifts with events.
3. **Export results** for dashboards, further modeling, or reporting.

**Key Features Across Notebooks:**

* Interactive visualizations of prices, returns, volatility, and posterior distributions.
* Integration with reusable classes in `src/`.
* End-to-end reproducibility from raw data to event-contextualized results.
* Quantitative and visual interpretation of market behavior and structural shifts.


