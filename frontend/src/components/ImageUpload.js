import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { FaCloudUploadAlt, FaImage, FaImages } from 'react-icons/fa';
import { sampleImages, loadSampleImage } from '../data/sampleImages';
import './ImageUpload.css';

const ImageUpload = ({ onUpload, imagePreview, loading }) => {
  const [showSamples, setShowSamples] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
      setShowSamples(false);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    },
    multiple: false,
    disabled: loading
  });

  const handleSampleSelect = async (sample) => {
    try {
      // Try to load from multiple possible paths
      const possiblePaths = [
        sample.path,  // Original path
        `/build${sample.path}`,  // Build folder
        `${process.env.PUBLIC_URL}${sample.path}`  // Public URL
      ];
      
      let file = null;
      for (const path of possiblePaths) {
        file = await loadSampleImage(path);
        if (file) {
          console.log(`Loaded sample image from: ${path}`);
          break;
        }
      }
      
      if (file) {
        onUpload(file);
        setShowSamples(false);
      } else {
        console.error(`Failed to load sample image: ${sample.name}`);
        alert(`Sorry, couldn't load sample image: ${sample.name}. Please try uploading your own image.`);
      }
    } catch (error) {
      console.error('Error selecting sample:', error);
      alert('Error loading sample image. Please try another one.');
    }
  };

  return (
    <motion.div
      className="image-upload-container"
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div
        {...getRootProps()}
        className={`upload-area ${isDragActive ? 'drag-active' : ''} ${loading ? 'disabled' : ''}`}
      >
        <input {...getInputProps()} />
        
        {imagePreview ? (
          <div className="upload-success">
            <div className="success-icon">✓</div>
            <h3>Image Uploaded!</h3>
            <p>Click to change image</p>
            <div className="success-badge">Ready to Process</div>
          </div>
        ) : (
          <div className="upload-prompt">
            <FaCloudUploadAlt className="upload-icon" />
            <h3>Upload Image</h3>
            <p>Drag & drop or click to browse</p>
            <span className="file-types">PNG, JPG, JPEG, GIF, WEBP</span>
          </div>
        )}
      </div>

      {/* Sample Images Button */}
      <motion.button
        className="sample-images-toggle"
        onClick={() => setShowSamples(!showSamples)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        disabled={loading}
      >
        <FaImages /> {showSamples ? 'Hide' : 'Show'} Sample Images
      </motion.button>

      {/* Sample Images Grid */}
      <AnimatePresence>
        {showSamples && (
          <motion.div
            className="sample-images-grid"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h4 className="samples-title">
              <FaImages /> Choose a Sample Image
            </h4>
            <div className="samples-container">
              {sampleImages.map((sample) => (
                <motion.div
                  key={sample.id}
                  className="sample-card"
                  onClick={() => handleSampleSelect(sample)}
                  whileHover={{ scale: 1.05, y: -5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <div className="sample-image-wrapper">
                    <img
                      src={`${process.env.PUBLIC_URL}${sample.path}`}
                      alt={sample.name}
                      loading="lazy"
                      onError={(e) => {
                        // Try alternative path
                        if (!e.target.dataset.retried) {
                          e.target.dataset.retried = 'true';
                          e.target.src = sample.path;
                        } else {
                          // Show placeholder with gradient
                          e.target.style.display = 'none';
                          e.target.parentElement.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                          e.target.parentElement.innerHTML = `
                            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: white;">
                              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                <polyline points="21 15 16 10 5 21"></polyline>
                              </svg>
                              <p style="margin-top: 8px; font-size: 12px;">Preview</p>
                            </div>
                          `;
                        }
                      }}
                    />
                    <div className="sample-overlay">
                      <FaImage />
                      <span>Use This</span>
                    </div>
                  </div>
                  <div className="sample-info">
                    <h5>{sample.name}</h5>
                    <p>{sample.description}</p>
                    <span className="sample-category">{sample.category}</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default ImageUpload;
