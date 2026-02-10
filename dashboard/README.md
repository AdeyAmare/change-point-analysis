# Brent Oil Dashboard

This folder contains a **full-stack dashboard** for exploring Brent oil price data. The dashboard provides a **4-point analysis** combining raw prices, Bayesian change points, geopolitical events, and an integrated view.

It is organized into two main parts:

```
dashboard/
├─ backend/   # Flask API serving processed CSV data
└─ frontend/  # React-based interactive dashboard
```

---

## Overview

The dashboard presents **four main visual analyses**:

1. **Raw Price Trend** – Historical Brent oil prices over time.
2. **Statistical Change Points** – Probabilistic regime shifts in daily log returns detected via Bayesian modeling.
3. **Geopolitical Events** – Key events that may have affected oil prices.
4. **Integrated Analysis** – A combined visualization showing prices, change points, and events simultaneously.

The backend exposes APIs that the frontend consumes to display the visualizations. Users can filter the data by **start and end dates**.

---

## Folder Structure

### `backend/`

Contains a Flask application that serves processed CSV data via REST endpoints:

* `app.py` – Main Flask server with endpoints:

  * `/api/prices` – Returns Brent oil prices with optional date filtering.
  * `/api/change_point` – Returns change point results.
  * `/api/events` – Returns geopolitical events with optional date filtering.
* Processes CSVs from `data/processed/dashboard_data` and `data/raw`.

**Dependencies**:

* Flask
* Flask-CORS
* pandas

### `frontend/`

Contains a React application that visualizes the data:

* `App.jsx` – Main dashboard component.
* Uses **Recharts** for all plots:

  * `LineChart` for raw prices
  * `BarChart` for change points
  * `ScatterChart` for events
  * `ComposedChart` for integrated view
* Includes controls for **date filtering**.

**Dependencies**:

* React
* Recharts
* Axios

---

## Installation

### Backend

1. Navigate to the `backend` folder:

```bash
cd dashboard/backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install flask flask-cors pandas
```

4. Ensure the CSV files exist in:

```
data/raw/BrentOilPrices.csv
data/processed/dashboard_data/change_point_results.csv
data/processed/geopolitical_events.csv
```

5. Run the Flask server:

```bash
python app.py
```

The server runs on `http://0.0.0.0:5000` by default.

---

### Frontend

1. Navigate to the `frontend` folder:

```bash
cd dashboard/frontend
```

2. Install Node dependencies:

```bash
npm install
```

3. (Optional) Set a custom backend URL in `.env`:

```
REACT_APP_API_BASE_URL=http://localhost:5000
```

4. Start the React development server:

```bash
npm start
```

The dashboard will open in the browser at `http://localhost:3000`.

---

## Using the Dashboard

### 1. Date Filtering

At the top, you can select:

* **Start date** – Earliest date for the analysis.
* **End date** – Latest date for the analysis.

Click **Run Analysis** to fetch filtered data from the backend and update the plots.

---

### 2. Visualizations

**Plot 1: Raw Price Trend**

* Displays Brent oil prices over time.
* Line plot shows trends and fluctuations.

**Plot 2: Statistical Change Points**

* Highlights detected regime shifts.
* Vertical bars represent the most probable change point(s) in log returns.

**Plot 3: Geopolitical Events**

* Plots key events that could impact oil prices.
* Events are labeled on the y-axis and aligned with dates on the x-axis.

**Plot 4: Integrated Analysis**

* Combines prices, change points, and events into a single chart.
* Change points appear as dashed red lines.
* Events appear as yellow vertical markers.
* Provides a holistic view of data trends and historical context.

---

### 3. Interactive Features

* Hover over plots to see **tooltips** with precise values and dates.
* Zoom in and filter by date to focus on a specific period.
* Date filters automatically update all four charts simultaneously.

---

## Output and Data

The dashboard relies on three main CSV datasets:

1. **Brent Oil Prices (`BrentOilPrices.csv`)**

   * Columns: `Date`, `Price`
   * Used for raw price trends and log return calculations.

2. **Change Point Results (`change_point_results.csv`)**

   * Columns: `tau_index`, `change_date`, `mean_log_return_before`, `mean_log_return_after`, `percentage_change`
   * Represents Bayesian-identified structural shifts.

3. **Geopolitical Events (`geopolitical_events.csv`)**

   * Columns: `event_date`, `event_name`, `description`
   * Provides context for structural shifts in the oil market.

All plots are derived from these sources. Date filtering is applied dynamically in the backend.

---

## Backend API Endpoints

| Endpoint            | Method | Description                           | Query Params              |
| ------------------- | ------ | ------------------------------------- | ------------------------- |
| `/api/prices`       | GET    | Returns Brent oil prices              | `start`, `end` (optional) |
| `/api/change_point` | GET    | Returns Bayesian change point results | None                      |
| `/api/events`       | GET    | Returns geopolitical events           | `start`, `end` (optional) |

**Response Format**: JSON array of objects, with dates in `YYYY-MM-DD` format.

---

## Logging and Error Handling

* All backend operations are logged with timestamps.
* Errors in data fetching or CSV reading return informative messages.
* Frontend displays an alert if fetching fails.

---

## Notes

* Ensure all CSV files are **up-to-date and formatted correctly**.
* Integrated analysis requires both change point and events datasets; missing files will still display available data but leave markers empty.
* The dashboard is **responsive** and should work across standard desktop resolutions.


