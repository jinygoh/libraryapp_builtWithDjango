// This file defines the user-related routes for the application.
// It uses the Express.Router class to create a modular, mountable route handler.
// The routes defined in this file are responsible for handling the user dashboard and profile.

const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const { isAuthenticated } = require('../middleware/auth');

// This route renders the user dashboard.
// The 'isAuthenticated' middleware is used to protect this route.
// The GET request to '/dashboard' is handled by the 'getDashboard' function in the 'userController'.
router.get('/dashboard', isAuthenticated, userController.getDashboard);

// This route renders the user profile page.
// The 'isAuthenticated' middleware is used to protect this route.
// The GET request to '/profile' is handled by the 'getProfile' function in the 'userController'.
router.get('/profile', isAuthenticated, userController.getProfile);

// This route handles the user profile form submission.
// The 'isAuthenticated' middleware is used to protect this route.
// The POST request to '/profile' is handled by the 'postProfile' function in the 'userController'.
router.post('/profile', isAuthenticated, userController.postProfile);

module.exports = router;
