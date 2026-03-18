import "../styles/sidebar.css";

const AGENTS = [
  { key: "task",     label: "Task Agent",     color: "#1D9E75", desc: "Creates & lists tasks" },
  { key: "calendar", label: "Calendar Agent", color: "#378ADD", desc: "Schedules events" },
  { key: "reminder", label: "Reminder Agent", color: "#D85A30", desc: "Sets reminders" },
];

export default function Sidebar({ activeAgent, onLogout }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="sidebar-brand">
          <div className="brand-mark">M</div>
          <div>
            <div className="brand-name">Multi-AI</div>
            <div className="brand-sub">Agent System</div>
          </div>
        </div>

        <div className="sidebar-section-label">Agents</div>
        {AGENTS.map((agent) => (
          <div
            key={agent.key}
            className={`agent-row ${activeAgent === agent.key ? "agent-active" : ""}`}
          >
            <span
              className="agent-dot"
              style={{ background: activeAgent === agent.key ? agent.color : "var(--muted)" }}
            />
            <div className="agent-info">
              <span className="agent-name">{agent.label}</span>
              <span className="agent-desc">{agent.desc}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="sidebar-bottom">
        <button className="logout-btn" onClick={onLogout}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Sign out
        </button>
      </div>
    </aside>
  );
}