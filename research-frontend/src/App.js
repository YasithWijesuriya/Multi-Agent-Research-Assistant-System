import React, { useState } from "react";
import axios from "axios";

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
    } catch (err) {
      console.error(err);
      alert("Error fetching report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>🤖 ResearchHub - AI Research Assistant</h1>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter research topic"
          style={{ padding: "0.5rem", width: "300px" }}
        />
        <button type="submit" style={{ padding: "0.5rem 1rem", marginLeft: "1rem" }}>
          {loading ? "Researching..." : "Start Research"}
        </button>
      </form>

      {report && (
        <div style={{ marginTop: "2rem" }}>
          <h2>📄 Final Research Report</h2>
          <pre style={{ whiteSpace: "pre-wrap", background: "#f0f0f0", padding: "1rem" }}>
            {report}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
