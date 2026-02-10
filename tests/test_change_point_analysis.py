import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.change_point_analysis import BrentOilChangePointAnalysis  # adjust import if needed
import logging

# Configure logging for tests
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def valid_csv(tmp_path: Path):
    """Creates a valid CSV with Date and Price columns."""
    file_path = tmp_path / "prices.csv"
    df = pd.DataFrame({
        "Date": pd.date_range("2026-01-01", periods=5),
        "Price": [80, 82, 81, 83, 85]
    })
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def invalid_csv_missing_columns(tmp_path: Path):
    """Creates a CSV missing required columns."""
    file_path = tmp_path / "invalid.csv"
    df = pd.DataFrame({
        "Timestamp": pd.date_range("2026-01-01", periods=5),
        "Value": [80, 82, 81, 83, 85]
    })
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def empty_csv(tmp_path: Path):
    """Creates an empty CSV file."""
    file_path = tmp_path / "empty.csv"
    pd.DataFrame(columns=["Date", "Price"]).to_csv(file_path, index=False)
    return file_path

# -----------------------------
# Tests
# -----------------------------

def test_missing_csv_raises_file_not_found(tmp_path: Path):
    """Test that loading a non-existent CSV raises FileNotFoundError."""
    analysis = BrentOilChangePointAnalysis(csv_path=tmp_path / "does_not_exist.csv")
    with pytest.raises(FileNotFoundError):
        analysis.load_and_prepare_data()

def test_invalid_columns_raise_value_error(invalid_csv_missing_columns: Path):
    """Test that CSV missing 'Date' or 'Price' raises ValueError."""
    analysis = BrentOilChangePointAnalysis(csv_path=invalid_csv_missing_columns)
    with pytest.raises(ValueError):
        analysis.load_and_prepare_data()

def test_empty_csv_returns_no_log_returns(empty_csv: Path):
    """Test that an empty CSV results in empty log_returns array."""
    analysis = BrentOilChangePointAnalysis(csv_path=empty_csv)
    # Should not raise; it will log info but result in empty log_returns
    analysis.load_and_prepare_data()
    assert isinstance(analysis.log_returns, np.ndarray)
    assert len(analysis.log_returns) == 0

def test_load_and_prepare_data_creates_log_returns(valid_csv: Path):
    """Check that valid CSV produces correct log_returns array type and length."""
    analysis = BrentOilChangePointAnalysis(csv_path=valid_csv)
    analysis.load_and_prepare_data()
    assert isinstance(analysis.log_returns, np.ndarray)
    # After thinning (every 5th row) and diff(), there should be len-1 entries
    expected_len = max(len(pd.read_csv(valid_csv)) // 5 - 1, 0)
    assert len(analysis.log_returns) == expected_len

def test_build_model_without_data_raises_runtime_error(valid_csv: Path):
    """Check error is raised if model is run before data preparation."""
    analysis = BrentOilChangePointAnalysis(csv_path=valid_csv)
    with pytest.raises(RuntimeError):
        analysis.build_and_run_model(draws=10, tune=10)  # small draws for test

def test_associate_change_point_with_no_events(valid_csv: Path):
    """Ensure that no events CSV returns None gracefully."""
    analysis = BrentOilChangePointAnalysis(csv_path=valid_csv)
    analysis.load_and_prepare_data()
    analysis.build_and_run_model(draws=10, tune=10, chains=1)
    event = analysis.associate_change_point_with_event()
    # Should be None if no events CSV provided
    assert event is None

def test_get_change_point_date_without_model(valid_csv: Path):
    """Check error raised if tau posterior is missing."""
    analysis = BrentOilChangePointAnalysis(csv_path=valid_csv)
    analysis.load_and_prepare_data()
    with pytest.raises(RuntimeError):
        analysis.get_change_point_date()

def test_quantify_impact_without_model(valid_csv: Path):
    """Check error raised if posterior trace is missing."""
    analysis = BrentOilChangePointAnalysis(csv_path=valid_csv)
    analysis.load_and_prepare_data()
    with pytest.raises(RuntimeError):
        analysis.quantify_impact()
