// API Configuration
// This file manages API URLs for local development and production

const config = {
    // Always use Railway backend (backend is deployed, not running locally)
    API_URL: 'https://web-production-8b8e1f.up.railway.app'
};

// Export for use in HTML files
window.API_CONFIG = config;
