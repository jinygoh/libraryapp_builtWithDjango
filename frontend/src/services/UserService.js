/**
 * This service handles API calls for user-related data.
 */
import axios from 'axios';
import authHeader from './auth-header';

const API_URL = '/api/';

/**
 * Gets the user's dashboard data.
 * @returns {Promise} - A promise that resolves with the response from the API.
 */
const getDashboard = () => {
  return axios.get(API_URL + 'dashboard', { headers: authHeader() });
};

const UserService = {
  getDashboard,
};

export default UserService;
