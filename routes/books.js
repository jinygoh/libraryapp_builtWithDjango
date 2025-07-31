// This file defines the book-related routes for the application.
// It uses the Express.Router class to create a modular, mountable route handler.
// The routes defined in this file are responsible for handling book searches, book details, borrowing, and returning books.

const express = require('express');
const router = express.Router();
const bookController = require('../controllers/bookController');
const { isAuthenticated } = require('../middleware/auth');

// This route handles book searches.
// This route is public and does not require authentication.
// The GET request to '/search' is handled by the 'searchBooks' function in the 'bookController'.
router.get('/search', bookController.searchBooks);

// This route renders the detail page for a specific book.
// This route is public and does not require authentication.
// The GET request to '/book/:bookId' is handled by the 'getBookDetail' function in the 'bookController'.
// The ':bookId' part is a route parameter that captures the book's ID from the URL.
router.get('/book/:bookId', bookController.getBookDetail);

// This route handles borrowing a book.
// The 'isAuthenticated' middleware is used to protect this route.
// The POST request to '/book/:bookId/borrow' is handled by the 'borrowBook' function in the 'bookController'.
router.post('/book/:bookId/borrow', isAuthenticated, bookController.borrowBook);

// This route handles returning a book.
// The 'isAuthenticated' middleware is used to protect this route.
// The POST request to '/loan/:loanId/return' is handled by the 'returnBook' function in the 'bookController'.
router.post('/loan/:loanId/return', isAuthenticated, bookController.returnBook);

// This route handles submitting a review for a book.
// The 'isAuthenticated' middleware is used to protect this route.
// The POST request to '/book/:bookId/review' is handled by the 'postReview' function in the 'bookController'.
router.post('/book/:bookId/review', isAuthenticated, bookController.postReview);


module.exports = router;
