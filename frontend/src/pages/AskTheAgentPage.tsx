import React, { useState } from 'react'
import { ThumbsUp, ThumbsDown, ArrowRight, FileText } from 'lucide-react'

const AskTheAgentPage: React.FC = () => {
  const [query, setQuery] = useState('')

  const sampleResponse = {
    id: '#8821-X',
    explanation: 'Based on the provided context, the **AuthenticationModule** handles user sessions through a JWT-based strategy. The core logic resides in `auth/provider.go`.',
    code: `func ValidateSession(token string) (bool, error) {
    // Check signature validity
    claims, err := jwt.Parse(token)
    if err != nil {
        return false, err
    }
    return claims.Valid, nil
}`,
    instruction: 'Ensure that the **RSA_256** key pair is properly mounted in the production environment variables before deploying this change.',
    confidence: 98.4,
    confidenceText: 'Model is highly certain about the JWT implementation details referenced.',
    sources: [
      { file: 'lib/auth/provider.go', lines: '40-52', relevance: 'High Relevance' },
      { file: 'config/schema.yaml', lines: 'Line 12', relevance: '' },
      { file: 'Vector Store: 8fb2...1a', lines: 'Chunk ID: 9921', relevance: '' }
    ],
    latency: '124ms',
    tokens: '452 / 4096'
  }

  return (
    <div className="page-container ask-agent-page">
      <div className="page-content ask-agent-content">
        <div className="agent-main-layout">
          {/* Main Content Area */}
          <div className="agent-main-content">
            {/* Generated Response Section */}
            <div className="generated-response-section">
              <div className="response-header">
                <h2 className="response-title">GENERATED_RESPONSE // ID: {sampleResponse.id}</h2>
                <div className="response-feedback">
                  <button className="feedback-button">
                    <ThumbsUp size={16} />
                  </button>
                  <button className="feedback-button">
                    <ThumbsDown size={16} />
                  </button>
                </div>
              </div>
              
              <div className="response-content">
                <div className="response-text">
                  <p>{sampleResponse.explanation}</p>
                </div>
                
                <div className="response-code">
                  <pre><code>{sampleResponse.code}</code></pre>
                </div>
                
                <div className="response-instruction">
                  <p>{sampleResponse.instruction}</p>
                </div>
              </div>
            </div>

            {/* Input Sequence Section */}
            <div className="input-sequence-section">
              <div className="input-header">
                <h3 className="input-title">INPUT_SEQUENCE</h3>
                <span className="input-status">STATUS: AWAITING_INPUT</span>
              </div>
              
              <textarea
                className="query-input"
                placeholder="// Enter system query regarding architecture or debug trace..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                rows={6}
              />
              
              <div className="input-actions">
                <button className="action-button">ATTACH</button>
                <button className="action-button">HISTORY</button>
                <button className="action-button primary">
                  EXECUTE
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="agent-sidebar">
            {/* Confidence Score */}
            <div className="sidebar-section">
              <h3 className="sidebar-title">Confidence Score</h3>
              <div className="confidence-display">
                <div className="confidence-bar-container">
                  <div 
                    className="confidence-bar" 
                    style={{ width: `${sampleResponse.confidence}%` }}
                  ></div>
                </div>
                <div className="confidence-value">{sampleResponse.confidence}%</div>
              </div>
              <p className="confidence-text">{sampleResponse.confidenceText}</p>
            </div>

            {/* Referenced Sources */}
            <div className="sidebar-section">
              <h3 className="sidebar-title">Referenced Sources</h3>
              <div className="sources-count">{sampleResponse.sources.length} sources</div>
              <div className="sources-list">
                {sampleResponse.sources.map((source, index) => (
                  <div key={index} className="source-item">
                    <div className="source-header">
                      <FileText size={14} className="source-icon" />
                      <span className="source-file">{source.file}</span>
                    </div>
                    <div className="source-details">
                      <span className="source-lines">{source.lines}</span>
                      {source.relevance && (
                        <span className="source-relevance">{source.relevance}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Metrics */}
            <div className="sidebar-metrics">
              <div className="metric-item">
                <span className="metric-label">LATENCY:</span>
                <span className="metric-value">{sampleResponse.latency}</span>
              </div>
              <div className="metric-item">
                <span className="metric-label">TOKENS:</span>
                <span className="metric-value">{sampleResponse.tokens}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AskTheAgentPage

