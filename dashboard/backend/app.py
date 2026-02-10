from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from pathlib import Path
import csv
import logging
from typing import Optional

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# Flask App Setup
# -------------------------
app = Flask(__name__)
# Allow React dev server (Vite default port = 5173)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# -------------------------
# Paths
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DASHBOARD_DATA_DIR = DATA_DIR / "dashboard_data"

PRICE_CSV = DATA_RAW_DIR / "BrentOilPrices.csv"
CHANGE_POINT_CSV = DASHBOARD_DATA_DIR / "change_point_results.csv"
EVENTS_CSV = DATA_DIR / "geopolitical_events.csv"

# -------------------------
# Helper Functions
# -------------------------
def filter_by_date(
    df: pd.DataFrame, 
    start: Optional[str] = None, 
    end: Optional[str] = None, 
    date_col: str = "Date"
) -> pd.DataFrame:
    """
    Filter a dataframe by a date range safely.

    Args:
        df (pd.DataFrame): Input dataframe containing a date column.
        start (Optional[str]): Start date (inclusive). Format: YYYY-MM-DD or any parseable string.
        end (Optional[str]): End date (inclusive). Format: YYYY-MM-DD or any parseable string.
        date_col (str): Column name containing dates.

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="mixed")

    if start:
        start_ts = pd.to_datetime(start, errors="coerce", format="mixed")
        if pd.notnull(start_ts):
            df = df[df[date_col] >= start_ts]

    if end:
        end_ts = pd.to_datetime(end, errors="coerce", format="mixed")
        if pd.notnull(end_ts):
            df = df[df[date_col] <= end_ts]

    return df

def safe_json_response(df: pd.DataFrame):
    """
    Convert dataframe to JSON-friendly format.
    - Converts datetime columns to ISO strings
    - Converts NaN/NaT to None

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        Response: Flask JSON response.
    """
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')

    data = df.replace({pd.NA: None}).where(pd.notnull(df), None).to_dict(orient="records")
    return jsonify(data)

# -------------------------
# API Endpoints
# -------------------------
@app.route("/api/prices", methods=["GET"])
def get_prices():
    """
    Get Brent oil prices, optionally filtered by start and end date query params.
    Query params:
        start (str): optional, start date
        end (str): optional, end date
    """
    if not PRICE_CSV.exists():
        logging.error(f"Price CSV not found: {PRICE_CSV}")
        return jsonify({"error": "Price CSV not found"}), 404

    try:
        df = pd.read_csv(PRICE_CSV)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        start = request.args.get("start")
        end = request.args.get("end")
        df = filter_by_date(df, start, end, "Date")

        return safe_json_response(df)
    except Exception as e:
        logging.exception("Error while processing /api/prices")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route("/api/change_point", methods=["GET"])
def get_change_point():
    """
    Get change point results from CSV.
    """
    if not CHANGE_POINT_CSV.exists():
        logging.error(f"Change point CSV not found: {CHANGE_POINT_CSV}")
        return jsonify({"error": "Change point CSV not found"}), 404

    try:
        df = pd.read_csv(CHANGE_POINT_CSV)
        df["change_date"] = pd.to_datetime(df["change_date"], errors="coerce")
        df = df.dropna(subset=["change_date"])

        return safe_json_response(df)
    except Exception as e:
        logging.exception("Error while processing /api/change_point")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route("/api/events", methods=["GET"])
def get_events():
    """
    Get geopolitical events, optionally filtered by start and end date query params.
    Handles CSV parsing issues with extra commas.
    """
    if not EVENTS_CSV.exists():
        logging.error(f"Events CSV not found: {EVENTS_CSV}")
        return jsonify({"error": f"Events CSV not found at {EVENTS_CSV}"}), 404

    try:
        df = pd.read_csv(
            EVENTS_CSV,
            on_bad_lines='warn',
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"'
        )
        df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
        df = df.dropna(subset=["event_date"])

        start = request.args.get("start")
        end = request.args.get("end")
        df = filter_by_date(df, start, end, "event_date")

        return safe_json_response(df)
    except Exception as e:
        logging.exception("Error while processing /api/events")
        return jsonify({"error": f"Data processing error: {str(e)}"}), 500

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    logging.info("Starting Flask server on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
