import React from 'react'

const AskTheAgentPage: React.FC = () => {
  return (
    <div className="page-container">
      <div className="page-content">
        <h1 className="page-title">ASK THE AGENT</h1>
        <div className="agent-interface">
          <div className="chat-container">
            <div className="chat-messages">
              <div className="message agent-message">
                <div className="message-content">
                  <p>Hello! I'm your AI agent. How can I help you today?</p>
                </div>
              </div>
            </div>
            <div className="chat-input-container">
              <input 
                type="text" 
                className="chat-input" 
                placeholder="Type your question here..."
              />
              <button className="send-button">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AskTheAgentPage

