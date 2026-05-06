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
      setError(null);
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

  const getSeverityColor = (severity) => {
    switch ((severity || "").toLowerCase()) {
      case "critical": return "#ff0080";
      case "high": return "#ff4444";
      case "medium": return "#ffaa00";
      case "low": return "#00ff41";
      default: return "#00f0ff";
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0a0e27", color: "#e0e6ff", fontFamily: "monospace", padding: "24px" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <h1 style={{ color: "#00f0ff", fontSize: 28, marginBottom: 8, textShadow: "0 0 20px rgba(0,240,255,0.5)" }}>
          🛡️ Cyber Logs Dashboard
        </h1>
        <p style={{ color: "#8892b0", marginBottom: 24 }}>Real-time security monitoring</p>
        <button
          onClick={sendLog}
          style={{
            background: "transparent", border: "2px solid #00f0ff", color: "#00f0ff",
            padding: "10px 24px", borderRadius: 6, cursor: "pointer", marginBottom: 24,
            fontFamily: "monospace", fontSize: 14, fontWeight: "bold",
            boxShadow: "0 0 15px rgba(0,240,255,0.3)"
          }}
        >
          + Send Test Log
        </button>
        {error && <p style={{ color: "#ff0080", marginBottom: 16 }}>Error: {error}</p>}
        {loading ? (
          <p style={{ color: "#8892b0" }}>Loading logs...</p>
        ) : logs.length === 0 ? (
          <p style={{ color: "#8892b0" }}>No logs yet. Click Send Test Log to add one.</p>
        ) : (
          <div>
            {logs.map((log, i) => (
              <div key={i} style={{
                background: "#1a1f3a", borderRadius: 8, padding: "14px 18px", marginBottom: 10,
                borderLeft: "4px solid " + getSeverityColor(log.severity),
                boxShadow: "0 0 10px " + getSeverityColor(log.severity) + "33"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ color: "#00f0ff", fontWeight: "bold" }}>{log.source_ip || "Unknown IP"}</span>
                  <span style={{
                    background: getSeverityColor(log.severity), color: "#0a0e27",
                    padding: "2px 10px", borderRadius: 4, fontSize: 12, fontWeight: "bold"
                  }}>
                    {(log.severity || "info").toUpperCase()}
                  </span>
                </div>
                <div style={{ color: "#e0e6ff", marginTop: 6 }}>{log.event_type || "Unknown Event"}</div>
                <div style={{ color: "#8892b0", fontSize: 12, marginTop: 4 }}>{log.created_at}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;