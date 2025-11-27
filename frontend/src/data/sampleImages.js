// Sample images for demo purposes
// Add your sample images to /public/sample-images/ folder

export const sampleImages = [
  {
    id: 1,
    name: "English Sample",
    path: "/sample-images/sample_1_english.jpg",
    description: "English text for OCR testing",
    category: "text"
  },
  {
    id: 2,
    name: "Hindi Sample",
    path: "/sample-images/sample_2_hindi.jpg",
    description: "Hindi text for multilingual OCR",
    category: "text"
  },
  {
    id: 3,
    name: "Mixed Languages",
    path: "/sample-images/sample_3_mixed.jpg",
    description: "Mixed language text sample",
    category: "text"
  },
  {
    id: 4,
    name: "Document",
    path: "/sample-images/sample_4_document.jpg",
    description: "Document with clear text",
    category: "text"
  },
  {
    id: 5,
    name: "Menu",
    path: "/sample-images/sample_5_menu.jpg",
    description: "Restaurant menu sample",
    category: "text"
  },
  {
    id: 6,
    name: "Flood Alerts",
    path: "/sample-images/sample_6_flood_alerts.png",
    description: "Alert message with text",
    category: "text"
  },
  {
    id: 7,
    name: "Solar Chargers",
    path: "/sample-images/sample_7_solar_chargers.png",
    description: "Information with text",
    category: "text"
  },
  {
    id: 8,
    name: "Traffic Maps",
    path: "/sample-images/sample_8_traffic_maps.png",
    description: "Traffic information text",
    category: "text"
  },
  {
    id: 9,
    name: "UPI Loans",
    path: "/sample-images/sample_9_upi_loans.png",
    description: "Loan information with text",
    category: "text"
  },
  {
    id: 10,
    name: "Sample 1",
    path: "/sample-images/sample_10_sample1.png",
    description: "Additional sample image 1",
    category: "text"
  },
  {
    id: 11,
    name: "Sample 2",
    path: "/sample-images/sample_11_sample2.png",
    description: "Additional sample image 2",
    category: "text"
  },
  {
    id: 12,
    name: "Sample 3",
    path: "/sample-images/sample_12_sample3.png",
    description: "Additional sample image 3",
    category: "text"
  },
  {
    id: 13,
    name: "Solar Chargers (Variant)",
    path: "/sample-images/sample_13_solar_chargers_variant.png",
    description: "Alternative solar charger information",
    category: "text"
  }
];

// Helper function to check if sample image exists
export const loadSampleImage = async (path) => {
  try {
    const response = await fetch(path);
    if (!response.ok) {
      console.warn(`Sample image not found: ${path}`);
      return null;
    }
    const blob = await response.blob();
    return new File([blob], path.split('/').pop(), { type: blob.type });
  } catch (error) {
    console.error('Error loading sample image:', error);
    return null;
  }
};
