/**
 * This service handles API calls for user authentication.
 */
import axios from 'axios';

const API_URL = '/api/';

/**
 * Registers a new user.
 * @param {string} username - The user's username.
 * @param {string} email - The user's email.
 * @param {string} password - The user's password.
 * @returns {Promise} - A promise that resolves with the response from the API.
 */
const register = (username, email, password) => {
  return axios.post(API_URL + 'register/', {
    username,
    email,
    password,
  });
};

/**
 * Logs in a user.
 * @param {string} username - The user's username.
 * @param {string} password - The user's password.
 * @returns {Promise} - A promise that resolves with the response from the API.
 */
const login = (username, password) => {
  return axios
    .post(API_URL + 'login/', {
      username,
      password,
    })
    .then((response) => {
      // If the response contains a token, store it in local storage.
      if (response.data.token) {
        localStorage.setItem('user', JSON.stringify(response.data));
      }
      return response.data;
    });
};

/**
 * Logs out a user by removing the user object from local storage.
 */
const logout = () => {
  localStorage.removeItem('user');
};

/**
 * Gets the current user from local storage.
 * @returns {object} - The current user object.
 */
const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

const AuthService = {
  register,
  login,
  logout,
  getCurrentUser,
};

export default AuthService;
