# `tests` — Unit Tests

This folder contains **unit tests for the `src` package**, ensuring that the Brent oil analysis code functions correctly, handles edge cases, and produces reliable outputs.

It now includes tests for both:

* **`initial_analysis`** (basic data loading, diagnostics, and event compilation)
* **`change_point_analysis`** (Bayesian change point modeling of Brent oil prices)

---

## Test Files

### `initial_analysis_tests.py`

Validates the `BrentOilAnalysisFoundation` class in `src.initial_analysis`:

* **CSV Loading**

  * Correctly loads valid Brent oil CSV files.
  * Raises `FileNotFoundError` if file is missing.
  * Raises `ValueError` if required columns are missing.

* **Time Series Diagnostics**

  * Ensures `check_stationarity` raises an error if `'log_price'` column is missing.

* **Event Data**

  * Validates that the structured events DataFrame is created correctly.
  * Confirms that saving the events dataset writes the file properly.

---

### `test_change_point_analysis.py`

Validates the `BrentOilChangePointAnalysis` class in `src.change_point_analysis`:

* **CSV Loading & Preparation**

  * Loads valid CSV files and computes log returns.
  * Handles missing files (`FileNotFoundError`), missing columns (`ValueError`), and empty CSVs gracefully.

* **Data Integrity**

  * Ensures `log_returns` is a NumPy array of the expected length.
  * Verifies that empty input data produces empty log returns without crashing.

* **Model Handling**

  * Raises `RuntimeError` if attempting to build or analyze the model before preparing data.
  * Ensures methods like `get_change_point_date` and `quantify_impact` raise errors when the posterior model is missing.

* **Event Association**

  * Confirms that `associate_change_point_with_event` returns `None` gracefully if no event data is provided.

* **Edge Cases & Robustness**

  * Tests minimal datasets.
  * Confirms graceful handling of invalid CSV formats.

---

## Usage

Run all tests from the project root with **pytest**:

```bash
pytest tests/
```

Or for detailed output:

```bash
pytest -v tests/
```

To run only change point tests:

```bash
pytest tests/test_change_point_analysis.py
```

---

## Features

* **Edge Case Coverage**: Missing files, empty CSVs, missing columns, invalid inputs.
* **Data Validation**: Ensures all processed arrays and DataFrames are of correct type and length.
* **Integration Checks**: Confirms that analysis classes can process input, run models, and associate events correctly.
* **File System Isolation**: Uses `tmp_path` fixtures for temporary CSV creation without modifying project data.
* **Error Handling Verification**: Confirms meaningful exceptions are raised when preconditions are unmet.

---

This updated test suite ensures **robustness and reliability** for all core functionalities in `src`, from initial data processing to Bayesian change point analysis and event integration.

