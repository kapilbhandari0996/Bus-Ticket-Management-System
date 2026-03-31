/**
 * API Client for LETS GO Bus Service Backend
 * Base URL for the backend API
 */
const API_BASE_URL = 'http://localhost:5000/api';

// Helper functions
function getAuthHeader() {
    const token = localStorage.getItem('authToken');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
        ...options.headers
    };

    console.log(`API Request: ${options.method || 'GET'} ${url}`);

    try {
        const response = await fetch(url, {
            ...options,
            headers
        });

        // Handle non-JSON responses
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            throw new Error('Server returned non-JSON response');
        }

        const data = await response.json();

        console.log(`API Response (${response.status}):`, data);

        if (!response.ok) {
            // Extract detailed error message
            const errorMsg = data.message || data.error || 'API request failed';
            throw new Error(errorMsg);
        }

        return data;
    } catch (error) {
        // Handle network errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            console.error('Network error:', error);
            throw new Error('Cannot connect to backend server. Please ensure it\'s running on port 5000.');
        }
        
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication API
const AuthAPI = {
    register: async (fullName, email, password, phone = '') => {
        return await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ full_name: fullName, email, password, phone })
        });
    },

    login: async (email, password) => {
        return await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },

    getCurrentUser: async () => {
        return await apiRequest('/auth/me');
    },

    updateProfile: async (fullName, phone) => {
        return await apiRequest('/auth/profile', {
            method: 'PUT',
            body: JSON.stringify({ full_name: fullName, phone })
        });
    },

    logout: () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
        window.location.href = 'login.html';
    }
};

// Buses API
const BusesAPI = {
    search: async (params) => {
        const queryString = new URLSearchParams(params).toString();
        return await apiRequest(`/buses/search?${queryString}`);
    },

    getLocations: async () => {
        return await apiRequest('/buses/locations');
    },

    getBusDetails: async (busId) => {
        return await apiRequest(`/buses/${busId}`);
    },

    getAvailableSeats: async (busId, date) => {
        return await apiRequest(`/buses/${busId}/seats?date=${date}`);
    },

    getRoutes: async () => {
        return await apiRequest('/buses/routes');
    }
};

// Bookings API
const BookingsAPI = {
    create: async (bookingData) => {
        return await apiRequest('/bookings', {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
    },

    getMyBookings: async () => {
        return await apiRequest('/bookings/my-bookings');
    },

    getBooking: async (bookingId) => {
        return await apiRequest(`/bookings/${bookingId}`);
    },

    getBookingByReference: async (reference) => {
        return await apiRequest(`/bookings/reference/${reference}`);
    },

    cancelBooking: async (bookingId) => {
        return await apiRequest(`/bookings/${bookingId}/cancel`, {
            method: 'POST'
        });
    }
};

// Payment API
const PaymentAPI = {
    initiate: async (bookingId, paymentMethod = 'UPI') => {
        return await apiRequest('/payment/initiate', {
            method: 'POST',
            body: JSON.stringify({ booking_id: bookingId, payment_method: paymentMethod })
        });
    },

    confirm: async (bookingId, transactionId) => {
        return await apiRequest('/payment/confirm', {
            method: 'POST',
            body: JSON.stringify({ booking_id: bookingId, transaction_id: transactionId })
        });
    },

    getStatus: async (bookingId) => {
        return await apiRequest(`/payment/${bookingId}/status`);
    },

    downloadTicket: async (bookingId) => {
        const token = localStorage.getItem('authToken');
        const url = `${API_BASE_URL}/payment/${bookingId}/ticket/pdf`;
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to download ticket');
        }

        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `ticket_${bookingId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        a.remove();
    }
};

// Check if user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}

// Get current user from localStorage
function getCurrentUser() {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
}

// Update user info in localStorage
function updateCurrentUser(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
}

// Require authentication for a page
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Update profile dropdown with user info
function updateProfileDropdown() {
    const user = getCurrentUser();
    if (user) {
        const profileSpans = document.querySelectorAll('.profile-dropdown .dropdown-menu span');
        profileSpans.forEach(span => {
            if (span.textContent.trim() === 'John Doe') {
                span.textContent = user.full_name;
            }
        });
    }
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', () => {
    updateProfileDropdown();
});
