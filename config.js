// API Configuration
// This file manages API URLs for local development and production

const config = {
    // Automatically detect environment
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'  // Local development
        : 'https://your-app-name.up.railway.app',  // Production - UPDATE THIS after Railway deployment
};

// Export for use in HTML files
window.API_CONFIG = config;
