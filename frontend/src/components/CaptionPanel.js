import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaImage, FaDownload, FaCopy, FaCheck, FaCloud, FaLaptop, FaTag, FaMapMarkerAlt, FaEye, FaHeart } from 'react-icons/fa';
import './CaptionPanel.css';

const CaptionPanel = ({ onProcess, result, loading, hasImage }) => {
  const [mode, setMode] = useState('cloud');
  const [copied, setCopied] = useState(false);

  const handleGenerate = () => {
    onProcess(mode);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text || result?.data?.detailed_description || result?.data?.caption);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadCaption = () => {
    if (result?.data?.detailed_description) {
      const content = `AI Image Caption Analysis
========================================

Quick Caption:
${result.data.caption}

Detailed Description:
${result.data.detailed_description}

Model: ${result.data.model}
Mode: ${result.data.mode}
Confidence: ${(result.data.confidence * 100).toFixed(0)}%
Generated: ${new Date().toLocaleString()}

${result.data.insights ? `
Insights:
- Subjects: ${result.data.insights.subjects?.join(', ') || 'N/A'}
- Settings: ${result.data.insights.settings?.join(', ') || 'N/A'}
- Mood: ${result.data.insights.mood || 'N/A'}
- Keywords: ${result.data.insights.keywords?.join(', ') || 'N/A'}
` : ''}
`;
      
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai_caption_${Date.now()}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <motion.div
      className="panel caption-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="panel-header">
        <FaImage className="panel-icon" />
        <h2>AI Image Captioning</h2>
        <p>Generate rich, detailed descriptions with scene understanding</p>
      </div>

      <div className="panel-content">
        {!hasImage ? (
          <motion.div
            className="no-image-state"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
          >
            <FaImage className="no-image-icon" />
            <h3>No Image Uploaded</h3>
            <p>Please upload an image from the left sidebar to generate AI-powered captions</p>
          </motion.div>
        ) : (
          <>
            <div className="mode-selector">
              <h3>Processing Mode</h3>
              <div className="mode-options">
                <motion.button
                  className={`mode-btn ${mode === 'cloud' ? 'selected' : ''}`}
                  onClick={() => setMode('cloud')}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaCloud />
                  <div>
                    <strong>Cloud Mode</strong>
                    <span>Faster, uses Hugging Face API</span>
                  </div>
            </motion.button>

            <motion.button
              className={`mode-btn ${mode === 'local' ? 'selected' : ''}`}
              onClick={() => setMode('local')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaLaptop />
              <div>
                <strong>Local Mode</strong>
                <span>More privacy, runs on server</span>
              </div>
            </motion.button>
          </div>
        </div>

        <motion.button
          className="action-btn primary"
          onClick={handleGenerate}
          disabled={loading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing Image...
            </>
          ) : (
            <>
              <FaImage /> Generate Caption
            </>
          )}
        </motion.button>

        {result && result.success && (
          <motion.div
            className="result-box"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="result-header">
              <h3>AI Generated Caption</h3>
              <div className="result-actions">
                <button
                  className="icon-btn"
                  onClick={() => copyToClipboard()}
                  title="Copy to clipboard"
                >
                  {copied ? <FaCheck /> : <FaCopy />}
                </button>
                <button
                  className="icon-btn"
                  onClick={downloadCaption}
                  title="Download as TXT"
                >
                  <FaDownload />
                </button>
              </div>
            </div>

            <div className="result-stats">
              <div className="stat">
                <span className="stat-label">Model:</span>
                <span className="stat-value">BLIP</span>
              </div>
              <div className="stat">
                <span className="stat-label">Mode:</span>
                <span className="stat-value">{result.data.mode}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Confidence:</span>
                <span className="stat-value">{(result.data.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>

            {/* Insights Section */}
            {result.data.insights && (
              <motion.div 
                className="insights-grid"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                {result.data.insights.subjects && result.data.insights.subjects.length > 0 && (
                  <div className="insight-card">
                    <div className="insight-icon"><FaEye /></div>
                    <div className="insight-content">
                      <h4>Subject</h4>
                      <div className="insight-tags">
                        {result.data.insights.subjects.map((subject, idx) => (
                          <span key={idx} className="tag subject-tag">{subject}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {result.data.insights.settings && result.data.insights.settings.length > 0 && (
                  <div className="insight-card">
                    <div className="insight-icon"><FaMapMarkerAlt /></div>
                    <div className="insight-content">
                      <h4>Setting</h4>
                      <div className="insight-tags">
                        {result.data.insights.settings.map((setting, idx) => (
                          <span key={idx} className="tag setting-tag">{setting}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {result.data.insights.mood && (
                  <div className="insight-card">
                    <div className="insight-icon"><FaHeart /></div>
                    <div className="insight-content">
                      <h4>Mood</h4>
                      <div className="insight-tags">
                        <span className="tag mood-tag">{result.data.insights.mood}</span>
                      </div>
                    </div>
                  </div>
                )}

                {result.data.insights.keywords && result.data.insights.keywords.length > 0 && (
                  <div className="insight-card full-width">
                    <div className="insight-icon"><FaTag /></div>
                    <div className="insight-content">
                      <h4>Keywords</h4>
                      <div className="insight-tags">
                        {result.data.insights.keywords.map((keyword, idx) => (
                          <span key={idx} className="tag keyword-tag">{keyword}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            <div className="caption-display">
              <div className="caption-icon">✨</div>
              <div className="caption-content">
                <div className="caption-section">
                  <h4>Quick Caption</h4>
                  <p className="caption-text">{result.data.caption}</p>
                  <button 
                    className="copy-section-btn"
                    onClick={() => copyToClipboard(result.data.caption)}
                    title="Copy quick caption"
                  >
                    {copied ? <FaCheck /> : <FaCopy />}
                  </button>
                </div>
                
                {result.data.detailed_description && result.data.detailed_description !== result.data.caption && (
                  <div className="caption-section detailed">
                    <h4>📝 Detailed Description</h4>
                    <p className="detailed-text">{result.data.detailed_description}</p>
                    <button 
                      className="copy-section-btn"
                      onClick={() => copyToClipboard(result.data.detailed_description)}
                      title="Copy detailed description"
                    >
                      {copied ? <FaCheck /> : <FaCopy />}
                    </button>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
          </>
        )}
      </div>
    </motion.div>
  );
};

export default CaptionPanel;
