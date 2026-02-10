from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from pathlib import Path
import csv

app = Flask(__name__)

# Allow React dev server (Vite = 5173)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --------------------------------------------------
# Paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DASHBOARD_DATA_DIR = DATA_DIR / "dashboard_data"

PRICE_CSV = DATA_RAW_DIR / "BrentOilPrices.csv"
CHANGE_POINT_CSV = DASHBOARD_DATA_DIR / "change_point_results.csv"
EVENTS_CSV = DATA_DIR / "geopolitical_events.csv"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def filter_by_date(df, start=None, end=None, date_col="Date"):
    """Filters dataframe by date range safely."""
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

def safe_json_response(df):
    """Handles NaN values and Timestamps that normally break jsonify."""
    # Convert datetime columns to string (ISO format)
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    
    # Replace NaN/NaT with None for JSON null
    data = df.replace({pd.NA: None}).where(pd.notnull(df), None).to_dict(orient="records")
    return jsonify(data)


# --------------------------------------------------
# API Endpoints
# --------------------------------------------------
@app.route("/api/prices", methods=["GET"])
def get_prices():
    if not PRICE_CSV.exists():
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
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@app.route("/api/change_point", methods=["GET"])
def get_change_point():
    if not CHANGE_POINT_CSV.exists():
        return jsonify({"error": "Change point CSV not found"}), 404

    try:
        df = pd.read_csv(CHANGE_POINT_CSV)
        df["change_date"] = pd.to_datetime(df["change_date"], errors="coerce")
        df = df.dropna(subset=["change_date"])

        return safe_json_response(df)
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@app.route("/api/events", methods=["GET"])
def get_events():
    if not EVENTS_CSV.exists():
        return jsonify({"error": f"Events CSV not found at {EVENTS_CSV}"}), 404

    try:
        # FIX: Added on_bad_lines and quoting to handle extra commas in CSV
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
        # This catch prevents the CORS error by returning a proper JSON response
        return jsonify({"error": f"Data processing error: {str(e)}"}), 500


# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)