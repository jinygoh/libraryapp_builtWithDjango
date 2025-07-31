// This file contains the controller functions for authentication-related routes.
// The controller functions are responsible for handling the business logic of the application.
// They are called by the route handlers in the 'routes' directory.

const { User } = require('../models');
const nodemailer = require('nodemailer');

// This function renders the login page.
exports.getLogin = (req, res, next) => {
  res.render('login', { layout: 'base' });
};

// This function handles the login form submission.
// It authenticates the user and creates a session for them.
exports.postLogin = async (req, res, next) => {
  const { username, password } = req.body;
  try {
    // Find the user by their username.
    const user = await User.findOne({ where: { username } });
    if (!user) {
      // If the user is not found, redirect to the login page with an error message.
      req.flash('error_msg', 'Invalid username or password');
      return res.redirect('/login');
    }
    // Check if the user's account is blocked.
    if (user.is_blocked) {
        // If the account is blocked, redirect to the login page with an error message.
        req.flash('error_msg', 'This account has been blocked.');
        return res.redirect('/login');
    }
    // Check if the provided password is valid.
    const isValid = await user.validPassword(password);
    if (!isValid) {
      // If the password is not valid, redirect to the login page with an error message.
      req.flash('error_msg', 'Invalid username or password');
      return res.redirect('/login');
    }
    // If the user is a staff member, redirect to the admin dashboard.
    req.session.user = user;
    if (user.is_staff) {
        return res.redirect('/staff');
    }
    // If the user is a regular user, redirect to the user dashboard.
    res.redirect('/dashboard');
  } catch (error) {
    next(error);
  }
};

// This function renders the registration page.
exports.getRegister = (req, res, next) => {
  res.render('register', { layout: 'base' });
};

// This function handles the registration form submission.
// It creates a new user and sends a confirmation email.
exports.postRegister = async (req, res, next) => {
  const { first_name, last_name, email, username, password } = req.body;
  try {
    // Create a new user in the database.
    const user = await User.create({ first_name, last_name, email, username, password });
    // Send a confirmation email.
    // Nodemailer setup and email sending will be implemented later.
    /*
    const transporter = nodemailer.createTransport({ ... });
    await transporter.sendMail({
        from: 'no-reply@library.com',
        to: user.email,
        subject: 'Registration successful',
        text: 'Welcome to the library!'
    });
    */
    // Redirect to the registration complete page.
    req.flash('success_msg', 'You are now registered and can log in');
    res.redirect('/login');
  } catch (error) {
    next(error);
  }
};

// This function handles user logout.
exports.getLogout = (req, res, next) => {
    req.session.destroy(() => {
        res.redirect('/');
    });
};

// This function renders the registration complete page.
exports.getRegistrationComplete = (req, res, next) => {
    res.render('registration_complete', { layout: 'base' });
};
