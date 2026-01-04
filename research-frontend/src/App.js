import React, { useState } from "react";
import axios from "axios";
import "./App.css";


function App() {
  const [topic, setTopic] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topic) return alert("Please enter a topic");
    
    setLoading(true);
    setReport("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/research", { topic });
      setReport(res.data.report);
//!        Backend JSON response
//!              ↓
//!        res.data.report
//!              ↓
//!        setReport("final research text")
//!              ↓
//!        report state update

    } catch (err) {
      console.error(err);
      alert("Error fetching report");
    } finally {
      setLoading(false);
    }
  };

return (
    <div className="container">
      <div className="card">
        <h1>🤖 ResearchHub</h1>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter research topic"
          />

          <button type="submit" disabled={loading}>
            {loading ? "Researching..." : "Start Research"}
          </button>
        </form>

        {loading && <div className="spinner" />}

        {report && (
          <div className="report">
            <h2>📄 Final Research Report</h2>
            <pre>{report}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;


// User types topic
// ↓
// topic state update
// ↓
// Submit button
// ↓
// axios POST request
// ↓
// FastAPI endpoint (/research)
// ↓
// run_research(topic)
// ↓
// final report string
// ↓
// JSON response
// ↓
// axios receives response
// ↓
// setReport(report)
// ↓
// React re-render
// ↓
// Report shown on screen
