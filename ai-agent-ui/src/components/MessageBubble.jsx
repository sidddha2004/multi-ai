import "../styles/message.css";

const BADGE_COLORS = {
  task_agent:     { bg: "#E1F5EE", color: "#0F6E56", label: "task" },
  calendar_agent: { bg: "#E6F1FB", color: "#185FA5", label: "calendar" },
  reminder_agent: { bg: "#FAECE7", color: "#993C1D", label: "reminder" },
};

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`msg-wrap ${isUser ? "msg-user" : "msg-bot"}`}>
      {!isUser && (
        <div className="avatar">AI</div>
      )}
      <div className="msg-body">
        <div className={`bubble ${isUser ? "bubble-user" : "bubble-bot"}`}>
          {message.content}
        </div>

        {message.plan && message.plan.length > 0 && (
          <div className="plan-card">
            <div className="plan-header">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 11 12 14 22 4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
              Execution plan
            </div>
            {message.plan.map((step, i) => {
              const badge = BADGE_COLORS[step.agent] || { bg: "#f0f0f0", color: "#555", label: step.agent };
              return (
                <div className="plan-step" key={i}>
                  <span
                    className="plan-badge"
                    style={{ background: badge.bg, color: badge.color }}
                  >
                    {badge.label}
                  </span>
                  <span className="plan-task">{step.task}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}