# Brent Oil Market Change Point Analysis

This repository contains a time-series analysis project focused on understanding **structural changes in Brent oil prices** and how they relate to **major geopolitical, economic, and policy events**. The project is developed in stages, following a structured data science workflow.

**The current submission covers foundational analysis only (Task 1).**

---

## Project Goal

The goal of this project is to identify periods where Brent oil price behavior changes significantly and to contextualize these changes using real-world events such as geopolitical conflicts, OPEC policy decisions, and major economic shocks. The analysis is intended to support data-driven decision-making for investors, policymakers, and energy companies by improving understanding of price dynamics, uncertainty, and regime shifts in the oil market.

---

## Analytical Motivation

Brent crude oil prices are highly sensitive to external shocks and policy interventions, often exhibiting abrupt changes in trend, volatility, or average price levels. Traditional time-series models that assume stable statistical properties over time are poorly suited to such environments. This project adopts a change point analysis perspective, which explicitly allows for **structural breaks** in the data-generating process.

Task 1 establishes the analytical foundation required to support Bayesian change point modeling in later stages of the project.

---

## Current Scope (Task 1)

The current stage focuses on understanding the data and preparing the analytical framework. Implemented components include:

Brent oil price data loading, validation, and preprocessing; exploratory time-series diagnostics including trend behavior, log returns, volatility patterns, and stationarity checks using both statistical tests and rolling statistics; and the construction of a curated dataset of major geopolitical and economic events relevant to the global oil market. Reproducible notebooks are provided to document each analytical step, alongside basic unit tests to validate core functionality and handle edge cases.

No change point modeling or dashboards are included at this stage.

---

## Change Point Analysis: Conceptual Overview

Change point models aim to detect points in time where the underlying statistical behavior of a time series changes. In the context of Brent oil prices, these changes may reflect shifts in market regimes driven by geopolitical events, policy decisions, or global economic disruptions.

Bayesian change point models are particularly well-suited for this task because they estimate change points probabilistically rather than deterministically. Instead of identifying a single break date, the model produces a posterior distribution over possible change point locations, allowing uncertainty to be quantified explicitly.

In later stages of this project, Bayesian change point analysis will be used to identify structural breaks in Brent oil prices and estimate how key parameters, such as average price levels or volatility, differ before and after detected regime shifts.

---

## Expected Outputs of Change Point Modeling

When applied, the change point models are expected to produce posterior distributions over change point dates, estimates of model parameters for each regime (for example, mean price levels before and after a break), and uncertainty intervals around all estimates. These outputs allow probabilistic statements about when structural changes likely occurred and how market behavior evolved across regimes, rather than relying on point estimates alone.

Detected change points will be compared with the curated event dataset to formulate hypotheses about which geopolitical or economic events plausibly coincide with observed structural shifts.

---

## Assumptions and Limitations

This analysis assumes that Brent oil prices reasonably reflect global oil market dynamics and that major geopolitical or economic events are incorporated into prices within a relatively short time window. In reality, market reactions may be delayed, anticipated in advance, or influenced by multiple overlapping factors.

The event dataset represents complex and often prolonged developments using approximate start dates. Many events evolve over extended periods, involve multiple policy actions, or overlap with other shocks, introducing temporal uncertainty when associating specific events with detected structural changes.

Change point models identify **when** statistical properties of the price series change, but they do not establish **why** those changes occur. The presence of a detected change point near the timing of a known event indicates a statistical association rather than a causal relationship. Establishing causality would require additional explanatory variables or structural economic modeling beyond the scope of this project.

Finally, the current analysis focuses exclusively on price data and does not incorporate other relevant drivers such as global demand indicators, exchange rates, inflation, or inventory levels. As a result, some detected changes may be driven by unobserved influences.

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

The project uses daily Brent oil prices recorded in USD per barrel, covering the period from 1987 to 2022. Event data is compiled manually from historical sources and includes major geopolitical, economic, and policy-related developments relevant to the oil market.

---

## Usage

After cloning the repository, install the required dependencies:

```bash
pip install -r requirements.txt
```

The recommended entry point for Task 1 is the step-by-step notebook:

```
notebooks/initial_analysis.ipynb
```

This notebook loads and validates the Brent oil price data, computes time-series diagnostics, performs stationarity checks with visualizations, and defines and saves the geopolitical events dataset.

Unit tests can be run from the project root using:

```bash
pytest tests/
```

The core analysis class can also be used programmatically:

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

Subsequent stages of the project will focus on Bayesian change point detection using PyMC, quantifying regime shifts in price behavior, aligning detected changes with real-world events, and developing an interactive dashboard using a Flask backend and a React frontend.

---
