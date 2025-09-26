import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [logs, setLogs] = useState([]);
  const [filters, setFilters] = useState({
    level: "",
    message: "",
    resourceId: "",
    startDate: "",
    endDate: "",
    traceId: "",
    spanId: "",
    commit: "",
    "metadata.parentResourceId": "",
    prediction: "",
  });

  // Fetch logs
  const fetchLogs = useCallback(async () => {
    try {
      const params = new URLSearchParams();
      for (const key in filters) {
        if (filters[key]) {
          params.append(key, filters[key]);
        }
      }
      const response = await axios.get(
        `https://log-ingestor-project-12345.el.r.appspot.com/logs?${params.toString()}`
      );
      setLogs(response.data);
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  }, [filters]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  // Handle filter change
  const handleFilterChange = (e) => {
    const { name, value, type } = e.target;
    if (type === "date" && value) {
      const isoValue = new Date(value).toISOString();
      setFilters((prev) => ({ ...prev, [name]: isoValue }));
    } else {
      setFilters((prev) => ({ ...prev, [name]: value }));
    }
  };

  // Reset filters
  const resetFilters = () => {
    setFilters({
      level: "",
      message: "",
      resourceId: "",
      startDate: "",
      endDate: "",
      traceId: "",
      spanId: "",
      commit: "",
      "metadata.parentResourceId": "",
      prediction: "",
    });
  };

  return (
    <div className="App">
      <div className="header">
  <h1 className="main-title">Log Ingestor & Query Interface</h1>
</div>

      {/* Search filters */}
      <div className="filter-container">
        <input
          name="level"
          value={filters.level}
          onChange={handleFilterChange}
          placeholder="Level (e.g., error)"
        />
        <input
          name="message"
          value={filters.message}
          onChange={handleFilterChange}
          placeholder="Message text search"
        />
        <input
          name="resourceId"
          value={filters.resourceId}
          onChange={handleFilterChange}
          placeholder="Resource ID"
        />

        {/* Date Filters */}
        <input
          type="date"
          name="startDate"
          onChange={handleFilterChange}
          placeholder="Start Date"
        />
        <input
          type="date"
          name="endDate"
          onChange={handleFilterChange}
          placeholder="End Date"
        />

        <input
          name="traceId"
          value={filters.traceId}
          onChange={handleFilterChange}
          placeholder="Trace ID"
        />
        <input
          name="spanId"
          value={filters.spanId}
          onChange={handleFilterChange}
          placeholder="Span ID"
        />
        <input
          name="commit"
          value={filters.commit}
          onChange={handleFilterChange}
          placeholder="Commit hash"
        />
        <input
          name="metadata.parentResourceId"
          value={filters["metadata.parentResourceId"]}
          onChange={handleFilterChange}
          placeholder="Parent Resource ID"
        />
        <input
          name="prediction"
          value={filters.prediction}
          onChange={handleFilterChange}
          placeholder="Prediction (anomaly/normal)"
        />
      </div>

      {/* Centered Reset Button */}
      <div className="reset-container">
        <button onClick={resetFilters} className="reset-btn">
          Reset Filters
        </button>
      </div>

      {/* Logs Table */}
      <div className="log-display">
        <table>
          <thead>
            <tr>
              <th>Level</th>
              <th>Message</th>
              <th>Resource ID</th>
              <th>Timestamp</th>
              <th>Trace ID</th>
              <th>Span ID</th>
              <th>Commit</th>
              <th>Parent Resource ID</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log._id}>
                <td>{log.level}</td>
                <td>{log.message}</td>
                <td>{log.resourceId}</td>
                <td>
                  {log.timestamp
                    ? new Date(log.timestamp).toLocaleString()
                    : "-"}
                </td>
                <td>{log.traceId}</td>
                <td>{log.spanId}</td>
                <td>{log.commit}</td>
                <td>{log.metadata?.parentResourceId}</td>
                <td>
                  <span className={`prediction ${log.prediction}`}>
                    {log.prediction}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
