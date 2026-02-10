# Laying the Foundation for Change Point Analysis of Brent Oil Prices

## Introduction and Objective

Birhan Energies operates in an environment where oil price volatility creates significant uncertainty for investors, policymakers, and energy companies. Brent crude oil prices are highly sensitive to geopolitical conflicts, economic shocks, and policy decisions such as OPEC production adjustments or international sanctions. Understanding when and how these events lead to structural changes in oil prices is critical for informed decision-making, risk management, and strategic planning.

The objective of this task is to establish a strong analytical foundation for examining how major political and economic events relate to changes in Brent oil prices. This includes defining a clear data analysis workflow, understanding the statistical properties of the price series, compiling a structured dataset of relevant events, and clarifying assumptions and limitations that shape interpretation. This groundwork supports subsequent Bayesian change point modeling and insight generation.

## Data Analysis Workflow

The analysis workflow begins with data ingestion and validation, ensuring correct date formatting, numeric price values, and the absence of missing or duplicate observations. Once loaded, exploratory data analysis is conducted to visualize the raw price series and identify broad trends, extreme shocks, and periods of heightened volatility.

To better understand the statistical behavior of the series, log prices and log returns are examined. Log transformations help stabilize variance and allow clearer assessment of relative price changes over time. Stationarity tests and rolling statistics are applied to evaluate whether the series exhibits stable statistical properties or requires modeling approaches that explicitly account for regime changes.

Parallel to price analysis, a structured dataset of major geopolitical and economic events is compiled (CSV). This includes OPEC policy decisions, armed conflicts in oil-producing regions, global financial crises, and major sanctions affecting energy markets. Each event is recorded with an approximate start date and a concise description. This event dataset is used later to contextualize statistically detected change points.

Insights from exploratory analysis directly inform modeling choices, particularly the use of Bayesian change point models that allow parameters such as the mean or volatility of the series to shift over time.

## Structured Event Dataset (CSV)

| event_date | event_name                     | description                                   |
| ---------- | ------------------------------ | --------------------------------------------- |
| 1973-10-17 | Arab Oil Embargo               | OAPEC embargo causes supply shock.            |
| 1979-01-01 | Iranian Revolution             | Disruption of Iranian oil production.         |
| 1990-08-02 | Iraqi Invasion of Kuwait       | Severe supply disruption.                     |
| 1997-07-01 | Asian Financial Crisis         | Demand shock from collapsing Asian economies. |
| 2001-09-11 | September 11 Attacks           | Heightened geopolitical uncertainty.          |
| 2008-09-15 | Global Financial Crisis        | Sharp collapse in demand and prices.          |
| 2010-04-20 | Deepwater Horizon Spill        | Offshore production concerns.                 |
| 2014-11-27 | OPEC Maintains Production      | Market share over price support.              |
| 2016-11-30 | OPEC Production Cut Agreement  | Coordinated output cuts.                      |
| 2020-03-11 | COVID-19 Pandemic Declared     | Historic collapse in demand.                  |
| 2020-04-20 | Negative Oil Prices            | WTI prices below zero.                        |
| 2022-02-24 | Russian Invasion of Ukraine    | Sanctions and supply risks.                   |
| 2023-04-02 | OPEC+ Surprise Production Cuts | Unexpected cuts trigger price reaction.       |

> **Note:** This dataset includes **13 major events**, covering supply shocks, geopolitical crises, and major policy decisions. These events are recorded with approximate dates to contextualize detected change points in the price series.

---

## Time Series Properties and Their Implications

Initial exploration of the Brent oil price series reveals long-term trends, abrupt price shocks, and extended periods of elevated volatility. These features suggest that the series is non-stationary in its raw form, making traditional constant-parameter models unsuitable without transformation.

Log returns exhibit more stable behavior and reduced trend effects but still display volatility clustering, a common characteristic of financial time series. These observations motivate the use of models that can detect structural breaks rather than assuming a single stable regime across the full sample.

Understanding these properties is essential for selecting an appropriate modeling framework. Change point models are particularly well-suited to this context because they explicitly allow the statistical behavior of the series to shift in response to external forces.

## Change Point Models: Purpose and Expected Outputs

Change point models aim to identify points in time where the underlying data-generating process changes. In the context of Brent oil prices, these models help detect structural breaks corresponding to shifts in average price levels, volatility, or overall market behavior.

The expected outputs of change point analysis include posterior distributions over potential change point dates and estimates of model parameters before and after each detected break. These results allow probabilistic statements about when a structural shift likely occurred and how market behavior differed across regimes.

However, change point models identify when changes occur, not why they occur. Associating detected change points with real-world events requires careful contextual interpretation rather than direct causal claims.

## Assumptions and Limitations

This analysis assumes that Brent oil prices reasonably reflect global oil market dynamics and that major geopolitical or economic events are incorporated into prices within a relatively short time frame. In reality, market reactions may be delayed, anticipated in advance, or influenced by concurrent unrelated factors. The event dataset represents complex and often prolonged developments using approximate start dates, acknowledging that many events unfold over extended periods, involve multiple decisions, or overlap with other shocks. This introduces temporal uncertainty when associating specific events with detected structural changes.

The modeling framework assumes that price behavior can be segmented into regimes with distinct statistical properties, which simplifies real-world dynamics and does not fully capture nonlinear effects, feedback loops, or expectation-driven behavior. Crucially, detecting a change point near a known event indicates a plausible association rather than a causal relationship. Establishing causality would require additional variables or structural modeling beyond the scope of this task. Finally, the analysis focuses solely on price data and excludes other relevant factors, such as global demand indicators, exchange rates, inflation, or inventory levels, meaning that some detected changes may be driven by unobserved influences.

