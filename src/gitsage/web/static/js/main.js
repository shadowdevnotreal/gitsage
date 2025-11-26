// GitSage Web Interface - Main JavaScript

// API helper function
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Environment status updater
async function updateEnvironmentStatus() {
    try {
        const data = await apiCall('/api/environment');
        if (data.success) {
            console.log('Environment data loaded:', data);
            // You can update UI elements here if needed
        }
    } catch (error) {
        console.error('Failed to load environment status:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('GitSage Web Interface initialized');

    // Auto-refresh environment status every 30 seconds
    if (window.location.pathname === '/') {
        updateEnvironmentStatus();
        setInterval(updateEnvironmentStatus, 30000);
    }
});

// Show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;

    const container = document.querySelector('.container');
    container.insertBefore(notification, container.firstChild);

    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Export functions for use in other scripts
window.GitSage = {
    apiCall,
    showNotification,
    updateEnvironmentStatus
};
