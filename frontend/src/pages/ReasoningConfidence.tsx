import React from 'react'

const ReasoningConfidence: React.FC = () => {
  return (
    <div className="page-container">
      <div className="page-content">
        <h1 className="page-title">REASONING & CONFIDENCE</h1>
        <div className="reasoning-dashboard">
          <div className="confidence-metrics">
            <div className="metric-card">
              <div className="metric-label">Overall Confidence</div>
              <div className="metric-value">87%</div>
              <div className="metric-bar">
                <div className="metric-fill" style={{ width: '87%' }}></div>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Reasoning Quality</div>
              <div className="metric-value">92%</div>
              <div className="metric-bar">
                <div className="metric-fill" style={{ width: '92%' }}></div>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Response Accuracy</div>
              <div className="metric-value">85%</div>
              <div className="metric-bar">
                <div className="metric-fill" style={{ width: '85%' }}></div>
              </div>
            </div>
          </div>
          <div className="reasoning-log">
            <h2 className="log-title">Recent Reasoning Steps</h2>
            <div className="log-entries">
              <div className="log-entry">
                <span className="log-time">14:32:15</span>
                <span className="log-step">Analyzed query context</span>
                <span className="log-confidence">Confidence: 95%</span>
              </div>
              <div className="log-entry">
                <span className="log-time">14:32:16</span>
                <span className="log-step">Retrieved relevant information</span>
                <span className="log-confidence">Confidence: 88%</span>
              </div>
              <div className="log-entry">
                <span className="log-time">14:32:17</span>
                <span className="log-step">Generated response</span>
                <span className="log-confidence">Confidence: 87%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ReasoningConfidence

