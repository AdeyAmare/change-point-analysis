import logging
from typing import Optional, Tuple, Dict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class BrentOilChangePointAnalysis:
    """
    Bayesian change point detection on Brent oil prices (Task 2 compliant,
    optimized for large datasets).
    """

    def __init__(self, csv_path: str, events_csv: Optional[str] = None) -> None:
        self.csv_path = csv_path
        self.events_csv = events_csv
        self.data: Optional[pd.DataFrame] = None
        self.log_returns: Optional[np.ndarray] = None
        self.model: Optional[pm.Model] = None
        self.trace: Optional[az.InferenceData] = None
        self.tau_posterior: Optional[np.ndarray] = None
        self.events: Optional[pd.DataFrame] = None

    # -------------------------
    # Data Preparation & EDA
    # -------------------------
    def load_and_prepare_data(self) -> None:
        logging.info("Loading and preparing data.")

        self.data = pd.read_csv(self.csv_path)
        if {"Date", "Price"} - set(self.data.columns):
            raise ValueError("CSV must contain Date and Price columns.")

        self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce", format="mixed")
        self.data = self.data.dropna().sort_values("Date").reset_index(drop=True)

        # ---- PERFORMANCE FIX ----
        self.data = self.data.iloc[::5].reset_index(drop=True)

        # Daily log returns
        self.data["LogPrice"] = np.log(self.data["Price"])
        self.data["LogReturn"] = self.data["LogPrice"].diff()

        self.log_returns = self.data["LogReturn"].dropna().values

        logging.info(
            f"Prepared {len(self.log_returns)} daily log-return observations "
            f"after thinning."
        )

    def plot_price_series(self, overlay_tau: bool = False) -> None:
        plt.figure(figsize=(12, 5))
        plt.plot(self.data["Date"], self.data["Price"], label="Price")
        if overlay_tau and self.tau_posterior is not None:
            tau_idx = int(np.median(self.tau_posterior))
            plt.axvline(self.data["Date"].iloc[tau_idx + 1], color='red', linestyle='--', label='Change Point')
        plt.title("Brent Oil Price (USD per Barrel)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    def plot_log_returns(self) -> None:
        plt.figure(figsize=(12, 5))
        plt.plot(self.data["Date"].iloc[1:], self.log_returns)
        plt.title("Daily Log Returns of Brent Oil Prices")
        plt.xlabel("Date")
        plt.ylabel("Log Return")
        plt.show()

    # -------------------------
    # Bayesian Change Point Model
    # -------------------------
    def build_and_run_model(
        self,
        draws: int = 1000,
        tune: int = 1000,
        chains: int = 4,
        target_accept: float = 0.9,
        seed: int = 42
    ) -> None:

        if self.log_returns is None:
            raise RuntimeError("Prepare data before modeling.")

        logging.info("Building Bayesian change point model.")

        n = len(self.log_returns)
        time_index = np.arange(n)

        with pm.Model() as model:

            # Narrow tau prior to middle 60% of series for faster convergence
            tau = pm.DiscreteUniform("tau", lower=int(0.2*n), upper=int(0.8*n))

            mu_1 = pm.Normal("mu_1", mu=0.0, sigma=0.01)
            mu_2 = pm.Normal("mu_2", mu=0.0, sigma=0.01)
            sigma = pm.HalfNormal("sigma", sigma=0.05)


            mu = pm.math.switch(time_index < tau, mu_1, mu_2)
            pm.Normal("obs", mu=mu, sigma=sigma, observed=self.log_returns)

            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                target_accept=target_accept,
                random_seed=seed,
                return_inferencedata=True,
                progressbar=True
            )

        self.model = model
        self.tau_posterior = self.trace.posterior["tau"].values.flatten()

        logging.info("Sampling completed.")


    # -------------------------
    # Diagnostics
    # -------------------------
    def check_convergence(self) -> None:
        summary = az.summary(self.trace)
        print(summary)
        az.plot_trace(self.trace)
        plt.show()

    # -------------------------
    # Interpretation
    # -------------------------
    def plot_tau_posterior(self) -> None:
        plt.figure(figsize=(10, 4))
        plt.hist(self.tau_posterior, bins=40, density=True)
        plt.title("Posterior Distribution of Change Point (tau)")
        plt.xlabel("Time Index")
        plt.ylabel("Density")
        plt.show()

    def plot_mu_posteriors(self) -> None:
        mu1_samples = self.trace.posterior["mu_1"].values.flatten()
        mu2_samples = self.trace.posterior["mu_2"].values.flatten()
        plt.figure(figsize=(10, 5))
        plt.hist(mu1_samples, bins=50, alpha=0.6, label="mu_1 (Before)")
        plt.hist(mu2_samples, bins=50, alpha=0.6, label="mu_2 (After)")
        plt.title("Posterior Distributions of Mean Log Returns")
        plt.xlabel("Log Return")
        plt.ylabel("Density")
        plt.legend()
        plt.show()

    def get_change_point_date(self) -> Tuple[int, pd.Timestamp]:
        tau_median = int(np.median(self.tau_posterior))
        change_date = self.data["Date"].iloc[tau_median + 1]
        return tau_median, change_date

    def quantify_impact(self) -> Dict[str, float]:
        mu1 = self.trace.posterior["mu_1"].values.flatten().mean()
        mu2 = self.trace.posterior["mu_2"].values.flatten().mean()
        pct_change = ((np.exp(mu2) - np.exp(mu1)) / np.exp(mu1)) * 100
        return {
            "mean_log_return_before": mu1,
            "mean_log_return_after": mu2,
            "percentage_change": pct_change
        }

    # -------------------------
    # Event Association
    # -------------------------
    def load_events(self) -> None:
        if self.events_csv:
            self.events = pd.read_csv(self.events_csv)
            self.events["event_date"] = pd.to_datetime(self.events["event_date"])
            self.events = self.events.sort_values("event_date").reset_index(drop=True)
            logging.info("Loaded %d events from CSV.", len(self.events))
        else:
            logging.warning("No events CSV provided; event association skipped.")
            self.events = pd.DataFrame(columns=["event_date", "event_name", "description"])

    def associate_change_point_with_event(self) -> Optional[pd.Series]:
        if self.events is None:
            self.load_events()

        _, change_date = self.get_change_point_date()
        # Find closest event prior to or on the change date
        prior_events = self.events[self.events["event_date"] <= change_date]
        if prior_events.empty:
            return None
        closest_event = prior_events.iloc[-1]
        return closest_event

    def save_results_for_dashboard(self, price_path: str = "brent_prices.csv", change_point_path: str = "change_point_results.csv") -> None:
        """
        Save Task 2 outputs in CSV files for use in Task 3 dashboard.
        Creates directories automatically if they do not exist.
        """
        if self.data is None or self.tau_posterior is None:
            raise RuntimeError("Task 2 results not available. Run the full analysis first.")

        # Ensure directories exist for price_path
        price_dir = os.path.dirname(price_path)
        if price_dir and not os.path.exists(price_dir):
            os.makedirs(price_dir)
            logging.info(f"Created directory {price_dir} for price CSV.")

        # Ensure directories exist for change_point_path
        cp_dir = os.path.dirname(change_point_path)
        if cp_dir and not os.path.exists(cp_dir):
            os.makedirs(cp_dir)
            logging.info(f"Created directory {cp_dir} for change point CSV.")

        # Save historical prices
        self.data[['Date', 'Price']].to_csv(price_path, index=False)
        logging.info(f"Historical prices saved to {price_path}")

        # Save change point summary
        tau_idx, change_date = self.get_change_point_date()
        impact = self.quantify_impact()
        
        cp_results = pd.DataFrame({
            'tau_index': [tau_idx],
            'change_date': [str(change_date.date())],
            'mean_log_return_before': [impact['mean_log_return_before']],
            'mean_log_return_after': [impact['mean_log_return_after']],
            'percentage_change': [impact['percentage_change']]
        })
        cp_results.to_csv(change_point_path, index=False)
        logging.info(f"Change point results saved to {change_point_path}")

    # -------------------------
    # Full Pipeline
    # -------------------------
    def run_full_analysis(self) -> None:
        self.load_and_prepare_data()
        self.plot_price_series()
        self.plot_log_returns()
        self.build_and_run_model()
        self.check_convergence()
        self.plot_tau_posterior()
        self.plot_mu_posteriors()
        self.plot_price_series(overlay_tau=True)

        tau_idx, date = self.get_change_point_date()
        impact = self.quantify_impact()

        print(
            f"\nChange point detected around {date.date()}.\n"
            f"Mean daily log return shifted from "
            f"{impact['mean_log_return_before']:.5f} to "
            f"{impact['mean_log_return_after']:.5f}, "
            f"representing a {impact['percentage_change']:.2f}% change."
        )

        event = self.associate_change_point_with_event()
        if event is not None:
            print(
                f"Closest relevant event prior to change point:\n"
                f"{event['event_name']} on {event['event_date'].date()}: {event['description']}"
            )
        else:
            print("No relevant event found near the change point.")
