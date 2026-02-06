# `tests` — Unit Tests

This folder contains **unit tests for the `src` package**, ensuring that the Brent oil analysis code functions correctly and handles edge cases.

---

## Test File

### `initial_analysis_tests.py`

This test suite uses **pytest** to validate the functionality of the `BrentOilAnalysisFoundation` class in `src.initial_analysis`:

* **CSV Loading**

  * Verifies that valid Brent oil CSV files are loaded correctly.
  * Checks that missing files raise `FileNotFoundError`.
  * Ensures missing required columns raise `ValueError`.

* **Time Series Diagnostics**

  * Ensures `check_stationarity` raises a `ValueError` if the required `'log_price'` column is missing.

* **Event Data**

  * Validates that the structured events DataFrame is created correctly.
  * Checks that saving the events dataset writes the file as expected.

---

## Usage

Run the tests with **pytest** from the project root:

```bash
pytest tests/
```

or for detailed output:

```bash
pytest -v tests/
```

---

## Features

* **Edge Case Coverage**: Tests missing files, missing columns, and invalid inputs.
* **File System Isolation**: Uses `tmp_path` fixtures for temporary file creation.
* **Data Validation**: Ensures DataFrames have expected columns and structure.
* **Integration Check**: Confirms that events are correctly saved to disk.

---

