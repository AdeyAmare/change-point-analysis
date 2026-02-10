import React, { useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer,
  BarChart, Bar, ScatterChart, Scatter, LabelList, ReferenceLine, ComposedChart
} from "recharts";
import axios from "axios";

function App() {
  const [prices, setPrices] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [events, setEvents] = useState([]);
  const [dateRange, setDateRange] = useState({ start: "", end: "" });

  const fetchData = async () => {
    try {
      const [pRes, cpRes, eRes] = await Promise.all([
        axios.get("http://localhost:5000/api/prices", { params: dateRange }),
        axios.get("http://localhost:5000/api/change_point"),
        axios.get("http://localhost:5000/api/events", { params: dateRange })
      ]);

      setPrices(pRes.data.map(p => ({ ...p, Date: new Date(p.Date).getTime() })));
      setChangePoints(cpRes.data.map(cp => ({ ...cp, change_date: new Date(cp.change_date).getTime() })));
      setEvents(eRes.data.map(e => ({ ...e, event_date: new Date(e.event_date).getTime() })));
    } catch (err) {
      console.error("Fetch Error:", err);
    }
  };

  const formatDate = (ts) => ts ? new Date(ts).toLocaleDateString() : "";

  return (
    // Changed padding to 15px and width to 100% to maximize space
    <div style={{
      padding: "15px",
      backgroundColor: "#0f172a",
      color: "#f1f5f9",
      minHeight: "100vh",
      width: "100vw",
      boxSizing: "border-box"
    }}>
      {/* Reduced bottom margin on header */}
      <h2 style={{ textAlign: 'center', color: '#38bdf8', margin: "0 0 15px 0" }}>
        Brent Oil: 4-Point Analysis Dashboard
      </h2>

      {/* Reduced bottom margin on controls */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', marginBottom: '15px' }}>
        <input type="date" name="start" value={dateRange.start} onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })} />
        <input type="date" name="end" value={dateRange.end} onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })} />
        <button onClick={fetchData} style={{ padding: '5px 20px', backgroundColor: '#38bdf8', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>
          Run Analysis
        </button>
      </div>

      {/* Grid container spanning full width with reduced gap */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "15px",
        width: "100%"
      }}>

        {/* PLOT 1 */}
        <div style={{ background: '#1e293b', padding: '10px', borderRadius: '8px' }}>
          <h4 style={{ margin: "0 0 10px 0" }}>1. Raw Price Trend</h4>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={prices}>
              <CartesianGrid stroke="#334155" />
              <XAxis dataKey="Date" type="number" domain={['dataMin', 'dataMax']} tickFormatter={formatDate} hide />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip labelFormatter={formatDate} contentStyle={{ backgroundColor: '#1e293b', border: 'none' }} />
              <Line type="monotone" dataKey="Price" stroke="#38bdf8" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* PLOT 2 */}
        <div style={{ background: '#1e293b', padding: '10px', borderRadius: '8px' }}>
          <h4 style={{ margin: "0 0 10px 0" }}>2. Statistical Change Points</h4>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={changePoints}>
              <CartesianGrid stroke="#334155" />
              <XAxis dataKey="change_date" type="number" domain={['dataMin', 'dataMax']} tickFormatter={formatDate} hide />
              <YAxis hide />
              <Tooltip labelFormatter={formatDate} />
              <Bar dataKey="change_date" fill="#f43f5e" barSize={5} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* PLOT 3 */}
        <div style={{ background: '#1e293b', padding: '10px', borderRadius: '8px' }}>
          <h4 style={{ margin: "0 0 10px 0" }}>3. Geopolitical Events</h4>
          <ResponsiveContainer width="100%" height={220}>
            <ScatterChart>
              <CartesianGrid stroke="#334155" />
              <XAxis dataKey="event_date" type="number" domain={['dataMin', 'dataMax']} tickFormatter={formatDate} hide />
              <YAxis dataKey="event_name" type="category" width={1} tick={false} axisLine={false} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} labelFormatter={formatDate} />
              <Scatter data={events} fill="#fbbf24">
                <LabelList dataKey="event_name" position="top" style={{ fill: '#fbbf24', fontSize: '10px' }} />
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        {/* PLOT 4 */}
        <div style={{ background: '#1e293b', padding: '10px', borderRadius: '8px', border: '1px solid #38bdf8' }}>
          <h4 style={{ color: '#38bdf8', margin: "0 0 10px 0" }}>4. Integrated Analysis (Combined)</h4>
          <ResponsiveContainer width="100%" height={220}>
            <ComposedChart data={prices}>
              <CartesianGrid stroke="#334155" />
              <XAxis dataKey="Date" type="number" domain={['dataMin', 'dataMax']} tickFormatter={formatDate} stroke="#94a3b8" fontSize={10} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip labelFormatter={formatDate} />
              <Line type="monotone" dataKey="Price" stroke="#38bdf8" dot={false} strokeWidth={2} />
              {changePoints.map((cp, i) => (
                <ReferenceLine key={`cp-${i}`} x={cp.change_date} stroke="#f43f5e" strokeDasharray="3 3" />
              ))}
              {events.map((e, i) => (
                <ReferenceLine key={`ev-${i}`} x={e.event_date} stroke="#fbbf24" strokeOpacity={0.5} />
              ))}
            </ComposedChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
}

export default App;