// This file contains the controller function for the home page route.

// This function renders the home page.
exports.getHome = (req, res, next) => {
  res.render('home', { layout: 'base' });
};
