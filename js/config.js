/**
 * API Configuration & Helper Functions
 * Centralized configuration for all API calls
 */

// API Base URL - Change this when deploying
const API_BASE_URL = "http://localhost:5000/api";

/**
 * Helper function to make API calls with authentication
 * @param {string} endpoint - API endpoint (e.g., '/auth/login')
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} body - Request body for POST/PUT requests
 * @returns {Promise} - API response promise
 */
async function apiCall(endpoint, method = "GET", body = null) {
  const token = localStorage.getItem("token");

  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  // Add authorization header if token exists
  if (token) {
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  // Add body if provided
  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

/**
 * Store authentication token
 * @param {string} token - JWT token from login
 */
function setAuthToken(token) {
  localStorage.setItem("token", token);
}

/**
 * Get authentication token
 * @returns {string} - JWT token
 */
function getAuthToken() {
  return localStorage.getItem("token");
}

/**
 * Clear authentication token on logout
 */
function clearAuthToken() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("loggedInUser");
}

/**
 * Store user information
 * @param {object} user - User object from login response
 */
function setUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
  localStorage.setItem("loggedInUser", JSON.stringify(user));
}

/**
 * Get stored user information
 * @returns {object} - User object
 */
function getUser() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

/**
 * Check if user is logged in
 * @returns {boolean} - True if logged in
 */
function isLoggedIn() {
  return !!getAuthToken();
}

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "/mainlogin.html";
  }
}

/**
 * Check user role
 * @param {string} role - Role to check (admin, student, teacher)
 * @returns {boolean} - True if user has this role
 */
function hasRole(role) {
  const user = getUser();
  return user && user.role === role;
}
