// This file configures a pre-configured instance of axios.
// This instance is used throughout the application to make API requests.

import axios from 'axios';

// Create a new axios instance.
const instance = axios.create({
    // The base URL for all API requests.
    baseURL: '/api'
});

// Add a request interceptor to the axios instance.
// This interceptor is called before each request is sent.
instance.interceptors.request.use(config => {
    // Get the JWT from local storage.
    const token = localStorage.getItem('token');
    // If the JWT is present, add it to the Authorization header of the request.
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    // Return the modified request configuration.
    return config;
});

// Export the pre-configured axios instance.
export default instance;
