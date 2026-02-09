/**
 * Authentication Handler
 * Manages login flow and token storage
 */

const AUTH_API = '/auth/login';
const TODOS_PAGE = '/static/todos.html';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Check if already logged in
    checkAuthStatus();
});

/**
 * Handle login form submission
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorElement = document.getElementById('errorMessage');
    
    // Clear previous errors
    errorElement.style.display = 'none';
    errorElement.textContent = '';
    
    // Validate inputs
    if (!username || !password) {
        showError('Please enter both username and password');
        return;
    }
    
    try {
        // Disable submit button
        const submitBtn = document.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Signing in...';
        
        // Build URL with query parameters
        const loginUrl = `${AUTH_API}?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
        
        // Make login request
        const response = await fetch(loginUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Invalid username or password');
            } else if (response.status === 422) {
                throw new Error('Invalid request format');
            } else {
                throw new Error('Login failed. Please try again.');
            }
        }
        
        const data = await response.json();
        
        if (!data.access_token) {
            throw new Error('No authentication token received');
        }
        
        // Store token in localStorage
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('username', username);
        
        // Redirect to todos page
        window.location.href = TODOS_PAGE;
        
    } catch (error) {
        console.error('Login error:', error);
        showError(error.message || 'An error occurred during login');
        
        // Re-enable submit button
        const submitBtn = document.querySelector('button[type="submit"]');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign In';
        
        // Clear password field
        document.getElementById('password').value = '';
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }
}

/**
 * Check if user is already authenticated
 */
function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    if (token) {
        // User is logged in, redirect to todos
        if (window.location.pathname === '/' || window.location.pathname.endsWith('index.html')) {
            window.location.href = TODOS_PAGE;
        }
    }
}

/**
 * Get authorization header
 */
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        redirectToLogin();
        return null;
    }
    
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

/**
 * Redirect to login page
 */
function redirectToLogin() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

/**
 * Logout user
 */
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
        window.location.href = '/';
    }
}
