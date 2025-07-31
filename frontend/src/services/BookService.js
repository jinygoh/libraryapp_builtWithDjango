/**
 * This service handles API calls for book-related data.
 */
import axios from 'axios';

const API_URL = '/api/';

/**
 * Searches for books.
 * @param {string} query - The search query.
 * @returns {Promise} - A promise that resolves with the response from the API.
 */
const searchBooks = (query) => {
  return axios.get(API_URL + `search/?q=${query}`);
};

/**
 * Gets a single book by its ID.
 * @param {number} id - The ID of the book.
 * @returns {Promise} - A promise that resolves with the response from the API.
 */
const getBook = (id) => {
  return axios.get(API_URL + `book/${id}/`);
};

const BookService = {
  searchBooks,
  getBook,
};

export default BookService;
