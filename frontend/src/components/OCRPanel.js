import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaEye, FaDownload, FaCopy, FaCheck, FaImage } from 'react-icons/fa';
import * as api from '../services/api';
import './OCRPanel.css';

const OCRPanel = ({ onProcess, result, loading, hasImage }) => {
  const [selectedLanguages, setSelectedLanguages] = useState(['en']);
  const [availableLanguages, setAvailableLanguages] = useState([]);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadLanguages();
  }, []);

  const loadLanguages = async () => {
    try {
      const data = await api.getOCRLanguages();
      setAvailableLanguages(data.languages || []);
    } catch (error) {
      console.error('Failed to load languages:', error);
    }
  };

  const toggleLanguage = (langCode) => {
    setSelectedLanguages(prev => 
      prev.includes(langCode)
        ? prev.filter(l => l !== langCode)
        : [...prev, langCode]
    );
  };

  const handleExtract = () => {
    onProcess(selectedLanguages);
  };

  const copyToClipboard = () => {
    if (result?.data?.text) {
      navigator.clipboard.writeText(result.data.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const downloadText = () => {
    if (result?.data?.text) {
      const blob = new Blob([result.data.text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ocr_text_${Date.now()}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <motion.div
      className="panel ocr-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="panel-header">
        <FaEye className="panel-icon" />
        <h2>Optical Character Recognition</h2>
        <p>Extract text from images in multiple languages</p>
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
            <p>Please upload an image from the left sidebar to extract text using OCR</p>
          </motion.div>
        ) : (
          <>
            <div className="language-selector">
              <h3>Select Languages</h3>
              <div className="language-grid">
                {availableLanguages.map(lang => (
                  <motion.button
                    key={lang.code}
                    className={`language-btn ${selectedLanguages.includes(lang.code) ? 'selected' : ''}`}
                    onClick={() => toggleLanguage(lang.code)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {lang.name}
                  </motion.button>
                ))}
              </div>
            </div>

            <motion.button
              className="action-btn primary"
              onClick={handleExtract}
              disabled={loading || selectedLanguages.length === 0}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Extracting Text...
                </>
              ) : (
                <>
                  <FaEye /> Extract Text
                </>
              )}
            </motion.button>

            {result && result.success === false && (
              <motion.div
                className="error-box"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
              >
                <div className="error-header">
                  <h3>❌ Error</h3>
                </div>
                <div className="error-message">
                  {result.error || 'Failed to extract text. Please try again.'}
                </div>
              </motion.div>
            )}

            {result && result.success && (
              <motion.div
                className="result-box"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
              >
                <div className="result-header">
                  <h3>Extracted Text</h3>
                  <div className="result-actions">
                    <button
                      className="icon-btn"
                      onClick={copyToClipboard}
                      title="Copy to clipboard"
                    >
                      {copied ? <FaCheck /> : <FaCopy />}
                    </button>
                    <button
                      className="icon-btn"
                      onClick={downloadText}
                      title="Download as TXT"
                    >
                      <FaDownload />
                    </button>
                  </div>
                </div>

                <div className="result-stats">
                  <div className="stat">
                    <span className="stat-label">Words:</span>
                    <span className="stat-value">{result.data.word_count}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Characters:</span>
                    <span className="stat-value">{result.data.character_count}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Confidence:</span>
                    <span className="stat-value">{(result.data.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>

                <div className="result-text">
                  {result.data.text || 'No text detected'}
                </div>
              </motion.div>
            )}
          </>
        )}
      </div>
    </motion.div>
  );
};

export default OCRPanel;
