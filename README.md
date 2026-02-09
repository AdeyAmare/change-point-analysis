# Brent Oil Market Change Point Analysis

**Task 1 – Laying the Foundation for Analysis**

## Project Context

This project is developed as part of the **10 Academy: Artificial Intelligence Mastery – Week 11 Challenge**, focusing on **Change Point Analysis and Bayesian Statistical Modeling of Time Series Data**.

The analysis is framed within a real-world consulting context. As a data scientist at **Birhan Energies**, the goal is to understand how major geopolitical, economic, and policy-driven events influence **Brent crude oil prices**, and to prepare a rigorous analytical foundation for Bayesian change point modeling in later stages.

This repository currently contains **Task 1 only**, which establishes the data, workflow, assumptions, and statistical groundwork required for robust change point analysis.

---

## Business Problem

Global oil markets are highly sensitive to geopolitical conflicts, OPEC policy decisions, economic crises, and international sanctions. These events can introduce **structural breaks** in price behavior rather than temporary fluctuations.

This volatility presents challenges for:

* Investors managing risk and portfolio exposure
* Policymakers planning for economic stability and energy security
* Energy companies forecasting prices, managing costs, and securing supply chains

The core business question guiding this project is:

**When do structural changes occur in Brent oil prices, and how can these changes be meaningfully associated with major real-world events?**

---

## Objective of Task 1

The objective of Task 1 is to **define a clear data analysis workflow and develop a deep understanding of both the data and the modeling approach** before applying Bayesian change point detection.

Specifically, Task 1 focuses on:

* Understanding the statistical properties of Brent oil price data
* Preparing diagnostics that inform modeling choices
* Compiling a structured dataset of major geopolitical and economic events
* Clearly documenting assumptions, limitations, and communication strategy

No change point models are implemented at this stage.

---

## Data Description

The primary dataset consists of **daily Brent oil prices (USD per barrel)** covering the period from **May 20, 1987 to September 30, 2022**.

**Fields**

* `Date`: Daily observation date (converted to datetime format)
* `Price`: Brent crude oil price in USD per barrel

A secondary dataset is manually compiled and contains **major geopolitical, economic, and policy events** relevant to global oil markets.

---

## Analysis Workflow

The planned analysis workflow follows a standard data science lifecycle and is fully implemented for Task 1.

The steps include:

1. Loading and validating raw Brent oil price data
2. Converting dates to a proper datetime index and sorting chronologically
3. Performing exploratory time series analysis to understand long-term trends
4. Computing transformations such as log prices and log returns
5. Analyzing volatility patterns using rolling window diagnostics
6. Testing stationarity using statistical tests and rolling statistics
7. Compiling a structured dataset of key geopolitical and economic events
8. Documenting assumptions, limitations, and modeling implications

This workflow prepares the data and context required for Bayesian change point modeling in later tasks.

---

## Time Series Properties and Diagnostics

Before applying any statistical model, the Brent oil price series is analyzed to understand its core properties.

### Trend Analysis

The raw price series is visualized to identify long-term movements, major shocks, and regime-like behavior over time.

### Volatility Patterns

Log returns are computed to reduce scale effects and highlight volatility clustering. Rolling volatility diagnostics are used to observe periods of heightened market uncertainty.

### Stationarity Testing

Stationarity is assessed using the **Augmented Dickey-Fuller (ADF) test**, complemented by rolling mean and rolling standard deviation plots. These diagnostics inform whether differencing or transformations are required for downstream modeling.

These analyses confirm that Brent oil prices exhibit **non-stationarity and regime-dependent behavior**, motivating the use of change point models rather than traditional fixed-parameter time series methods.

---

## Change Point Analysis: Conceptual Overview

Change point models are designed to detect **structural breaks** in a time series—points where the underlying data-generating process changes.

In the context of Brent oil prices, a change point may represent:

* A shift in average price levels
* A change in volatility regime
* A transition driven by persistent geopolitical or economic shocks

Bayesian change point models are particularly well-suited for this problem because they:

* Treat change points as uncertain rather than fixed
* Estimate probability distributions over possible change dates
* Quantify uncertainty in both timing and parameter changes

Task 1 focuses on preparing the data and diagnostics so that Bayesian change point models can be applied correctly and interpreted responsibly in later stages.

---

## Bayesian Change Point Models: Purpose and Expected Outputs

Bayesian change point models are used to identify points in time where the underlying data-generating process of a time series changes. In the context of Brent oil prices, these models aim to detect structural breaks or regime shifts, such as changes in average price levels, volatility, or overall market dynamics.

The expected outputs of a Bayesian change point analysis include posterior probability distributions over potential change point dates, as well as estimates of model parameters before and after each detected break. These outputs allow probabilistic statements about when a structural shift most likely occurred, how market behavior differed across regimes, and the uncertainty surrounding these estimates.

Rather than producing a single deterministic change date, the Bayesian framework quantifies uncertainty explicitly, which is particularly important in volatile markets where multiple overlapping influences may be present.

## Change Point Analysis: Purpose, Outputs, and Limitations

A change point model is a statistical framework designed to identify points in time at which the underlying data-generating process of a time series changes. In the context of Brent oil prices, this means detecting periods where key parameters such as the mean level, variance, or overall volatility regime shift, indicating a structural break rather than normal short-term price fluctuations.

Change point models are used because oil price dynamics are influenced by discrete shocks—such as geopolitical conflicts, policy interventions, or economic crises—that can alter market behavior in a persistent way. Traditional time series models assume stable parameters over time and therefore struggle to capture these regime shifts. Change point methods explicitly relax this assumption, making them well-suited for analyzing non-stationary financial and commodity price series.

The primary outputs of change point analysis include estimated change point dates and parameter estimates before and after each detected break. In a Bayesian framework, these outputs are expressed as posterior distributions, allowing probabilistic assessment of when a structural change most likely occurred and how the statistical properties of prices differ across regimes. These results support interpretation of how market behavior evolves over time rather than providing exact deterministic break dates.

Despite their usefulness, change point models have important limitations. They identify when statistical changes occur but do not explain why they occur. Multiple overlapping events may contribute to a single detected change, and market reactions may be anticipatory or delayed relative to observable events. Consequently, detected change points should be interpreted as indicators of structural change that require external contextual information, rather than as evidence of direct causal relationships.

## Expected Outputs of Change Point Modeling

Although change point models are not implemented in Task 1, the expected outputs are clearly defined.

These include:

* Posterior probability distributions over possible change point dates
* Estimates of model parameters before and after each detected break
* Uncertainty intervals quantifying confidence in detected regime shifts

Rather than producing a single deterministic break date, the Bayesian framework allows probabilistic statements about **when structural changes most likely occurred and how market behavior differed across regimes**.

---

## Event Dataset

A structured dataset of **major geopolitical, economic, and policy events** has been compiled and saved as a CSV file.

The dataset includes events such as:

* OPEC production decisions
* Geopolitical conflicts in oil-producing regions
* Global financial crises
* COVID-19 and demand shocks
* International sanctions and supply disruptions

Each event is recorded with an approximate start date and a concise description. These events will later be used to **contextualize detected change points**, not to assert direct causality.

---

## Assumptions and Limitations

This analysis assumes that Brent oil prices reasonably reflect global oil market dynamics and that major events are incorporated into prices within a relatively short time frame.

Several limitations are acknowledged:

* Markets may anticipate events before official dates or react with delays
* Many geopolitical events evolve over time and overlap with other shocks
* Change point models detect statistical changes, not causal mechanisms
* Correlation in timing does not imply causal impact

Detected change points should therefore be interpreted as **indicators of structural change that require external contextual reasoning**, not as definitive evidence of cause-and-effect relationships.

---

## Communication Strategy

Results from later stages of this project will be communicated through multiple formats tailored to different stakeholders.

Planned communication channels include:

* A technical report or blog-style writeup explaining methodology and findings
* An interactive dashboard for exploratory analysis and scenario inspection
* Visual summaries highlighting major regime shifts and associated events

These formats are intended to support investors, policymakers, and energy companies in decision-making under uncertainty.

---

## Repository Structure

```
src/        Core analysis logic
notebooks/  Exploratory and step-by-step analysis
tests/      Unit tests
data/
  raw/      Original Brent oil price data
  processed/Structured event dataset
```

The repository follows standard data science best practices, with a clear separation between raw data, processing logic, exploratory analysis, and tests.

---

## Usage (Task 1)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Task 1 pipeline:

```bash
python src/initial_analysis.py
```

This executes:

* Data loading and validation
* Time series diagnostics and visualizations
* Event dataset compilation and export

The primary exploratory workflow is also documented in the accompanying notebook:

```
notebooks/initial_analysis.ipynb
```

---

## Next Steps

Subsequent tasks will:

* Implement Bayesian change point detection using PyMC
* Quantify regime shifts in price behavior
* Associate detected changes with real-world events
* Deliver insights through an interactive Flask + React dashboard

Task 1 establishes the statistical, conceptual, and organizational foundation required for these advanced analyses.

---