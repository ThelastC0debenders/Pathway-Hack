import React from 'react'

const ChangeIntelligence: React.FC = () => {
  return (
    <div className="page-container">
      <div className="page-content">
        <h1 className="page-title">CHANGE INTELLIGENCE</h1>
        <div className="intelligence-settings">
          <div className="settings-card">
            <h2 className="settings-section-title">Model Selection</h2>
            <div className="settings-options">
              <div className="option-item">
                <label className="option-label">
                  <input type="radio" name="model" value="gpt-4" defaultChecked />
                  <span>GPT-4</span>
                </label>
              </div>
              <div className="option-item">
                <label className="option-label">
                  <input type="radio" name="model" value="gpt-3.5" />
                  <span>GPT-3.5 Turbo</span>
                </label>
              </div>
              <div className="option-item">
                <label className="option-label">
                  <input type="radio" name="model" value="claude" />
                  <span>Claude 3</span>
                </label>
              </div>
            </div>
          </div>
          <div className="settings-card">
            <h2 className="settings-section-title">Configuration</h2>
            <div className="config-item">
              <label>Temperature</label>
              <input type="range" min="0" max="1" step="0.1" defaultValue="0.7" />
            </div>
            <div className="config-item">
              <label>Max Tokens</label>
              <input type="number" defaultValue="2000" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChangeIntelligence

