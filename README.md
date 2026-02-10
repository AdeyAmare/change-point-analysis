# Brent Oil Market Change Point Analysis

## Project Context

This project is part of the **10 Academy: Artificial Intelligence Mastery – Week 11 Challenge**, focusing on **Change Point Analysis and Bayesian Statistical Modeling of Time Series Data** applied to Brent crude oil prices. It combines **advanced statistical modeling, data engineering, and interactive visualization** to provide actionable insights into global energy markets.

The analysis is framed in a **real-world consulting context**. As a data scientist at **Birhan Energies**, the goal is to detect **structural shifts in Brent crude oil prices** influenced by geopolitical events, economic shocks, OPEC decisions, and policy interventions. These insights enable:

* **Investors** to manage risk and optimize portfolios
* **Policymakers** to plan for economic stability and energy security
* **Energy companies** to forecast prices, manage operational costs, and secure supply chains

The project is structured into **three main components**:

1. **Task 1:** Foundational data analysis, exploratory time series diagnostics, and event dataset creation
2. **Task 2:** Bayesian change point detection and posterior inference
3. **Dashboard:** Interactive React + Flask visualization integrating prices, change points, and events

Additionally, the **tests/ folder** ensures robustness, correctness, and proper error handling across the workflow.

---

## Business Problem

Global oil markets are inherently volatile due to **geopolitical conflicts, OPEC decisions, economic crises, and policy interventions**. These events can introduce **structural breaks** in price behavior, which traditional time series models often fail to capture.

The central question is:

> **When do structural changes occur in Brent oil prices, and how can these changes be meaningfully associated with major real-world events?**

Understanding these shifts supports decision-making in high-stakes environments, from investment strategies to national energy policies.

---

## Task 1: Laying the Foundation

**Objective:** Task 1 establishes a **clear data analysis workflow** and prepares the dataset for Bayesian modeling, ensuring proper understanding of the underlying statistical properties of Brent oil prices.

**Key Activities:**

* Data cleaning and validation
* Exploratory time series analysis (trends, volatility, stationarity)
* Log transformations and log return computations
* Rolling volatility diagnostics
* Compilation of a structured geopolitical and economic events dataset
* Documentation of assumptions, limitations, and implications for modeling

**Data Description:**

| Dataset             | Fields          | Description                                                    |
| ------------------- | --------------- | -------------------------------------------------------------- |
| Brent oil prices    | `Date`, `Price` | Daily USD per barrel, May 20, 1987 – Sep 30, 2022              |
| Geopolitical events | `Date`, `Event` | Manually curated dataset of major events impacting oil markets |

**Analysis Workflow:**

1. Load and validate raw Brent oil price data
2. Convert `Date` column to datetime format and sort chronologically
3. Perform exploratory analysis to identify long-term trends and shocks
4. Compute log prices and log returns
5. Analyze rolling volatility to highlight periods of heightened market uncertainty
6. Test stationarity using Augmented Dickey-Fuller (ADF) test and rolling statistics
7. Compile structured event dataset
8. Document assumptions and limitations

**Time Series Properties:**

* **Trend Analysis:** Identifies major shocks and regime-like behavior
* **Volatility Patterns:** Log returns highlight clustering of volatility
* **Stationarity Testing:** ADF test and rolling statistics indicate non-stationarity, motivating change point modeling

---

## Task 2: Bayesian Change Point Analysis

Task 2 extends Task 1 by implementing **Bayesian single change point detection** using **PyMC**. This framework identifies **structural breaks** in the price-generating process, estimates **pre- and post-change parameters**, and quantifies **uncertainty in the timing of regime shifts**.

**Modeling Highlights:**

* Detects a **single structural break** in log returns
* Estimates **posterior distributions** of mean daily returns before and after the change point
* Computes **percentage changes** to quantify market impact
* Associates change points with nearest geopolitical or economic events


**Expected Outputs:**

| Output                     | Format   | Description                                                        |
| -------------------------- | -------- | ------------------------------------------------------------------ |
| `change_point_results.csv` | CSV      | Posterior samples and mean estimates                               |
| Posterior analysis         | Notebook | Histograms and distributions of pre- and post-change point regimes |
| Event association          | Notebook | Closest event to detected change point                             |

**Assumptions and Limitations:**

* Detects **statistical shifts**, not causal effects
* Multiple overlapping events may contribute to a single detected change
* Market responses can be anticipatory or delayed
* Current model assumes **one primary change point**

---

## Event Dataset

A curated dataset of key geopolitical and economic events was created to provide **contextual interpretation** of detected change points.

| Event Type             | Example Events                                 |
| ---------------------- | ---------------------------------------------- |
| OPEC Decisions         | Production cuts, quotas, or increases          |
| Geopolitical Conflicts | Wars, sanctions, embargoes                     |
| Economic Crises        | 2008 financial crisis, COVID-19 demand shocks  |
| Policy Interventions   | International regulations affecting oil supply |

---

## Dashboard

An interactive dashboard visualizes **raw prices, detected change points, and events** for intuitive exploration by stakeholders.

**Analysis Points:**

| Analysis Point            | Description                                             |
| ------------------------- | ------------------------------------------------------- |
| Raw Prices                | Line chart of daily Brent oil prices                    |
| Statistical Change Points | Bar chart highlighting detected Bayesian change points  |
| Geopolitical Events       | Scatter chart marking major events from curated dataset |
| Integrated Analysis       | Overlay combining prices, change points, and events     |

**Backend (Flask API):**

| Endpoint            | Parameters     | Description                               |
| ------------------- | -------------- | ----------------------------------------- |
| `/api/prices`       | `start`, `end` | Returns Brent oil prices in date range    |
| `/api/change_point` | None           | Returns detected Bayesian change points   |
| `/api/events`       | `start`, `end` | Returns geopolitical events in date range |

**Frontend (React) Features:**

* Date filters for start and end date
* Fetches data from backend API using Axios
* Renders responsive **Recharts** charts
* Integrates uncertainty and event overlays

**Running Dashboard:**

```bash
# Backend
cd dashboard/backend
pip install -r requirements.txt
python app.py

# Frontend
cd dashboard/frontend
npm install
npm start
```

Access dashboard at `http://localhost:5173`.

---

## Tests

Unit tests verify **correctness, robustness, and error handling** across the project.

| Test File                       | Purpose                                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------- |
| `initial_analysis_tests.py`     | CSV loading, time series diagnostics, event dataset creation                                      |
| `test_change_point_analysis.py` | Data preparation, log returns, model preconditions, event association, empty/invalid CSV handling |

**Running Tests:**

```bash
pytest tests/
pytest -v tests/
pytest tests/test_change_point_analysis.py
```

---

## Repository Structure

```
src/        Core analysis logic (Task 1 + change point modeling)
notebooks/  Exploratory and analysis notebooks
dashboard/  React frontend + Flask backend
tests/      Unit tests
data/
  raw/      Original Brent oil price CSVs
  processed/ Structured event dataset and dashboard-ready CSVs
```

---

## Workflow Diagram

```text
Raw Data (Brent Prices) ──┐
                           │
                           ▼
                   Task 1 Analysis
                           │
          ┌────────────────┴─────────────┐
          ▼                              ▼
Change Point Analysis               Event Compilation
          │                              │
          └─────────┬─────────────┬──────┘
                    ▼             ▼
           Posterior Distributions  Structured Event Dataset
                    │             │
                    └─────┬───────┘
                          ▼
                     Interactive Dashboard
```

---

## Dependencies

| Technology / Library | Purpose                            |
| -------------------- | ---------------------------------- |
| Python 3.10+         | Core analysis                      |
| pandas               | Data manipulation                  |
| numpy                | Numerical operations               |
| PyMC                 | Bayesian modeling                  |
| matplotlib / seaborn | Visualization in notebooks         |
| Flask                | Backend API                        |
| Flask-CORS           | Cross-origin requests for frontend |
| React                | Frontend dashboard                 |
| Recharts             | Charts in React                    |
| pytest               | Unit testing                       |

---

## Full Usage Instructions

### Task 1: Data Analysis

```bash
pip install -r requirements.txt
python src/initial_analysis.py
```

*Outputs:* Time series diagnostics, log returns, rolling volatility plots, and exported `geopolitical_events.csv`.
Interactive notebook: `notebooks/initial_analysis.ipynb`.

### Task 2: Bayesian Change Point Analysis

Run in Jupyter notebook:

```bash
python notebooks/change_point_analysis.ipynb
```

*Outputs:* Posterior distributions, change point visualization, mean return shifts, event association.

### Dashboard

1. Start backend:

```bash
cd dashboard/backend
python app.py
```

2. Start frontend:

```bash
cd dashboard/frontend
npm install
npm start
```

Access dashboard at `http://localhost:5173`.

---

## Summary

This repository delivers a **complete end-to-end solution** for Brent oil market analysis:

* **Task 1:** Solid statistical foundation, exploratory analysis, and event dataset
* **Task 2:** Bayesian change point modeling with uncertainty quantification
* **Dashboard:** Interactive, stakeholder-focused visualization
* **Tests:** Ensures robustness and correct execution under edge cases

The project enables analysts and decision-makers to:

* Detect structural breaks in Brent oil prices
* Quantify shifts in regime behavior and uncertainty
* Contextualize market shifts with major geopolitical and economic events

