import pytest
import pandas as pd
from pathlib import Path
from tempfile import TemporaryDirectory
from src.initial_analysis import BrentOilAnalysisFoundation

# -------------------------------
# Fixtures
# -------------------------------

@pytest.fixture
def sample_csv(tmp_path):
    """Create a valid sample Brent CSV file."""
    df = pd.DataFrame({
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Price": [80.5, 81.2, 79.9]
    })
    file_path = tmp_path / "BrentOilPrices.csv"
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def missing_column_csv(tmp_path):
    """CSV missing the 'Price' column."""
    df = pd.DataFrame({
        "Date": ["2023-01-01", "2023-01-02"],
        "Value": [100, 101]
    })
    file_path = tmp_path / "bad.csv"
    df.to_csv(file_path, index=False)
    return file_path

# -------------------------------
# Tests
# -------------------------------

def test_load_brent_data_success(sample_csv, tmp_path):
    """Test loading valid Brent CSV."""
    output_path = tmp_path / "events.csv"
    foundation = BrentOilAnalysisFoundation(sample_csv, output_path)
    df = foundation.load_brent_data()
    assert isinstance(df, pd.DataFrame)
    assert "Price" in df.columns
    assert "Date" not in df.columns  # Date is index
    assert len(df) == 3

def test_load_brent_data_file_not_found(tmp_path):
    """Test loading a non-existent file raises FileNotFoundError."""
    foundation = BrentOilAnalysisFoundation(tmp_path / "nonexistent.csv", tmp_path / "events.csv")
    with pytest.raises(FileNotFoundError):
        foundation.load_brent_data()

def test_load_brent_data_missing_columns(missing_column_csv, tmp_path):
    """Test loading CSV missing required columns raises ValueError."""
    foundation = BrentOilAnalysisFoundation(missing_column_csv, tmp_path / "events.csv")
    with pytest.raises(ValueError):
        foundation.load_brent_data()

def test_check_stationarity_with_invalid_df(sample_csv, tmp_path):
    """Test that check_stationarity raises ValueError if 'log_price' missing."""
    output_path = tmp_path / "events.csv"
    foundation = BrentOilAnalysisFoundation(sample_csv, output_path)
    df = foundation.load_brent_data()
    # Drop log_price to simulate missing column
    df = df.copy()
    with pytest.raises(ValueError):
        foundation.check_stationarity(df)

def test_define_and_save_events(tmp_path):
    """Test events dataframe is created and saved correctly."""
    sample_file = tmp_path / "dummy.csv"
    pd.DataFrame({"Date": ["2023-01-01"], "Price": [80]}).to_csv(sample_file, index=False)
    output_file = tmp_path / "events.csv"
    foundation = BrentOilAnalysisFoundation(sample_file, output_file)
    events_df = foundation.define_relevant_events()
    assert isinstance(events_df, pd.DataFrame)
    assert "event_name" in events_df.columns
    foundation.save_events_dataset(events_df)
    assert output_file.exists()
    saved_df = pd.read_csv(output_file)
    assert len(saved_df) == len(events_df)
