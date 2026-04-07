// API Configuration
// This file manages API URLs for local development and production

const config = {
    // Automatically detect environment
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'  // Local development
        : 'https://web-production-8b8e1f.up.railway.app',  // Production - Railway backend
};

// Export for use in HTML files
window.API_CONFIG = config;
