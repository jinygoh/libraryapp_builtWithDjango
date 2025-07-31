// This file defines the route for the home page.
// It uses the Express.Router class to create a modular, mountable route handler.

const express = require('express');
const router = express.Router();
const indexController = require('../controllers/indexController');

// This route renders the home page.
// The GET request to the root URL ('/') is handled by the 'getHome' function in the 'indexController'.
router.get('/', indexController.getHome);

module.exports = router;
