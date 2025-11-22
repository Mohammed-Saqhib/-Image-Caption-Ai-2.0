import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

import ImageUpload from './components/ImageUpload';
import OCRPanel from './components/OCRPanel';
import CaptionPanel from './components/CaptionPanel';
import TranslationPanel from './components/TranslationPanel';
import TTSPanel from './components/TTSPanel';
import Header from './components/Header';
import TabNavigation from './components/TabNavigation';
import Login from './components/Login';

import * as api from './services/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('ocr');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Results
  const [ocrResult, setOcrResult] = useState(null);
  const [captionResult, setCaptionResult] = useState(null);
  const [translationResult, setTranslationResult] = useState(null);
  
  // Check if user is already logged in
  useEffect(() => {
    const savedUser = localStorage.getItem('aiplatform_currentUser');
    if (savedUser) {
      setCurrentUser(savedUser);
      setIsAuthenticated(true);
    }
  }, []);
  
  // Health check on mount (only when authenticated)
  useEffect(() => {
    if (isAuthenticated) {
      checkHealth();
    }
  }, [isAuthenticated]);

  const handleLogin = (username) => {
    setCurrentUser(username);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('aiplatform_currentUser');
    setCurrentUser(null);
    setIsAuthenticated(false);
    setUploadedImage(null);
    setImagePreview(null);
    setOcrResult(null);
    setCaptionResult(null);
    setTranslationResult(null);
    toast.info('👋 Logged out successfully!');
  };

  const checkHealth = async () => {
    try {
      const health = await api.healthCheck();
      console.log('API Health:', health);
      toast.success('✅ Connected to API successfully!', {
        position: 'bottom-right',
        autoClose: 3000,
      });
    } catch (error) {
      console.error('API Health Check Failed:', error);
      toast.error('⚠️ Could not connect to API. Check backend status.', {
        position: 'bottom-right',
        autoClose: 5000,
      });
    }
  };

  const handleImageUpload = (file) => {
    setUploadedImage(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
    
    toast.info('📸 Image uploaded! Select a feature to process.', {
      position: 'top-center',
      autoClose: 2000,
    });
  };

  const handleOCR = async (languages) => {
    if (!uploadedImage) {
      toast.warn('Please upload an image first!');
      return;
    }

    setLoading(true);
    try {
      const result = await api.extractText(uploadedImage, languages.join(','));
      console.log('OCR Result:', result);
      setOcrResult(result);
      setActiveTab('ocr');
      toast.success('✅ Text extracted successfully!');
    } catch (error) {
      console.error('OCR Error:', error);
      const errorMessage = error.response?.data?.detail || error.response?.data?.error || error.message || 'Failed to extract text';
      toast.error(`❌ ${errorMessage}`);
      // Set error result for display
      setOcrResult({
        success: false,
        error: errorMessage
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCaption = async (mode) => {
    if (!uploadedImage) {
      toast.warn('Please upload an image first!');
      return;
    }

    setLoading(true);
    try {
      const result = await api.generateCaption(uploadedImage, mode);
      setCaptionResult(result);
      setActiveTab('caption');
      toast.success('✅ Caption generated successfully!');
    } catch (error) {
      console.error('Caption Error:', error);
      toast.error('❌ Failed to generate caption. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async (text, targetLanguage) => {
    if (!text) {
      toast.warn('Please enter text to translate!');
      return;
    }

    setLoading(true);
    try {
      const result = await api.translateText(text, targetLanguage);
      setTranslationResult(result);
      toast.success('✅ Text translated successfully!');
    } catch (error) {
      console.error('Translation Error:', error);
      toast.error('❌ Failed to translate text. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTTS = async (text, language, rate) => {
    if (!text) {
      toast.warn('Please enter text for speech!');
      return null;
    }

    setLoading(true);
    try {
      const audioBlob = await api.textToSpeech(text, language, rate);
      toast.success('🎧 Audio generated successfully!');
      return audioBlob;
    } catch (error) {
      console.error('TTS Error:', error);
      toast.error('❌ Failed to generate speech. Try again.');
      return null;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
          <Header user={currentUser} onLogout={handleLogout} />
          
          <div className="container">
            <motion.div
              className="main-content"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              {/* Left Column - Sticky Sidebar */}
              <div className="left-column">
                <ImageUpload
                  onUpload={handleImageUpload}
                  imagePreview={imagePreview}
                  loading={loading}
                />
                
                <TabNavigation
                  activeTab={activeTab}
                  setActiveTab={setActiveTab}
                />
              </div>

              {/* Right Column - Content Panels */}
              <div className="right-column">
                {/* Image Preview Section - Always Visible when image uploaded */}
                {imagePreview && (
                  <motion.div
                    className="uploaded-image-section"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.4 }}
                  >
                    <div className="uploaded-image-header">
                      <h3>📸 Uploaded Image</h3>
                      <button 
                        className="change-image-btn"
                        onClick={() => {
                          setUploadedImage(null);
                          setImagePreview(null);
                          setOcrResult(null);
                          setCaptionResult(null);
                          setTranslationResult(null);
                        }}
                      >
                        Change Image
                      </button>
                    </div>
                    <div className="uploaded-image-display">
                      <img src={imagePreview} alt="Uploaded" className="main-image-preview" />
                      <div className="image-overlay">
                        <div className="image-details">
                          <span className="detail-badge">
                            ✓ Ready for Processing
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Processing Panels */}
                <div className="processing-section">
                  {activeTab === 'ocr' && (
                    <OCRPanel
                      onProcess={handleOCR}
                      result={ocrResult}
                      loading={loading}
                      hasImage={!!uploadedImage}
                    />
                  )}

                  {activeTab === 'caption' && (
                    <CaptionPanel
                      onProcess={handleCaption}
                      result={captionResult}
                      loading={loading}
                      hasImage={!!uploadedImage}
                    />
                  )}

                  {activeTab === 'translation' && (
                    <TranslationPanel
                      onTranslate={handleTranslate}
                      result={translationResult}
                      loading={loading}
                      ocrText={ocrResult?.data?.text}
                      captionText={captionResult?.data?.caption}
                    />
                  )}

                  {activeTab === 'tts' && (
                    <TTSPanel
                      onGenerate={handleTTS}
                      loading={loading}
                      ocrText={ocrResult?.data?.text}
                      captionText={captionResult?.data?.caption}
                      translatedText={translationResult?.data?.translated_text}
                    />
                  )}
                </div>
              </div>
            </motion.div>
          </div>
        </>
      )}

      <ToastContainer
        position="bottom-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </div>
  );
}

export default App;
