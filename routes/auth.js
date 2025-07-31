// This file defines the authentication-related routes for the application.
// It uses the Express.Router class to create a modular, mountable route handler.
// The routes defined in this file are responsible for handling user login, registration, and logout.

const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// This route renders the login page.
// The GET request to '/login' is handled by the 'getLogin' function in the 'authController'.
router.get('/login', authController.getLogin);

// This route handles the login form submission.
// The POST request to '/login' is handled by the 'postLogin' function in the 'authController'.
router.post('/login', authController.postLogin);

// This route renders the registration page.
// The GET request to '/register' is handled by the 'getRegister' function in the 'authController'.
router.get('/register', authController.getRegister);

// This route handles the registration form submission.
// The POST request to '/register' is handled by the 'postRegister' function in the 'authController'.
router.post('/register', authController.postRegister);

// This route handles user logout.
// The GET request to '/logout' is handled by the 'getLogout' function in the 'authController'.
router.get('/logout', authController.getLogout);

// This route renders the registration complete page.
// The GET request to '/register/complete' is handled by the 'getRegistrationComplete' function in the 'authController'.
router.get('/register/complete', authController.getRegistrationComplete);


module.exports = router;
