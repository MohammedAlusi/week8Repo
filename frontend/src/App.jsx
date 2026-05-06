import { useEffect, useState } from "react";

function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getLogs = async () => {
    try {
      const res = await fetch("/api/logs");
      const data = await res.json();
      setLogs(data);
    } catch (e) {
      setError("Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  const sendLog = async () => {
    await fetch("/api/logs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Failed login from 192.168.1.100" })
    });
    getLogs();
  };

  useEffect(() => { getLogs(); }, []);

  return (
    <div style={{ minHeight: "100vh", background: "#0a0e27", color: "#e0e6ff", fontFamily: "monospace", padding: "24px" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <h1 style={{ color: "#00f0ff", fontSize: 28, marginBottom: 8 }}>Cyber Logs Dashboard</h1>
        <button onClick={sendLog} style={{ border: "2px solid #00f0ff", background: "transparent", color: "#00f0ff", padding: "10px 24px", borderRadius: 6, cursor: "pointer", marginBottom: 24 }}>
          + Send Test Log
        </button>
        {error && <p style={{ color: "#ff0080" }}>{error}</p>}
        {loading ? <p style={{ color: "#8892b0" }}>Loading...</p> : logs.length === 0 ? (
          <p style={{ color: "#8892b0" }}>No logs yet.</p>
        ) : (
          <div>
            {logs.map((log, i) => (
              <div key={i} style={{ background: "#1a1f3a", borderRadius: 8, padding: 14, marginBottom: 10, borderLeft: "4px solid #00f0ff" }}>
                <strong style={{ color: "#00f0ff" }}>{log.source_ip || "Unknown"}</strong> - {log.event_type} - {log.severity}
                <div style={{ color: "#8892b0", fontSize: 12 }}>{log.created_at}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
