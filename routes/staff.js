// This file defines the staff-related routes for the application.
// It uses the Express.Router class to create a modular, mountable route handler.
// The routes defined in this file are responsible for handling administrative tasks.

const express = require('express');
const router = express.Router();
const staffController = require('../controllers/staffController');
const { isAuthenticated, isStaff } = require('../middleware/auth');

// All routes in this file are protected by the 'isAuthenticated' and 'isStaff' middleware.
router.use(isAuthenticated, isStaff);

// This route renders the admin dashboard.
// The GET request to '/staff' is handled by the 'getDashboard' function in the 'staffController'.
router.get('/', staffController.getDashboard);

// This route renders the admin page for managing users.
// The GET request to '/staff/users' is handled by the 'getUsers' function in the 'staffController'.
router.get('/users', staffController.getUsers);

// This route handles blocking a user.
// The POST request to '/staff/users/block/:userId' is handled by the 'blockUser' function in the 'staffController'.
router.post('/users/block/:userId', staffController.blockUser);

// This route handles unblocking a user.
// The POST request to '/staff/users/unblock/:userId' is handled by the 'unblockUser' function in the 'staffController'.
router.post('/users/unblock/:userId', staffController.unblockUser);

// This route renders the admin page for managing books.
// The GET request to '/staff/books' is handled by the 'getBooks' function in the 'staffController'.
router.get('/books', staffController.getBooks);

// This route renders the page for adding a new book.
// The GET request to '/staff/books/add' is handled by the 'getAddBook' function in the 'staffController'.
router.get('/books/add', staffController.getAddBook);

// This route handles adding a new book.
// The POST request to '/staff/books/add' is handled by the 'postAddBook' function in the 'staffController'.
router.post('/books/add', staffController.postAddBook);

// This route renders the page for editing a book.
// The GET request to '/staff/books/edit/:bookId' is handled by the 'getEditBook' function in the 'staffController'.
router.get('/books/edit/:bookId', staffController.getEditBook);

// This route handles editing a book.
// The POST request to '/staff/books/edit/:bookId' is handled by the 'postEditBook' function in the 'staffController'.
router.post('/books/edit/:bookId', staffController.postEditBook);

// This route handles deleting a book.
// The POST request to '/staff/books/delete/:bookId' is handled by the 'deleteBook' function in the 'staffController'.
router.post('/books/delete/:bookId', staffController.deleteBook);

// This route sends bulk emails to users with overdue books.
// The POST request to '/staff/send_overdue_emails' is handled by the 'sendOverdueEmails' function in the 'staffController'.
router.post('/send_overdue_emails', staffController.sendOverdueEmails);

module.exports = router;
