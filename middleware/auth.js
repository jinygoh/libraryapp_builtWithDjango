// This file contains the authentication and authorization middleware for the application.
// The middleware functions are used to protect routes that require authentication or staff privileges.

// This middleware function checks if a user is authenticated.
// It is used to protect routes that should only be accessible to logged-in users.
exports.isAuthenticated = (req, res, next) => {
  // The 'req.session.user' object will be set upon successful login.
  if (req.session.user) {
    // If the user is authenticated, continue to the next middleware or route handler.
    return next();
  }
  // If the user is not authenticated, redirect them to the login page.
  req.flash('error_msg', 'Please log in to view this resource');
  res.redirect('/login');
};

// This middleware function checks if a user is a staff member.
// It is used to protect routes that should only be accessible to staff members.
exports.isStaff = (req, res, next) => {
  // The 'req.session.user' object will be set upon successful login.
  // The 'is_staff' property will be true for staff members.
  if (req.session.user && req.session.user.is_staff) {
    // If the user is a staff member, continue to the next middleware or route handler.
    return next();
  }
  // If the user is not a staff member, redirect them to the home page with an error message.
  req.flash('error_msg', 'You are not authorized to view this resource');
  res.redirect('/');
};
