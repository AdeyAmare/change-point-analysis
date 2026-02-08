# Brent Oil Market Change Point Analysis

This repository contains a time-series analysis project that studies **structural changes in Brent oil prices** and how they relate to **major geopolitical, economic, and policy events**. The work follows a structured data science workflow and is developed in stages.

**The current submission covers Task 1 only: building the analytical foundation.**

---

## Project Goal

The goal of this project is to identify periods where the behavior of Brent oil prices changes in a meaningful way and to relate those changes to real-world events such as geopolitical conflicts, OPEC policy decisions, and major economic shocks.

By understanding when price regimes shift and how large those shifts are, the analysis aims to support better decision-making for investors, policymakers, and energy companies dealing with uncertainty in the global oil market.

---

## Why Change Point Analysis?

Brent crude oil prices are strongly affected by external events. Conflicts, sanctions, financial crises, and policy announcements can cause sudden changes in price levels or volatility. Because of this, oil prices rarely follow a single stable pattern over long periods.

Traditional time-series models often assume that statistical properties such as the mean and variance remain constant over time. This assumption does not hold well for oil prices. Change point analysis provides an alternative approach by explicitly allowing the data to shift between different regimes.

Task 1 focuses on preparing the data and understanding its behavior so that Bayesian change point models can be applied correctly in later stages.

---

## Current Scope (Task 1)

This stage focuses on understanding the data and setting up a solid analytical base. The work completed so far includes loading and validating Brent oil price data, performing exploratory time-series analysis, and examining key properties such as trends, log returns, volatility patterns, and stationarity using both statistical tests and rolling diagnostics.

In addition, a structured dataset of major geopolitical and economic events has been created. These events include OPEC decisions, conflicts in oil-producing regions, global financial crises, and major sanctions. The dataset records approximate start dates and brief descriptions and will later be used to interpret detected structural changes.

Reproducible notebooks document each step of the analysis, and basic unit tests are included to ensure core functionality works as expected.

At this stage, no change point models or dashboards have been implemented.

---

## Change Point Analysis: Conceptual Overview

Change point models are designed to detect moments in time when the underlying behavior of a time series changes. For Brent oil prices, this may mean a shift in average price levels, a change in volatility, or a transition to a new market regime.

Bayesian change point models are especially useful because they treat change points as uncertain quantities rather than fixed dates. Instead of producing a single break point, the model estimates a probability distribution over possible change dates. This allows uncertainty to be measured and reported directly.

In later tasks, Bayesian change point models will be used to identify structural breaks in Brent oil prices and to estimate how key parameters differ before and after those breaks.

---

## Expected Outputs of Change Point Modeling

When change point modeling is applied, the main outputs will include probability distributions for possible change point dates, estimates of model parameters for each regime (such as average price levels before and after a change), and uncertainty intervals around these estimates.

These outputs make it possible to say not only *when* a structural change likely occurred, but also *how confident* the model is about that timing and *how market behavior changed* across regimes.

Detected change points will then be compared with the event dataset to identify which geopolitical or economic events plausibly align with observed price shifts.

---

## Assumptions and Limitations

This analysis assumes that Brent oil prices reasonably reflect global oil market conditions and that major events are incorporated into prices within a relatively short time frame. In practice, markets may react slowly, anticipate events in advance, or respond to several overlapping factors at once.

The event dataset uses approximate start dates for complex developments such as conflicts or sanctions. Many of these events evolve over time, involve multiple decisions, or overlap with other shocks, which makes precise alignment with price changes uncertain.

Change point models identify **when** statistical properties of the price series change, but they do not explain **why** those changes occur. A detected change point occurring near a known event suggests a possible relationship, not proof of causation. Demonstrating causal impact would require additional variables and more complex economic modeling, which is beyond the scope of this project.

Finally, the current analysis focuses only on price data. Other important factors such as global demand, exchange rates, inflation, or inventory levels are not included, meaning some detected changes may be driven by unobserved influences.

---

## Repository Structure

```
src/        Core analysis logic
notebooks/  Exploratory and step-by-step analysis
tests/      Unit tests
data/       Raw and processed datasets
```

Each directory contains additional documentation describing its contents.

---

## Data

The project uses daily Brent oil prices recorded in USD per barrel, covering the period from 1987 to 2022. The geopolitical and economic event data is compiled manually from historical sources and focuses on events relevant to global oil markets.

---

## Usage

After cloning the repository, install the required dependencies:

```bash
pip install -r requirements.txt
```

The recommended starting point for Task 1 is the step-by-step notebook:

```
notebooks/initial_analysis.ipynb
```

This notebook loads and validates the price data, computes time-series diagnostics, performs stationarity checks with visualizations, and defines and saves the geopolitical events dataset.

Unit tests can be run from the project root using:

```bash
pytest tests/
```

The core analysis class can also be used directly in code:

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

## Next Steps

Future stages of the project will apply Bayesian change point detection using PyMC, quantify regime shifts in price behavior, align detected changes with real-world events, and present results through an interactive dashboard built with a Flask backend and a React frontend.

---