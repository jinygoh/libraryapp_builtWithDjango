// This file contains the controller functions for user-related routes.
// The controller functions are responsible for handling the business logic of the application.
// They are called by the route handlers in the 'routes' directory.

const { User, Loan, Review } = require('../models');

// This function renders the user dashboard.
// It fetches the user's loans and reviews from the database.
exports.getDashboard = async (req, res, next) => {
  try {
    const userId = req.session.user.id;
    // Find all loans and reviews associated with the user.
    const loans = await Loan.findAll({ where: { userId }, include: ['Book'] });
    const reviews = await Review.findAll({ where: { userId }, include: ['Book'] });
    // Render the dashboard view with the user's data.
    res.render('dashboard', { layout: 'base', loans, reviews });
  } catch (error) {
    next(error);
  }
};

// This function renders the user profile page.
// It fetches the user's data from the database.
exports.getProfile = async (req, res, next) => {
  try {
    const userId = req.session.user.id;
    // Find the user by their ID.
    const user = await User.findByPk(userId);
    // Render the profile view with the user's data.
    res.render('profile', { layout: 'base', user });
  } catch (error) {
    next(error);
  }
};

// This function handles the user profile form submission.
// It updates the user's profile information in the database.
exports.postProfile = async (req, res, next) => {
  try {
    const userId = req.session.user.id;
    // Get the updated user data from the request body.
    const { first_name, last_name, email, date_of_birth } = req.body;
    // Find the user by their ID and update their profile.
    await User.update({ first_name, last_name, email, date_of_birth }, { where: { id: userId } });
    // Redirect to the profile page.
    req.flash('success_msg', 'Profile updated successfully');
    res.redirect('/profile');
  } catch (error) {
    next(error);
  }
};
